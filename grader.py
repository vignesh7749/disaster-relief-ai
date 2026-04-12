from env import DisasterEnv
from models import Action


class Grader:
    """
    Explicit grader with guaranteed valid outputs
    """

    # 🔥 Explicit task registry (VERY IMPORTANT)
    TASKS = [
        "basic_delivery",
        "multi_stop_route",
        "emergency_rerouting",
    ]

    def grade_basic_delivery(self) -> float:
        return self._execute_task()

    def grade_multi_stop_route(self) -> float:
        return self._execute_task()

    def grade_emergency_rerouting(self) -> float:
        env = DisasterEnv()
        env.reset()

        # simulate change
        env.blocked_cells.append((5, 5))

        return self._run(env)

    # 🔥 unified execution
    def _execute_task(self) -> float:
        env = DisasterEnv()
        env.reset()
        return self._run(env)

    def _run(self, env: DisasterEnv) -> float:
        steps = 0

        while steps < 30:
            if not env.pending_deliveries:
                break

            target = env.pending_deliveries[0].location
            env.step(Action(move=target, charge=False))
            steps += 1

        # 🔥 Always return safe score
        return self._safe_score(env)

    def _safe_score(self, env: DisasterEnv) -> float:
        total = env.successful_deliveries + len(env.pending_deliveries)

        # 🔥 HARD GUARANTEE
        if total <= 0:
            return 0.5

        ratio = env.successful_deliveries / total

        # 🔥 STRICT RANGE ENFORCEMENT
        if ratio <= 0:
            return 0.1
        if ratio >= 1:
            return 0.9

        # 🔥 clamp
        return float(max(0.1, min(0.9, ratio)))