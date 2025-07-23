from pathlib import Path
from os import environ
from sys import path, exit

environ["SUMO_HOME"] = str(
    Path(environ["VIRTUAL_ENV"]) / "lib" / "python3.11" / "site-packages" / "sumo"
)

if "SUMO_HOME" in environ:
    tools = Path(environ.get("SUMO_HOME")) / "tools"
    path.append(tools)
    print(f"Pasta tools adicionada ao sys.path: {tools}")
else:
    exit("please declare environment variable 'SUMO_HOME'")

try:
    import traci
    from sumolib import checkBinary  # noqa

    print("traci importado com sucesso.")
except ModuleNotFoundError as e:
    print(f"Erro ao importar módulo: {e}")
    exit(
        "Certifique-se de que o SUMO e o Traci estão instalados corretamente e o caminho do SUMO_HOME está correto."
    )


BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    def __init__(self):
        self.sumocfg_filename: str = "config.sumocfg"
        self.sumocfg_filepath: str = str(
            BASE_DIR / "src" / "sumo_files" / self.sumocfg_filename
        )
        self.lane_length: int = 300  # meters
        self.speed_road_accidented: float = 1.0  # meters/seconds
        self.timing_to_slow_down_vehicle: int = 10  # seconds
        self.accident_duration_timeout: int = 1500  # seconds
        self.color_accident: tuple[int, int, int, int] = (255, 0, 0, 255)  # color red


settings = Config()
