"""High-level Go2 action helpers (importable).

This module mirrors the example placed in 中文目录 百万/actions.py but is a proper Python
module under unitree_sdk2py so it can be imported as

    from unitree_sdk2py.actions import Go2Actions

By default it runs in simulation mode (safe). Set simulate=False to attempt to use the
repository's SportClient to send commands to the robot.
"""

import time
from typing import List, Dict


def _get_sport_client():
    try:
        from .go2.sport.sport_client import SportClient
    except Exception as e:
        raise RuntimeError("unable to import SportClient: %s" % e)
    c = SportClient(enableLease=False)
    c.Init()
    return c


class Go2Actions:
    """High-level action wrapper for Unitree Go2.

    simulate: when True, actions are logged but not sent to robot (safe default).
    """

    def __init__(self, simulate: bool = True):
        self.simulate = simulate
        self._client = None
        if not simulate:
            # may raise if SDK/network not available
            self._client = _get_sport_client()

        # safety limits (tunable)
        self.max_speed = 1.0  # m/s
        self.max_vyaw = 2.0   # rad/s
        self.max_duration = 60.0  # s

    def _clip(self, v, lo, hi):
        return max(lo, min(hi, v))

    def stand(self):
        """Bring robot to stand (StandUp)."""
        if self.simulate:
            print("[SIM] stand() -> StandUp")
            return 0
        return self._client.StandUp()

    def sit(self):
        """Make the robot sit."""
        if self.simulate:
            print("[SIM] sit() -> Sit")
            return 0
        return self._client.Sit()

    def stop(self):
        """Emergency/stop movement."""
        if self.simulate:
            print("[SIM] stop() -> StopMove")
            return 0
        return self._client.StopMove()

    def move(self, vx: float = 0.0, vy: float = 0.0, vyaw: float = 0.0, duration: float = 0.0):
        """Send velocity command. If duration>0, repeat until duration elapses.

        vx, vy in m/s, vyaw in rad/s.
        """
        vx = self._clip(vx, -self.max_speed, self.max_speed)
        vy = self._clip(vy, -self.max_speed, self.max_speed)
        vyaw = self._clip(vyaw, -self.max_vyaw, self.max_vyaw)
        duration = max(0.0, min(self.max_duration, duration))

        if self.simulate:
            print(f"[SIM] move vx={vx} vy={vy} vyaw={vyaw} duration={duration}")
            if duration > 0:
                # small sleep for demo only
                time.sleep(min(duration, 1.0))
            return 0

        # Move uses a no-reply call in the SDK. If duration <=0, send a single command.
        if duration <= 0:
            return self._client.Move(vx, vy, vyaw)

        end = time.time() + duration
        while time.time() < end:
            self._client.Move(vx, vy, vyaw)
            time.sleep(0.05)
        # stop after
        self._client.Move(0.0, 0.0, 0.0)
        return 0

    def trot(self, duration: float = 1.0):
        """Start trot/run gait for duration seconds."""
        duration = max(0.0, min(self.max_duration, duration))
        if self.simulate:
            print(f"[SIM] trot duration={duration} -> TrotRun then StopMove")
            time.sleep(min(duration, 1.0))
            return 0

        # if SDK supports persistent trot, call it and wait
        self._client.TrotRun()
        time.sleep(duration)
        self._client.StopMove()
        return 0

    def turn(self, vyaw: float = 0.5, duration: float = 1.0):
        """Turn in place by issuing a yaw rate for duration seconds."""
        vyaw = self._clip(vyaw, -self.max_vyaw, self.max_vyaw)
        return self.move(0.0, 0.0, vyaw, duration)

    def custom_sequence(self, seq: List[Dict]):
        """Execute a list of actions. Each item: {'action': str, 'params': dict}.

        Supported actions: stand, sit, move, trot, turn, stop
        """
        for step in seq:
            act = step.get("action")
            params = step.get("params", {})
            if act == "stand":
                self.stand()
            elif act == "sit":
                self.sit()
            elif act == "move":
                self.move(**params)
            elif act == "trot":
                self.trot(**params)
            elif act == "turn":
                self.turn(**params)
            elif act == "stop":
                self.stop()
            else:
                print(f"[WARN] Unknown action: {act}")
        return 0
