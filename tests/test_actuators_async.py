import asyncio

from src.actuators import Actuators


def test_run_async_inside_running_event_loop():
    actuators = Actuators.__new__(Actuators)

    async def run_test():
        async def operation():
            return "completed"

        return actuators._run_async(operation())

    assert asyncio.run(run_test()) == "completed"
