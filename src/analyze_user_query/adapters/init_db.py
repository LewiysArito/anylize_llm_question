import asyncio
from clickhouse_connect.driver.asyncclient import AsyncClient
from analyze_user_query.clickhouse_helper import Column 
from analyze_user_query.adapters.orm import analize_user_llm_query
from analyze_user_query.adapters.repository import get_async_client

async def create_table(client: AsyncClient, table: Column) -> None:
    sql = table.generate_sql_for_create(if_not_exists=True)
    await client.command(sql)

async def init_tables_clickhouse_if_not_exists(client: AsyncClient, tables: list[Column]) -> None:
    tasks = [create_table(client, table) for table in tables]
    await asyncio.gather(*tasks)

async def main():
    client = None
    try:
        client = await get_async_client()
        await init_tables_clickhouse_if_not_exists(client, tables=[analize_user_llm_query])
    except Exception as e:
        raise
    finally:
        if client:
            await client.close()

if __name__ == "__main__":
    asyncio.run(main())