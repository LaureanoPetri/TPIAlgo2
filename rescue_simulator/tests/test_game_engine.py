from src.game_engine import GameEngine
engine = GameEngine()
# Mock
class MockMapManager:
    def is_in_mine_area(self, pos):
        return False

    def get_resource_at(self, pos):
        return None

    def is_position_valid(self, pos):
        return True


