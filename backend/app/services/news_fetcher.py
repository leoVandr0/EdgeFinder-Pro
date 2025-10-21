"""
Real News Fetcher - Get live forex news from ForexFactory and other sources
"""
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re

class NewsDataProvider:
    """
    Fetch real forex news from ForexFactory and other sources
    """

    def __init__(self):
        self.news_cache = []
        self.cache_timestamp = None
        self.cache_duration = timedelta(minutes=30)  # Update every 30 minutes
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    async def fetch_forexfactory_news(self) -> List[Dict]:
        """
        Scrape news from ForexFactory
        """
        news_items = []

        try:
            async with httpx.AsyncClient(timeout=15.0, headers=self.headers, follow_redirects=True) as client:
                # ForexFactory news page
                response = await client.get("https://www.forexfactory.com/news")

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Find news articles (structure may vary, this is a basic parser)
                    articles = soup.find_all('div', class_='news__item')

                    if not articles:
                        # Try alternative structure
                        articles = soup.find_all('article') or soup.find_all('div', class_='article')

                    for article in articles[:15]:  # Get up to 15 articles
                        try:
                            # Extract title
                            title_elem = article.find(['h1', 'h2', 'h3', 'h4', 'a'])
                            if not title_elem:
                                continue

                            title = title_elem.get_text(strip=True)

                            # Extract content/summary
                            content_elem = article.find(['p', 'div', 'span'])
                            content = content_elem.get_text(strip=True) if content_elem else title

                            # Extract time
                            time_elem = article.find(['time', 'span'], class_=re.compile('time|date'))
                            timestamp = datetime.utcnow()

                            if time_elem:
                                time_text = time_elem.get_text(strip=True)
                                # Parse relative times like "2 hours ago"
                                if 'hour' in time_text.lower():
                                    hours = int(re.search(r'\d+', time_text).group())
                                    timestamp = datetime.utcnow() - timedelta(hours=hours)
                                elif 'minute' in time_text.lower():
                                    minutes = int(re.search(r'\d+', time_text).group())
                                    timestamp = datetime.utcnow() - timedelta(minutes=minutes)
                                elif 'day' in time_text.lower():
                                    days = int(re.search(r'\d+', time_text).group())
                                    timestamp = datetime.utcnow() - timedelta(days=days)

                            news_items.append({
                                "title": title[:200],  # Limit title length
                                "content": content[:500],  # Limit content length
                                "source": "ForexFactory",
                                "timestamp": timestamp.isoformat(),
                                "url": "https://www.forexfactory.com/news"
                            })

                        except Exception as e:
                            print(f"Error parsing article: {e}")
                            continue

        except Exception as e:
            print(f"Error fetching ForexFactory news: {e}")

        return news_items

    async def fetch_investing_news(self) -> List[Dict]:
        """
        Fetch news from Investing.com RSS feed
        """
        news_items = []

        try:
            async with httpx.AsyncClient(timeout=15.0, headers=self.headers, follow_redirects=True) as client:
                # Investing.com forex news RSS feed - news_1.rss is specifically for forex/currency news
                response = await client.get("https://www.investing.com/rss/news_1.rss")

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'xml')
                    items = soup.find_all('item')[:15]

                    for item in items:
                        try:
                            title = item.find('title')
                            link_elem = item.find('link')
                            pub_date_elem = item.find('pubDate')

                            if not title:
                                continue

                            title_text = title.get_text(strip=True)
                            link_url = link_elem.get_text(strip=True) if link_elem else ""
                            pub_date_text = pub_date_elem.get_text(strip=True) if pub_date_elem else ""

                            # Parse timestamp  - Investing.com uses format: 2025-10-21 03:13:37
                            timestamp = datetime.utcnow()
                            if pub_date_text:
                                try:
                                    timestamp = datetime.strptime(pub_date_text, '%Y-%m-%d %H:%M:%S')
                                except:
                                    try:
                                        timestamp = datetime.strptime(pub_date_text, '%a, %d %b %Y %H:%M:%S')
                                    except:
                                        pass

                            news_items.append({
                                "title": title_text[:300],
                                "content": title_text[:500],  # Use title as content since RSS doesn't have description
                                "source": "Investing.com",
                                "timestamp": timestamp.isoformat(),
                                "url": link_url
                            })
                        except Exception as e:
                            print(f"Error parsing RSS item: {e}")
                            continue

        except Exception as e:
            print(f"Error fetching Investing.com news: {e}")

        return news_items

    async def fetch_dailyfx_news(self) -> List[Dict]:
        """
        Fetch news from DailyFX
        """
        news_items = []

        try:
            async with httpx.AsyncClient(timeout=15.0, headers=self.headers) as client:
                response = await client.get("https://www.dailyfx.com/feeds/market-news")

                if response.status_code == 200:
                    # Parse JSON or XML feed
                    try:
                        data = response.json()
                        articles = data.get('articles', [])[:10]

                        for article in articles:
                            news_items.append({
                                "title": article.get('displayTitle', ''),
                                "content": article.get('displayDescription', ''),
                                "source": "DailyFX",
                                "timestamp": article.get('publishDate', datetime.utcnow().isoformat()),
                                "url": f"https://www.dailyfx.com{article.get('url', '')}"
                            })
                    except:
                        pass

        except Exception as e:
            print(f"Error fetching DailyFX news: {e}")

        return news_items

    async def get_real_news(self, limit: int = 10) -> List[Dict]:
        """
        Get real news from multiple sources
        """
        # Check cache first
        if self.cache_timestamp and (datetime.utcnow() - self.cache_timestamp) < self.cache_duration:
            print(f"Returning {len(self.news_cache)} cached news articles")
            return self.news_cache[:limit]

        print("=" * 50)
        print("Fetching fresh news from sources...")
        print("=" * 50)

        # Fetch from multiple sources in parallel
        results = await asyncio.gather(
            self.fetch_investing_news(),  # Forex-specific RSS feed
            self.fetch_forexfactory_news(),  # ForexFactory news scraping
            self.fetch_dailyfx_news(),  # DailyFX news feed
            return_exceptions=True
        )

        # Combine all news
        all_news = []
        for i, result in enumerate(results):
            if isinstance(result, list):
                print(f"Source {i}: Fetched {len(result)} articles")
                all_news.extend(result)
            elif isinstance(result, Exception):
                print(f"Source {i}: Error - {result}")

        # Sort by timestamp (newest first)
        all_news.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

        # Update cache
        self.news_cache = all_news
        self.cache_timestamp = datetime.utcnow()

        print(f"Total: Fetched {len(all_news)} real news articles!")
        print("=" * 50)

        return all_news[:limit]


# Singleton instance
news_provider = NewsDataProvider()


async def get_real_forex_news(limit: int = 10) -> List[Dict]:
    """
    Get real forex news from multiple sources
    """
    return await news_provider.get_real_news(limit=limit)
