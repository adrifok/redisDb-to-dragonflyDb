"""
Migration script from Redis to DragonflyDB
It just change the connection string.
"""
import os
import sys
import shutil
from datetime import datetime
from feast import FeatureStore
import pandas as pd
import redis

def verify_redis_data():
    """Verify data exists in Redis before migration"""
    print("\n Verifying data in Redis...")
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        keys = r.keys('*')
        print(f"✅ Found {len(keys)} keys in Redis")
        return len(keys) > 0
    except Exception as e:
        print(f"❌ Error connecting to Redis: {e}")
        return False

def verify_dragonfly_data():
    """Verify data exists in DragonflyDB after migration"""
    print("\n Verifying data in DragonflyDB...")
    try:
        r = redis.Redis(host='localhost', port=6380, decode_responses=True)
        keys = r.keys('*')
        print(f"✅ Found {len(keys)} keys in DragonflyDB")
        return len(keys) > 0
    except Exception as e:
        print(f"❌ Error connecting to DragonflyDB: {e}")
        return False

def main():
    print("=" * 60)
    print("MIGRATING FROM REDIS TO DRAGONFLYDB")
    print("=" * 60)
    
    # Verify Redis has data
    if not verify_redis_data():
        print("\n⚠️  No data found in Redis. Please run demo_redis.py first!")
        return
    
    # Change to feature_repo directory
    os.chdir('feature_repo')
    
    print("\n" + "=" * 60)
    print("MIGRATION STEPS")
    print("=" * 60)
    
    # Step 1: Switch to DragonflyDB configuration
    print("\n Switching to DragonflyDB configuration...")
    print("    Configuration change:")
    print("      Redis:       localhost:6379")
    print("      DragonflyDB: localhost:6380")
    shutil.copy('feature_store_dragonfly.yaml', 'feature_store.yaml')
    print("Switched to DragonflyDB at localhost:6380")
    
    # Step 2: Apply feature definitions (uses same registry)
    print("\n  Applying feature definitions to DragonflyDB...")
    os.system("feast apply")
    
    # Initialize Feast store
    store = FeatureStore(repo_path=".")
    
    # Step 3: Materialize features to DragonflyDB
    print("\n  Materializing features to DragonflyDB...")
    end_date = datetime.now()
    store.materialize(
        start_date=datetime(2025, 10, 1),
        end_date=end_date
    )
    print("Features materialized to DragonflyDB")
    
    # Verify DragonflyDB has data
    verify_dragonfly_data()
    
    # Step 4: Fetch online features from DragonflyDB
    print("\n Fetching online features from DragonflyDB...")
    entity_rows = [
        {"user_id": 1},
        {"user_id": 5},
        {"user_id": 10},
    ]
    
    features = store.get_online_features(
        features=[
            "user_stats:total_orders",
            "user_stats:total_spent",
            "user_stats:avg_order_value",
        ],
        entity_rows=entity_rows,
    ).to_dict()
    
    # Display results
    print("\nRetrieved Features from DragonflyDB:")
    print("-" * 60)
    df = pd.DataFrame(features)
    print(df.to_string(index=False))
    
    print("\n" + "=" * 60)
    print("MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n Key Takeaway:")
    print("   Migration was as simple as changing the connection string!")
    print("   Redis:       localhost:6379")
    print("   DragonflyDB: localhost:6380")
    print("\n DragonflyDB Benefits:")
    print("   • Drop-in Redis replacement")
    print("   • Better performance and scalability")
    print("   • Lower memory footprint")
    print("   • Full Redis API compatibility")
    
    # Change back to original directory
    os.chdir('..')

if __name__ == "__main__":
    main()
