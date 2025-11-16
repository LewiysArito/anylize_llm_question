import asyncio
from clickhouse_connect.driver.asyncclient import AsyncClient
from analyze_user_query.clickhouse_helper import Table
from analyze_user_query.adapters.orm import analyze_user_llm_query
from analyze_user_query.adapters.repository import get_async_client
from analyze_user_query import config

logger = config.logger

async def create_table(client: AsyncClient, table: Table) -> None:
    sql = table.generate_sql_for_create(if_not_exists=True)
    try:
        await client.command(sql)
        logger.info(f"Table `{table.table_name}` created (or already exists).")
    except Exception as e:
        logger.error(f"Failed to create table `{table.table_name}`: {e}")
        raise
    await client.command(sql)

async def init_tables_clickhouse_if_not_exists(client: AsyncClient, tables: list[Table]) -> None:
    tasks = [create_table(client, table) for table in tables]
    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        logger.error(f"Error initializing tables: {e}")
        raise

async def main():
    client = None
    try:
        client = await get_async_client()
        await init_tables_clickhouse_if_not_exists(client, tables=[analyze_user_llm_query])
    except Exception as e:
        logger.error(f"Fatal error during ClickHouse initialization: {e}")
        raise
    finally:
        if client:
            await client.close()

if __name__ == "__main__":
    asyncio.run(main())