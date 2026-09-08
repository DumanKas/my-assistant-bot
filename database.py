import asyncio
import asyncpg
import os
import numpy as np
from pgvector.asyncpg import register_vector
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

DATABASE_URL = os.getenv("DATABASE_URL")


def get_embedding(text: str):
    embedding = model.encode(text)
    return embedding.tolist()

async def init_connection(conn):
    await register_vector(conn)
async def create_pool():
    pool = await asyncpg.create_pool(
    dsn = DATABASE_URL,
    init = init_connection,
)
    return pool
async def init_db(pool):
    async with pool.acquire() as conn:
        await conn.execute('''CREATE EXTENSION IF NOT EXISTS vector''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS history(
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        embedding vector(384),
        created_at TIMESTAMP DEFAULT NOW())''')

        await conn.execute('''CREATE INDEX ON history USING ivfflat (embedding vector_cosine_ops)''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS note(id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        text TEXT NOT NULL)''')





async def save_message(pool,user_id: int,role: str, content: str):
    embedding = await asyncio.to_thread(get_embedding, content)
    async with pool.acquire() as conn:
        await conn.execute('''
        INSERT INTO history(user_id,role,content,embedding) VALUES($1 ,$2 ,$3, $4)''', user_id, role, content,embedding)


async def get_history(pool, user_id: int):
    async with pool.acquire() as conn:
        rows = await conn.fetch('''SELECT * FROM history WHERE user_id = $1 ''', user_id)
        return [{"role": row["role"], "content": row["content"]} for row in rows]



async def clear_history(pool, user_id: int):
    async with pool.acquire() as conn:
        await conn.execute('''
        DELETE FROM history WHERE user_id = $1 ''', user_id)


async def save_note(pool, user_id: int, text: str):
    async with pool.acquire() as conn:
        await conn.execute('''INSERT INTO note(user_id, text) VALUES($1, $2)''', user_id,text)

async def get_notes(pool, user_id: int):
    async with pool.acquire() as conn:
        rows = await conn.fetch('''SELECT * FROM note WHERE user_id = $1 ''', user_id)
        return [{"text": row['text']} for row in rows]



async def get_similar_messages(pool, user_id, question: str, top_k: int = 3, exclude_ids = None):
    question_embedding = await asyncio.to_thread(get_embedding, question)
    exclude_ids = exclude_ids or []
    async with pool.acquire() as conn:
        rows = await conn.fetch('''
        SELECT * FROM history 
        WHERE user_id = $1 AND embedding IS NOT NULL AND id != ALL($2 :: int[])
        ORDER BY embedding <=> $3 
        LIMIT $4''',
        user_id,exclude_ids, question_embedding, top_k)
        return [{"role": row['role'], "content": row['content']} for row in rows]


async def get_recent_messages(pool, user_id, limit=5):
    async with pool.acquire() as conn:
        rows = await conn.fetch('''
        SELECT id,role,content FROM history
        WHERE user_id = $1
        ORDER BY created_at DESC
        LIMIT $2''', user_id, limit)

        messages = [{"id": row['id'], "role": row['role'], "content": row['content']} for row in rows]
        return list(reversed(messages))


async def get_context(pool, user_id: int, question: str, top_k: int = 3, recent_limit: int = 5):
    recent_messages = await get_recent_messages(pool, user_id, limit=recent_limit)
    recent_ids = [m['id'] for m in recent_messages]
    similar_messages = await get_similar_messages(pool, user_id, question, top_k=top_k,exclude_ids=recent_ids)
    result = recent_messages + similar_messages
    return result
