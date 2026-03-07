from fastapi import FastAPI
from contextlib import asynccontextmanager
from pathlib import Path

from ..database import SessionLocal
from ..services import GraphStore
from ..config import setting
from .seeder import DatabaseSeeder


async def update_env_file(
    initialize_graph: bool | None = None,
    seed_database: bool | None = None,
):
    """Update .env feature flags after successful startup tasks."""
    env_file = Path(".env")

    if not env_file.exists():
        return

    try:
        # Read file content
        content = env_file.read_text(encoding="utf-8")

        new_content = content

        if initialize_graph is not None:
            new_content = (
                new_content.replace("INITIALIZE_GRAPH=true", f"INITIALIZE_GRAPH={str(initialize_graph).lower()}")
                .replace('INITIALIZE_GRAPH="true"', f'INITIALIZE_GRAPH="{str(initialize_graph).lower()}"')
                .replace("INITIALIZE_GRAPH=false", f"INITIALIZE_GRAPH={str(initialize_graph).lower()}")
                .replace('INITIALIZE_GRAPH="false"', f'INITIALIZE_GRAPH="{str(initialize_graph).lower()}"')
            )

        if seed_database is not None:
            new_content = (
                new_content.replace("SEED_DATABASE=true", f"SEED_DATABASE={str(seed_database).lower()}")
                .replace('SEED_DATABASE="true"', f'SEED_DATABASE="{str(seed_database).lower()}"')
                .replace("SEED_DATABASE=false", f"SEED_DATABASE={str(seed_database).lower()}")
                .replace('SEED_DATABASE="false"', f'SEED_DATABASE="{str(seed_database).lower()}"')
            )

        # Write back only if there were changes
        if new_content != content:
            env_file.write_text(new_content, encoding="utf-8")
    except Exception as e:
        print(f"⚠️ Could not update .env file: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server started!!!")
    db = SessionLocal()

    print("🔄 Loading graph into memory cache...")
    GraphStore.get_graph()
    print("📊 Graph loaded in memory cache")

    if setting.INITIALIZE_GRAPH:
        print("🔄 Initializing graph data...")
        graph = GraphStore.get_graph(force_reload=True)
        print("📊 Graph data initialized")

        # Automatically disable flag after successful seeding
        await update_env_file(initialize_graph=False)
        print("📊 Graph initialization flag updated")

    if setting.SEED_DATABASE:
        print("🔄 Seeding database with demo users...")
        seed_stats = DatabaseSeeder.seed_users(db)
        print(f"📊 Database seeded: {seed_stats}")

        await update_env_file(seed_database=False)
        print("📊 Database seeding flag updated")

    db.close()

    yield