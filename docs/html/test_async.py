import asyncio
import pytest


async def return_true():
    return True


@pytest.mark.asyncio
async def test_pass():
    assert True


@pytest.mark.asyncio
async def test_fail():
    assert False


def test_loop(event_loop):
    assert event_loop.run_until_complete(return_true()) == True
