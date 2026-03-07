from fastapi import FastAPI
from contextlib import asynccontextmanager
from pathlib import Path

from ..database import SessionLocal
from ..services import GraphStore
from ..config import setting


async def update_env_file():
    """Automatically disable RESET_DB_ON_START flag after successful database seeding"""
    env_file = Path(".env")

    if not env_file.exists():
        return

    try:
        # Read file content
        content = env_file.read_text(encoding="utf-8")

        # Replace true with false
        new_content = content.replace(
            "INITIALIZE_GRAPH=true", "INITIALIZE_GRAPH=false"
        ).replace('INITIALIZE_GRAPH="true"', 'INITIALIZE_GRAPH="false"')

        # Write back only if there were changes
        if new_content != content:
            env_file.write_text(new_content, encoding="utf-8")
    except Exception as e:
        print(f"⚠️ Could not update .env file: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server started!!!")
    db = SessionLocal()

    if setting.INITIALIZE_GRAPH:
        print("🔄 Initializing graph data...")
        graph = GraphStore.load_graph()
        print("📊 Graph data initialized")

        # Automatically disable flag after successful seeding
        await update_env_file()
        print("📊 Graph initialization flag updated")

    db.close()

    yield