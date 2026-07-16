#!/usr/bin/env python3
"""CLI for Go2 actions (unitree_sdk2py.cli)

Usage examples:
  python -m unitree_sdk2py.cli stand
  python -m unitree_sdk2py.cli move --vx 0.2 --duration 2.0
  python -m unitree_sdk2py.cli --no-sim trot --duration 3.0
"""
import argparse
import json
import sys
from .actions import Go2Actions


def main(argv=None):
    parser = argparse.ArgumentParser(prog="go2-action")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("stand")
    sub.add_parser("sit")
    sub.add_parser("stop")

    mv = sub.add_parser("move")
    mv.add_argument("--vx", type=float, default=0.0)
    mv.add_argument("--vy", type=float, default=0.0)
    mv.add_argument("--vyaw", type=float, default=0.0)
    mv.add_argument("--duration", type=float, default=0.0)

    tr = sub.add_parser("trot")
    tr.add_argument("--duration", type=float, default=1.0)

    turn = sub.add_parser("turn")
    turn.add_argument("--vyaw", type=float, default=0.5)
    turn.add_argument("--duration", type=float, default=1.0)

    seq = sub.add_parser("seq")
    seq.add_argument("json_file", help="JSON file with action sequence")

    parser.add_argument("--no-sim", action="store_true", help="Disable simulation (send commands to robot)")

    args = parser.parse_args(argv)
    actions = Go2Actions(simulate=not args.no_sim)

    if args.cmd == "stand":
        actions.stand()
    elif args.cmd == "sit":
        actions.sit()
    elif args.cmd == "stop":
        actions.stop()
    elif args.cmd == "move":
        actions.move(args.vx, args.vy, args.vyaw, args.duration)
    elif args.cmd == "trot":
        actions.trot(args.duration)
    elif args.cmd == "turn":
        actions.turn(args.vyaw, args.duration)
    elif args.cmd == "seq":
        try:
            with open(args.json_file, "r", encoding="utf-8") as f:
                seq_data = json.load(f)
        except Exception as e:
            print(f"Failed to load JSON: {e}", file=sys.stderr)
            return 2
        actions.custom_sequence(seq_data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
