import pytest

import httpx


@pytest.mark.usefixtures("async_environment")
async def test_read_timeout(server):
    timeout = httpx.Timeout(None, read=1e-6)

    async with httpx.AsyncClient(timeout=timeout) as client:
        with pytest.raises(httpx.ReadTimeout):
            await client.get(server.url.copy_with(path="/slow_response"))


@pytest.mark.usefixtures("async_environment")
async def test_write_timeout(server):
    timeout = httpx.Timeout(None, write=1e-6)

    async with httpx.AsyncClient(timeout=timeout) as client:
        with pytest.raises(httpx.WriteTimeout):
            data = b"*" * 1024 * 1024 * 100
            await client.put(server.url.copy_with(path="/slow_response"), content=data)


@pytest.mark.usefixtures("async_environment")
async def test_connect_timeout(server):
    timeout = httpx.Timeout(None, connect=1e-6)

    async with httpx.AsyncClient(timeout=timeout) as client:
        with pytest.raises(httpx.ConnectTimeout):
            # See https://stackoverflow.com/questions/100841/
            await client.get("http://10.255.255.1/")


@pytest.mark.usefixtures("async_environment")
async def test_pool_timeout(server):
    limits = httpx.Limits(max_connections=1)
    timeout = httpx.Timeout(None, pool=1e-4)

    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
        async with client.stream("GET", server.url):
            with pytest.raises(httpx.PoolTimeout):
                await client.get("http://localhost:8000/")
