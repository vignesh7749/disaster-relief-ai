from env import DisasterEnv
from models import Action


class Grader:
    """
    Evaluates environment performance across tasks.
    """

    def basic_delivery(self) -> float:
        env = DisasterEnv()
        env.reset()

        steps = 0

        while steps < 50:
            if not env.pending_deliveries:
                break

            target = env.pending_deliveries[0].location
            env.step(Action(move=target, charge=False))
            steps += 1

        return self._score(env)

    def multi_stop_route(self) -> float:
        env = DisasterEnv()
        env.reset()

        env.pending_deliveries = [
            d for d in env.pending_deliveries
        ]

        return self._run(env)

    def emergency_rerouting(self) -> float:
        env = DisasterEnv()
        env.reset()

        # simulate new blocked path mid-run
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
            return 1.0

        return env.successful_deliveries / total