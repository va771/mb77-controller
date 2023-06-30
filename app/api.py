import asyncio

import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse
import aioserial

from app.mb77 import MB77Command
from app.settings import config_loader

app = FastAPI()

# aioserial instance doesn't work properly if it is created into endpoint
# maybe close method was called incorrectly
MANAGED_DEVICES = [
    aioserial.AioSerial(
        port=c.port,
        baudrate=c.baudrate
    )
    for c in config_loader()
]


async def read_and_print(aioserial_instance):
    data: bytes = await aioserial_instance.read_async(4)
    data = data.strip(b"\r\n")
    return data


async def execute_command(aioserial_instance, cmd: MB77Command):
    expected_ack = cmd.value.ack
    ack, _ = await asyncio.gather(
        read_and_print(aioserial_instance),
        aioserial_instance.write_async(cmd.value.req)
    )
    if ack != expected_ack:
        raise ValueError(f"Incorrect acknowledgement for cmd={cmd}: "
                         f"expect {expected_ack} / actual {ack}")


@app.post("/mb77-07/{device_id}/reset")
async def manage_device(device_id: int):
    await execute_command(MANAGED_DEVICES[device_id], MB77Command.POWER_OFF)
    await asyncio.sleep(2)
    await execute_command(MANAGED_DEVICES[device_id], MB77Command.POWER_ON)
    return JSONResponse(content="ok")


@app.post("/mb77-07/{device_id}/power-on")
async def manage_device(device_id: int):
    await execute_command(MANAGED_DEVICES[device_id], MB77Command.POWER_ON)
    return JSONResponse(content="ok")


@app.post("/mb77-07/{device_id}/power-off")
async def manage_device(device_id: int):
    await execute_command(MANAGED_DEVICES[device_id], MB77Command.POWER_OFF)
    return JSONResponse(content="ok")


if __name__ == "__main__":
    uvicorn.run("api:app")
