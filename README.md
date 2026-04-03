---
title: Disaster Relief AI
emoji: 🚨
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---
# 🚨 Disaster Relief Logistics AI

## 🎥 Demo

👉 Run locally:
http://127.0.0.1:8000/

Watch the AI simulate disaster logistics in real time with:

* Intelligent routing
* Obstacle avoidance
* Priority-based delivery

## 🧠 Overview

Disaster Relief Logistics AI is an intelligent simulation environment designed to optimize the delivery of critical supplies during emergency scenarios.

The system uses AI-driven decision-making to prioritize high-importance deliveries, avoid blocked routes, and manage limited resources like battery power.

---

## 🚀 Key Features

* 🧠 A* Pathfinding for optimal route planning
* 🚧 Dynamic obstacle avoidance (blocked roads)
* 📦 Priority-based delivery system (high, medium, low)
* 🔋 Battery-aware decision making
* 🎮 Real-time interactive dashboard visualization
* ⚡ FastAPI-based OpenEnv compliant backend

---

## 🧩 Tech Stack

* Python
* FastAPI
* Pydantic
* HTML + JavaScript (Visualization UI)

---

## 📂 Project Structure

```
DisasterReliefAI/
│
├── main.py
├── env.py
├── models.py
├── grader.py
├── inference.py
├── openenv.yaml
├── Dockerfile
├── index.html
└── requirements.txt
```

---

## ⚙️ How to Run

### 1. Setup

```
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

### 2. Start Server

```
uvicorn main:app --reload
```

### 3. Open Dashboard

```
http://127.0.0.1:8000/
```

---

## 🎮 Demo Flow

1. Open dashboard
2. Click **Start Simulation 🚀**
3. Observe:

   * Intelligent routing
   * Priority-based deliveries
   * Obstacle avoidance
   * Real-time visualization

---

## 🧠 AI Approach

The system uses:

* A* algorithm for optimal pathfinding
* Heuristic-based decision making
* Priority-aware scheduling
* Constraint handling (battery + obstacles)

---

## 🏆 Use Case

This system can be applied to:

* Disaster response logistics
* Emergency medical supply delivery
* Smart transportation systems


## 🌟 Highlights

* Real-world disaster use-case
* Advanced A* pathfinding
* Interactive visualization
* Fully OpenEnv compliant
* Clean, production-grade code

---

## 🔮 Future Scope

* Multi-vehicle coordination
* Real-time map integration (GPS / APIs)
* Machine learning-based demand prediction
---

## 👤 Author

Vignesh
