# Tidal Force Robotics
# 2021, Email Blaster
# MIT License


import logging
import asyncio
from email_blaster.shutdown import shutdown


def handle_exception(loop, context):
    # context["message"] will always be there; but context["exception"] may not
    msg = context.get("exception", context["message"])
    logging.error(f"Caught exception: {msg}")
    logging.info("Shutting down...")
    asyncio.create_task(shutdown(loop))
