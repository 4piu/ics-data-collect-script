#!/usr/bin/env python3
# This collect the user behavior data
import json
import socket
import time
from pynput import keyboard, mouse

SERVER = ("localhost", 3001)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_key_press(key: keyboard.Key):
    key_name = ((key.char if hasattr(key, "char") else key.name) or 'other').upper()
    sock.sendto(bytes(json.dumps({
        "src": "KBD",
        "timestamp": round(time.time(), 3),
        "key": key_name,
        "is_pressed": True
    }), 'utf-8'), SERVER)


def send_key_release(key: keyboard.Key):
    key_name = ((key.char if hasattr(key, "char") else key.name) or 'other').upper()
    sock.sendto(bytes(json.dumps({
        "src": "KBD",
        "timestamp": round(time.time(), 3),
        "key": key_name,
        "is_pressed": False
    }), 'utf-8'), SERVER)


def send_move(x: int, y: int):
    sock.sendto(bytes(json.dumps({
        "src": "M_MOVE",
        "timestamp": round(time.time(), 3),
        "coordination": {"x": x, "y": y}
    }), 'utf-8'), SERVER)


def send_click(x: int, y: int, button: mouse.Button, is_clicked: bool):
    sock.sendto(bytes(json.dumps({
        "src": "M_CLK",
        "timestamp": round(time.time(), 3),
        "coordination": {"x": x, "y": y},
        "button": button.name,
        "is_clicked": is_clicked
    }), 'utf-8'), SERVER)


def send_scroll(x: int, y: int, dx: int, dy: int):
    sock.sendto(bytes(json.dumps({
        "src": "M_SCR",
        "timestamp": round(time.time(), 3),
        "coordination": {"x": x, "y": y},
        "displacement": {"dx": dx, "dy": dy}
    }), 'utf-8'), SERVER)


def main():
    with keyboard.Listener(on_press=send_key_press, on_release=send_key_release), \
            mouse.Listener(on_move=send_move, on_scroll=send_scroll, on_click=send_click) as listener:
        listener.join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("exit")
        pass
