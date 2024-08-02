import asyncio
from simulation import Simulation


async def listen_for_pause(simulation):
    while True:
        await asyncio.get_event_loop().run_in_executor(None, input, "Нажмите Enter для переключения паузы:")
        await simulation.pause_simulation()


async def main():
    simulation = Simulation(5, 5)
    await asyncio.gather(
        simulation.start_simulation(),
        listen_for_pause(simulation)

    )

if __name__ == "__main__":
    asyncio.run(main())
