class MockVehicle:
    """Vehículo de prueba para simular movimiento y posición"""
    def __init__(self, name, initial_position=(0,0)):
        self.name = name
        self.position = initial_position
        self.collected_resources = 0
        self.active = True  # Indica si está operativo

class GameEngine:
    def __init__(self, map_manager, players):
        self.map_manager = map_manager
        self.players = players
        self.tick = 0
        self.vehicles = []
        self.score = 0
        self.init_vehicles()

    def init_vehicles(self):
        """Inicializa vehículos de prueba"""
        self.vehicles.append(MockVehicle("Jeep1", (0,0)))
        self.vehicles.append(MockVehicle("Moto1", (0,0)))
        self.vehicles.append(MockVehicle("Camion1", (0,0)))

    def advance_tick(self):
        """Avanza la simulación un tick, preparado para integración real"""
        self.tick += 1
        print(f"\n=== Tick {self.tick} ===")

        for vehicle in self.vehicles:
            if not vehicle.active:
                continue  # Ignorar vehículos destruidos

            # --- Movimiento ---
            # Se llama a una función auxiliar que luego definirá la estrategia real
            vehicle.position = self.calculate_next_position(vehicle)

            # --- Recolección ---
            collected = self.collect_resources(vehicle)
            vehicle.collected_resources += collected

            # --- Chequeo de minas y colisiones ---
            if self.check_mines(vehicle) or self.check_collisions(vehicle):
                vehicle.active = False
                print(f"{vehicle.name} ha sido destruido!")

            # --- Puntaje ---
            if self.at_base(vehicle) and vehicle.collected_resources > 0:
                self.score += vehicle.collected_resources
                print(f"{vehicle.name} entrega {vehicle.collected_resources} recursos a la base")
                vehicle.collected_resources = 0

            # Mostrar estado actual
            print(f"{vehicle.name} posición: {vehicle.position}, recursos: {vehicle.collected_resources}")

        print(f"Puntaje total: {self.score}")


    # --- Funciones auxiliares (placeholders) ---

    def calculate_next_position(self, vehicle):
        """Devuelve la próxima posición según estrategia (temporal: 1 a la izquierda)"""
        # Mismo comportamiento de juguete por ahora
        return (vehicle.position[0] + 1, vehicle.position[0])

    def collect_resources(self, vehicle):
        """Devuelve cantidad de recursos recolectados en la posición actual"""
        # Por ahora devuelve 1 por tick; luego usar map_manager
        return 1

    def check_mines(self, vehicle):
        """Devuelve True si el vehículo entra en área de mina"""
        # Placeholder; luego usar map_manager
        return False

    def check_collisions(self,vehicle):
        positions = {}
        for v in self.vehicles:
            if not v.active:
                continue
            if v.position in positions:
                # Colisión detectada
                other = positions[v.position]
                print(f"Colisión entre {v.name} y {other.name} en {v.position}")
                v.active = False
                other.active = False
            else:
                positions[v.position] = v


    def at_base(self, vehicle):
        """Devuelve True si el vehículo está en la base"""
        # Placeholder; luego usar posición de la base del jugador
        return vehicle.position[0] >= 5  # ejemplo temporal

    def start_simulation(self):
        pass
 
    def update_score(self):
        """Actualiza el puntaje total en base a recursos entregados"""
        for vehicle in self.vehicles:
            if vehicle.active and self.at_base(vehicle):
                if vehicle.collected_resources > 0:
                    self.score += vehicle.collected_resources
                    print(f"{vehicle.name} entrega {vehicle.collected_resources} recursos a la base.")
                    vehicle.collected_resources = 0

    def is_simulation_over(self):
        # Termina cuando todos los vehículos están inactivos
        return all(not v.active for v in self.vehicles)

    def get_game_state(self):
        return {
            "tick": self.tick,
            "score": self.score,
            "vehicles": [
                {
                    "name": v.name,
                    "position": v.position,
                    "resources": v.collected_resources,
                    "active": v.active
                }
                for v in self.vehicles
            ]
        }

if __name__ == "__main__":
    # Crear instancia del GameEngine
    engine = GameEngine(map_manager=None, players=[])  # Por ahora mocks o vacíos

    # Simular 3 ticks
    for _ in range(3):
        engine.advance_tick()
    
    # Mostrar el estado final
    print("\n=== Estado final del juego ===")
    state = engine.get_game_state()
    print(state)
