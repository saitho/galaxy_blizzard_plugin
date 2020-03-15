import os
import asyncio
import json
from unittest.mock import Mock

import pytest
from galaxy.api.types import Achievement

from tests.async_mock import AsyncMock

# pytest-asyncio: all test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

OW_ID = '5272175'


@pytest.fixture()
def ow_player_achievements_response():
    return [{
        "name": "Achievement A",
        "description": "Description Achievement A",
        "api_key": "achievementa",
        "image_url": None,
        "unlocked": True
    }, {
        "name": "Achievement B",
        "description": "Description Achievement B",
        "api_key": "achievementb",
        "image_url": None,
        "unlocked": False
    }]

@pytest.fixture()
def ow_player_achievements_response_private():
    return []

async def test_overwatch_achievements(
    pg, backend_mock, ow_player_achievements_response
):
    backend_mock.get_ow_player_achievements.return_value = ow_player_achievements_response

    ctx = await pg.prepare_achievements_context([OW_ID])
    result = await pg.get_unlocked_achievements(OW_ID, ctx)

    # assert only unlocked achievements
    assert len(result) == 1
    assert result[0] == Achievement(achievement_id='achievementa', unlock_time=None)

async def test_overwatch_achievements_private_profile(pg, backend_mock, ow_player_achievements_response_private):
    backend_mock.get_ow_player_achievements.return_value = ow_player_achievements_response_private

    ctx = await pg.prepare_achievements_context([OW_ID])
    result = await pg.get_unlocked_achievements(OW_ID, ctx)

    assert len(result) == 0
