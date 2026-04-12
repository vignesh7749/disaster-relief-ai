import os
import logging
import heapq
from typing import Tuple, List, Dict, Any
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Required environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy")

# ✅ OpenAI-style client (required by spec)
client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)


class SmartAgent:
    """
    Disaster logistics agent using:
    - A* pathfinding
    - Priority-based delivery selection
    - Battery-aware decision making
    """

    BATTERY_THRESHOLD: float = 25.0

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    def get_neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = node
        return [
            (x + 1, y), (x - 1, y),
            (x, y + 1), (x, y - 1),
            (x + 1, y + 1), (x - 1, y - 1),
            (x + 1, y - 1), (x - 1, y + 1),
        ]

    def astar(
        self,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        blocked: List[Tuple[int, int]],
    ) -> List[Tuple[int, int]]:

        open_set: List[Tuple[float, Tuple[int, int]]] = []
        heapq.heappush(open_set, (0.0, start))

        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {start: 0.0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return self._reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                if (
                    0 <= neighbor[0] < 10
                    and 0 <= neighbor[1] < 10
                    and neighbor not in blocked
                ):
                    tentative_g = g_score[current] + self.heuristic(current, neighbor)

                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score = tentative_g + self.heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score, neighbor))

        return []

    def _reconstruct_path(
        self,
        came_from: Dict[Tuple[int, int], Tuple[int, int]],
        current: Tuple[int, int],
    ) -> List[Tuple[int, int]]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

    def decide_action(self, state: Dict[str, Any]) -> Dict[str, Any]:
        location = tuple(state["vehicle_location"])
        blocked = [tuple(b) for b in state["blocked_cells"]]
        deliveries = state["pending_deliveries"]

        # 🔋 Battery-aware logic
        if state["battery_level"] < self.BATTERY_THRESHOLD:
            logger.info("STEP: Charging due to low battery")
            return {"charge": True}

        deliveries = sorted(
            deliveries,
            key=lambda d: {"high": 3, "medium": 2, "low": 1}[d["priority"]],
            reverse=True,
        )

        target = tuple(deliveries[0]["location"])
        path = self.astar(location, target, blocked)

        next_step = path[1] if len(path) > 1 else target

        logger.info(f"STEP: Moving to {next_step} using A*")

        return {"move": list(next_step)}


import requests

def run() -> None:
    agent = SmartAgent()

    logger.info("START")

    try:
        import requests
        state = requests.post(f"{API_BASE_URL}/reset").json()
    except Exception as e:
        logger.error(f"Failed to reset env: {e}")
        logger.info("END")
        return

    done = False

    while not done:
        try:
            deliveries = state.get("pending_deliveries", [])

            if not deliveries:
                logger.info("No pending deliveries")
                break

            action = agent.decide_action(state)

            result = requests.post(
                f"{API_BASE_URL}/step",
                json=action
            ).json()

            state = result.get("observation", {})
            done = result.get("done", True)

            logger.info(f"STEP: {result}")

        except Exception as e:
            logger.error(f"Error during step: {e}")
            break

    logger.info("END")
if __name__ == "__main__":
    run()
