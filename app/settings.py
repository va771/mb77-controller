import dataclasses
from configparser import ConfigParser
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "config.ini"


@dataclasses.dataclass
class SerialDevice:
    port: str
    baudrate: int


def config_loader() -> list[SerialDevice]:
    config = ConfigParser()
    config.read(CONFIG_FILE)
    section = config["managed devices"]
    managed_devices: list[SerialDevice] = []
    for d in section:
        port, br = section[d].split(",")
        managed_devices.append(SerialDevice(port=port, baudrate=br))
    return managed_devices


if __name__ == "__main__":
    print(config_loader())
