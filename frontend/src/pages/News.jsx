import { useState, useEffect } from 'react';
import { newsAPI } from '../api/api';
import Card from '../components/Card';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { Newspaper, TrendingUp, TrendingDown, Minus } from 'lucide-react';

const News = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [news, setNews] = useState([]);
  const [sentiment, setSentiment] = useState(null);

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = async () => {
    try {
      setLoading(true);
      setError(null);

      const [newsRes, sentimentRes] = await Promise.all([
        newsAPI.getSummaries({ limit: 10 }),
        newsAPI.getSentiment(),
      ]);

      setNews(newsRes.data.articles);
      setSentiment(sentimentRes.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load news');
    } finally {
      setLoading(false);
    }
  };

  const getSentimentIcon = (sentiment) => {
    if (sentiment === 'positive') return <TrendingUp className="h-5 w-5 text-green-600" />;
    if (sentiment === 'negative') return <TrendingDown className="h-5 w-5 text-red-600" />;
    return <Minus className="h-5 w-5 text-gray-600" />;
  };

  const getSentimentBadge = (sentiment) => {
    const colors = {
      positive: 'bg-green-100 text-green-800',
      negative: 'bg-red-100 text-red-800',
      neutral: 'bg-gray-100 text-gray-800',
    };
    return colors[sentiment] || 'bg-gray-100 text-gray-800';
  };

  if (loading) return <LoadingSpinner message="Loading news..." />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Market News & Sentiment</h1>
        <button onClick={fetchNews} className="btn-primary">
          Refresh
        </button>
      </div>

      {/* Overall Sentiment */}
      {sentiment && (
        <Card title="Overall Market Sentiment">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <p className="text-sm text-gray-600 mb-2">Overall Sentiment</p>
              <div className="flex items-center justify-center">
                {getSentimentIcon(sentiment.overall_sentiment)}
                <p className={`ml-2 text-2xl font-bold ${
                  sentiment.overall_sentiment === 'positive' ? 'text-green-600' :
                  sentiment.overall_sentiment === 'negative' ? 'text-red-600' :
                  'text-gray-600'
                }`}>
                  {sentiment.overall_sentiment}
                </p>
              </div>
            </div>

            <div className="text-center">
              <p className="text-sm text-gray-600 mb-2">Sentiment Score</p>
              <p className={`text-2xl font-bold ${
                sentiment.sentiment_score > 0 ? 'text-green-600' :
                sentiment.sentiment_score < 0 ? 'text-red-600' :
                'text-gray-600'
              }`}>
                {sentiment.sentiment_score > 0 ? '+' : ''}{sentiment.sentiment_score.toFixed(3)}
              </p>
            </div>

            <div className="text-center">
              <p className="text-sm text-gray-600 mb-2">Articles Analyzed</p>
              <p className="text-2xl font-bold text-gray-900">{sentiment.total_articles}</p>
            </div>

            <div className="text-center">
              <p className="text-sm text-gray-600 mb-2">Breakdown</p>
              <div className="flex justify-center space-x-2 text-sm">
                <span className="text-green-600 font-semibold">
                  {sentiment.sentiment_breakdown.positive} +
                </span>
                <span className="text-gray-600 font-semibold">
                  {sentiment.sentiment_breakdown.neutral} =
                </span>
                <span className="text-red-600 font-semibold">
                  {sentiment.sentiment_breakdown.negative} -
                </span>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* News Articles */}
      <Card title={`Latest News (${news.length})`}>
        <div className="space-y-4">
          {news.map((article, idx) => (
            <div
              key={idx}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-start flex-1">
                  <Newspaper className="h-5 w-5 text-primary-600 mr-3 mt-1 flex-shrink-0" />
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">
                      {article.title}
                    </h3>
                    <div className="flex items-center space-x-3 text-sm text-gray-500">
                      <span>{article.source}</span>
                      <span>•</span>
                      <span>{new Date(article.timestamp).toLocaleString()}</span>
                    </div>
                  </div>
                </div>
                <span className={`px-2 py-1 rounded text-xs font-medium whitespace-nowrap ml-3 ${getSentimentBadge(article.sentiment)}`}>
                  {article.sentiment}
                </span>
              </div>

              <p className="text-gray-700 mb-3">{article.summary}</p>

              <div className="flex items-center justify-between pt-3 border-t border-gray-200">
                <div className="flex items-center text-sm">
                  <span className="text-gray-600 mr-2">Sentiment Score:</span>
                  <span className={`font-semibold ${
                    article.sentiment_score > 0 ? 'text-green-600' :
                    article.sentiment_score < 0 ? 'text-red-600' :
                    'text-gray-600'
                  }`}>
                    {article.sentiment_score > 0 ? '+' : ''}{article.sentiment_score.toFixed(3)}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default News;
