import asyncio
from typing import AsyncIterable, Awaitable

from langchain.callbacks import AsyncIteratorCallbackHandler

from app.services.utils.normal_chat_flow_utils import generate_normal_output
from app.services.utils.rag_flow_utils import generate_rag_output
from app.common import mongo_logger


async def send_message_to_chat_flow(content: str) -> AsyncIterable[any]:

    callback = AsyncIteratorCallbackHandler()

    async def wrap_done(fn: Awaitable, event: asyncio.Event):
        try:
            await fn
        except Exception as e:
            mongo_logger.error(e)
        finally:
            event.set()

    task = asyncio.create_task(
        wrap_done(
            generate_normal_output(text=content, callback=callback),
            callback.done,
        )
    )

    async for token in callback.aiter():
        yield token

    await task


async def send_message_to_rag_flow(content: str) -> AsyncIterable[any]:

    callback = AsyncIteratorCallbackHandler()

    async def wrap_done(fn: Awaitable, event: asyncio.Event):
        try:
            await fn
        except Exception as e:
            mongo_logger.error(e)
        finally:
            event.set()

    task = asyncio.create_task(
        wrap_done(
            generate_rag_output(text=content, callback=callback),
            callback.done,
        )
    )

    async for token in callback.aiter():
        yield token

    await task
