import asyncpg
import asyncio

async def test_connection():
    try:
        conn = await asyncpg.connect(
            user='postgres',
            password='password',
            database='pomodoro',
            host='0.0.0.0',
            port=5432
        )
        await conn.close()
        print("Connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")

asyncio.run(test_connection())