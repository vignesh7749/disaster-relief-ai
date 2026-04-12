from env import DisasterEnv
from models import Action


class Grader:
    """
    Evaluates environment performance across tasks.
    """

    def grade_basic_delivery(self) -> float:
        env = DisasterEnv()
        env.reset()
        return self._run(env)

    def grade_multi_stop_route(self) -> float:
        env = DisasterEnv()
        env.reset()
        return self._run(env)

    def grade_emergency_rerouting(self) -> float:
        env = DisasterEnv()
        env.reset()

        # simulate obstacle
        env.blocked_cells.append((5, 5))

        return self._run(env)

    def _run(self, env: DisasterEnv) -> float:
        steps = 0

        while steps < 50:
            if not env.pending_deliveries:
                break

            target = env.pending_deliveries[0].location
            env.step(Action(move=target, charge=False))
            steps += 1

        return self._score(env)

    def _score(self, env: DisasterEnv) -> float:
        total = env.successful_deliveries + len(env.pending_deliveries)

        if total == 0:
            score = 0.5
        else:
            score = env.successful_deliveries / total

        # 🔥 STRICT FIX — NEVER allow 0 or 1
        if score <= 0.0:
            score = 0.01
        elif score >= 1.0:
            score = 0.99

        return float(score)
