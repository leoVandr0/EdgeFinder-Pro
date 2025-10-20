#!/usr/bin/env python3
"""
Seed database with sample data for testing and development.
Run this script after deploying to populate initial data.
"""

import json
import asyncio
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.db import connect_mongodb, init_postgres, get_postgres_engine, get_session_maker
from app.services.db import StrengthDB, InsightDB
from app.services.analytics import generate_trade_insights
from sqlalchemy import select


async def load_mongodb_data():
    """Load events into MongoDB"""
    print("Loading MongoDB data...")

    mongo_db = await connect_mongodb()
    if not mongo_db:
        print("MongoDB not configured, skipping...")
        return

    # Load events
    with open(os.path.join(os.path.dirname(__file__), 'sample_events.json')) as f:
        events = json.load(f)

    # Add timestamps to events
    for i, event in enumerate(events):
        event['timestamp'] = (datetime.utcnow() + timedelta(days=i)).isoformat()

    # Insert into MongoDB
    events_collection = mongo_db.events
    await events_collection.delete_many({})  # Clear existing
    result = await events_collection.insert_many(events)

    print(f"✓ Loaded {len(result.inserted_ids)} events into MongoDB")


async def load_postgres_data():
    """Load strength and insights into PostgreSQL"""
    print("Loading PostgreSQL data...")

    engine = get_postgres_engine()
    await init_postgres()

    SessionLocal = get_session_maker(engine)

    async with SessionLocal() as session:
        # Load strength data
        with open(os.path.join(os.path.dirname(__file__), 'sample_strength.json')) as f:
            strengths = json.load(f)

        # Clear existing data
        await session.execute(select(StrengthDB))
        await session.commit()

        # Insert strength data
        for currency, data in strengths.items():
            strength = StrengthDB(
                currency=currency,
                strength_score=data['base_score'],
                momentum=0.0,
                trend='neutral',
                rank=0
            )
            session.add(strength)

        await session.commit()
        print(f"✓ Loaded {len(strengths)} currency strengths into PostgreSQL")

        # Generate and load insights
        insights_data = generate_trade_insights(limit=20)

        for insight_dict in insights_data:
            insight = InsightDB(
                pair=insight_dict['pair'],
                signal_type=insight_dict['signal_type'],
                confidence=insight_dict['confidence'],
                entry_price=insight_dict['entry_price'],
                stop_loss=insight_dict['stop_loss'],
                take_profit=insight_dict['take_profit'],
                reasoning=insight_dict['reasoning'],
                timeframe=insight_dict['timeframe']
            )
            session.add(insight)

        await session.commit()
        print(f"✓ Loaded {len(insights_data)} trade insights into PostgreSQL")


async def main():
    """Main seed function"""
    print("=" * 50)
    print("EdgeFinder Pro - Database Seeder")
    print("=" * 50)

    try:
        # Load data
        await load_postgres_data()
        await load_mongodb_data()

        print("\n" + "=" * 50)
        print("✓ Database seeding completed successfully!")
        print("=" * 50)

    except Exception as e:
        print(f"\n✗ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
