from pydantic import BaseModel
from datetime import datetime

from enum import Enum


class SimulationStatus(str, Enum):
    pending = "pending"
    running = "running"
    finished = "finished"


class ConvergenceData(BaseModel):
    seconds: int
    loss: float


class Machine(BaseModel):
    machine_id: int
    name: str


class Simulation(BaseModel):
    simulation_id: int
    name: str
    machine_id: int
    status: SimulationStatus
    creation_date: datetime
    update_date: datetime
    machine: Machine
