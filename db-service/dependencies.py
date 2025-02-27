import os
from neo4j import AsyncGraphDatabase
from typing import AsyncGenerator

# refactor for better security
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://neo4j-db:7687")
NEO4J_USER = os.environ.get("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "test1234")

driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


async def get_db_session() -> AsyncGenerator:
    async with driver.session() as session:
        yield session


def close_db_connection():
    driver.close()
