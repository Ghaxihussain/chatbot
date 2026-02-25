import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect(
        user='myuser',
        password='mypass', 
        database='chatbotdb',
        host='localhost'
    )
    print("✅✅✅ IT WORKS!!! ✅✅✅")
    await conn.close()

asyncio.run(test())