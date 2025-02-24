"""
run the main app
"""
from .seer_sessions import Seer_sessions


def run() -> None:
    reply = Seer_sessions().run()
    print(reply)
