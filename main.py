from fastapi import FastAPI
import logging

from models import Action
from env import DisasterEnv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Disaster Relief Logistics AI")

env = DisasterEnv()

from fastapi.responses import HTMLResponse

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/reset")
def reset():
    """Reset environment"""
    return env.reset()


@app.post("/step")
def step(action: Action):
    """Execute one step"""
    obs, reward, done, info = env.step(action)

    return {
        "observation": obs.model_dump(),
        "reward": reward.model_dump(),
        "done": done,
        "info": info,
    }


@app.get("/state")
def state():
    """Get current state"""
    return env.state()
def main():
    return app