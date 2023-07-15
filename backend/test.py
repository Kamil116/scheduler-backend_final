from unittest.mock import AsyncMock
import pytest

from backend.fsm import start_handler, start_menu, SettingsStates, select_course
from backend.utils.helpers import make_row_keyboard


@pytest.mark.asyncio
async def test_start_handler_without_proper_action():
    message = AsyncMock()
    state = SettingsStates.start  # Replace with the appropriate state object

    await start_handler(message, state)

    message.answer.assert_called_with(
        "Invalid action", reply_markup=make_row_keyboard(start_menu)
    )


@pytest.mark.asyncio
async def test_start_handler_with_proper_action():
    message = AsyncMock()
    state = SettingsStates.start

    await start_handler(message, state)


if __name__ == "__main__":
    pytest.main()
