# Feast: Redis to DragonflyDB Migration 

This showcases how to migrate a Feast feature store from Redis to DragonflyDB.

##  What This Demo Shows

1. Setting up Feast with Redis as the online store
2. Materializing features to Redis
3. Migrating to DragonflyDB (drop-in Redis replacement)
4. Verifying the migration works seamlessly

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- pip

##  Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start Redis and DragonflyDB

```bash
docker-compose up -d
```

This starts:
- **Redis** on port `6379`
- **DragonflyDB** on port `6380`

Verify containers are running:
```bash
docker ps
```

### Step 3: Generate Sample Data

```bash
python generate_sample_data.py
```

This creates sample user statistics data in `data/user_stats.parquet`.

### Step 4: Run Feast with Redis

```bash
python demo_redis.py
```

This will:
- Initialize Feast with Redis configuration
- Apply feature definitions
- Materialize features to Redis
- Fetch and display online features

### Step 5: Migrate to DragonflyDB

```bash
python migrate_to_dragonfly.py
```

This demonstrates the migration by:
- Switching to DragonflyDB configuration
- Re-materializing features to DragonflyDB
- Fetching features from DragonflyDB
- Showing that everything works identically!

## Project Structure

```
.
├── README.md
├── requirements.txt
├── docker-compose.yml
├── generate_sample_data.py          # Generate sample data
├── demo_redis.py                    # Demo with Redis
├── migrate_to_dragonfly.py          # Migration script
├── compare_performance.py           # Performance comparison
├── feature_repo/
│   ├── feature_definitions.py       # Feast feature definitions
│   ├── feature_store_redis.yaml     # Redis configuration
│   └── feature_store_dragonfly.yaml # DragonflyDB configuration
└── data/
    ├── user_stats.parquet           # Sample data
    └── registry.db                  # Feast registry
```

## Key Migration Insight

The **only difference** between Redis and DragonflyDB configurations is the connection string:

**Redis (`feature_store_redis.yaml`):**
```yaml
online_store:
  type: redis
  connection_string: "localhost:6379"
```

**DragonflyDB (`feature_store_dragonfly.yaml`):**
```yaml
online_store:
  type: redis
  connection_string: "localhost:6380"
```

DragonflyDB is a drop-in replacement for Redis with the same API.


