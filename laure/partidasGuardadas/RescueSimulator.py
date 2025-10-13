# rescue_simulator.py
from src.game_engine import GameEngine
import json, os

def main():
    # Cargar configuración (si existe)
    config_file = os.path.join("config", "default_config.json")
    config = None
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)

    juego = GameEngine(config)
    juego.start()

if __name__ == "__main__":
    main()
