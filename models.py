from pydantic import BaseModel, Field
from typing import List, Tuple, Optional


class Delivery(BaseModel):
    """Represents a delivery request."""
    location: Tuple[int, int]
    priority: str  # "high", "medium", "low"


class Observation(BaseModel):
    """Environment state returned to agent."""
    vehicle_location: Tuple[int, int]
    battery_level: float
    pending_deliveries: List[Delivery]
    blocked_cells: List[Tuple[int, int]]
    time_elapsed: float


class Action(BaseModel):
    """Agent action."""
    move: Optional[Tuple[int, int]] = None
    charge: bool = False


class Reward(BaseModel):
    """Reward structure."""
    value: float
    breakdown: dict