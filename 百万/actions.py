# Go2 高层动作封装（放在中文目录“百万”中，模拟模式默认开启）
"""
文件: 百万/actions.py
说明: 提供一个简单的 Go2 动作封装类，用于演示/本地测试（默认模拟，不发送真实命令）。
"""
import time
from typing import List, Dict


def _get_sport_client():
    try:
        from unitree_sdk2py.go2.sport.sport_client import SportClient
    except Exception as e:
        raise RuntimeError("无法导入 SportClient: %s" % e)
    c = SportClient(enableLease=False)
    c.Init()
    return c


class Go2Actions:
    def __init__(self, simulate: bool = True):
        """
        simulate: True 时仅打印日志，不向机器人发送命令。用于本地测试。
        """
        self.simulate = simulate
        self._client = None
        if not simulate:
            self._client = _get_sport_client()

        # 参数限幅
        self.max_speed = 1.0  # m/s (示例)
        self.max_vyaw = 2.0   # rad/s
        self.max_duration = 60.0  # s

    def _clip(self, v, lo, hi):
        return max(lo, min(hi, v))

    def stand(self):
        if self.simulate:
            print("[SIM] stand() -> StandUp")
            return 0
        return self._client.StandUp()

    def sit(self):
        if self.simulate:
            print("[SIM] sit() -> Sit")
            return 0
        return self._client.Sit()

    def stop(self):
        if self.simulate:
            print("[SIM] stop() -> StopMove")
            return 0
        return self._client.StopMove()

    def move(self, vx: float = 0.0, vy: float = 0.0, vyaw: float = 0.0, duration: float = 0.0):
        vx = self._clip(vx, -self.max_speed, self.max_speed)
        vy = self._clip(vy, -self.max_speed, self.max_speed)
        vyaw = self._clip(vyaw, -self.max_vyaw, self.max_vyaw)
        duration = max(0.0, min(self.max_duration, duration))
        if self.simulate:
            print(f"[SIM] move vx={vx} vy={vy} vyaw={vyaw} duration={duration}")
            if duration > 0:
                time.sleep(min(duration, 1.0))  # short sleep for demo
            return 0
        # Move uses no-reply call; to maintain command for duration, send repeatedly or use loop
        end = time.time() + duration
        if duration <= 0:
            return self._client.Move(vx, vy, vyaw)
        while time.time() < end:
            self._client.Move(vx, vy, vyaw)
            time.sleep(0.05)  # 20Hz
        # stop after movement
        self._client.Move(0.0, 0.0, 0.0)
        return 0

    def trot(self, duration: float = 1.0):
        duration = max(0.0, min(self.max_duration, duration))
        if self.simulate:
            print(f"[SIM] trot duration={duration} -> TrotRun (start), sleep, StopMove")
            time.sleep(min(duration, 1.0))
            return 0
        # 如果 SDK 提供持续 trot 接口，这里调用 TrotRun() 然后等待，再 StopMove()
        self._client.TrotRun()
        time.sleep(duration)
        self._client.StopMove()
        return 0

    def turn(self, vyaw: float = 0.5, duration: float = 1.0):
        vyaw = self._clip(vyaw, -self.max_vyaw, self.max_vyaw)
        return self.move(0.0, 0.0, vyaw, duration)

    def custom_sequence(self, seq: List[Dict]):
        """
        seq: 列表，每项为 {'action': 'stand'|'sit'|'move'|'trot'|'turn'|'stop', 'params': {...}}
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
