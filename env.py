import logging
import math
from typing import List, Tuple, Dict

from models import Observation, Action, Reward, Delivery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DisasterEnv:
    """
    Disaster Relief Logistics Environment.
    Includes:
    - Blocked roads
    - Priority deliveries
    """

    def __init__(self) -> None:
        self.grid_size = 10
        self.max_battery = 100.0
        self.reset()

    def reset(self) -> Observation:
        """Initialize environment."""
        self.vehicle_location = (0, 0)
        self.battery_level = self.max_battery
        self.time_elapsed = 0.0

        self.blocked_cells: List[Tuple[int, int]] = [(2, 2), (4, 5)]

        self.pending_deliveries: List[Delivery] = [
            Delivery(location=(5, 5), priority="high"),
            Delivery(location=(7, 2), priority="medium"),
            Delivery(location=(8, 8), priority="low"),
        ]

        self.successful_deliveries = 0

        logger.info("Environment reset")
        return self.state()

    def step(self, action: Action):
        """Execute action."""
        distance = 0.0
        penalty = 0.0
        reward_value = 0.0

        if action.move:
            new_loc = action.move

            # 🚧 Check blocked path
            if new_loc in self.blocked_cells:
                penalty -= 10
                logger.warning("Hit blocked cell!")
            else:
                distance = math.dist(self.vehicle_location, new_loc)
                self.vehicle_location = new_loc
                self.battery_level -= distance * 2

        if action.charge:
            self.battery_level = min(self.max_battery, self.battery_level + 20)

        # 📦 Delivery check
        for delivery in self.pending_deliveries[:]:
            if delivery.location == self.vehicle_location:
                reward_value += self._priority_reward(delivery.priority)
                self.pending_deliveries.remove(delivery)
                self.successful_deliveries += 1

        self.time_elapsed += 1

        reward = Reward(
            value=reward_value + penalty - 0.2 * self.time_elapsed,
            breakdown={
                "delivery_reward": reward_value,
                "penalty": penalty,
                "time_penalty": -0.2 * self.time_elapsed,
            },
        )

        done = len(self.pending_deliveries) == 0 or self.battery_level <= 0

        return self.state(), reward, done, {}

    def state(self) -> Observation:
        """Return current state."""
        return Observation(
            vehicle_location=self.vehicle_location,
            battery_level=self.battery_level,
            pending_deliveries=self.pending_deliveries,
            blocked_cells=self.blocked_cells,
            time_elapsed=self.time_elapsed,
        )

    def _priority_reward(self, priority: str) -> float:
        """Reward based on priority."""
        return {
            "high": 10.0,
            "medium": 5.0,
            "low": 2.0,
        }.get(priority, 1.0)