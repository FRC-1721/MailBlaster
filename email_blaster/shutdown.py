# Tidal Force Robotics
# 2021, Email Blaster
# MIT License


import logging


async def shutdown(loop, signal=None):
    """Cleanup tasks tied to the service's shutdown."""
    if signal:
        logging.info(f"Received exit signal {signal.name}...")
    logging.info("Closing database connections")
    loop.close()
