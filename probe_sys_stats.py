#!/usr/bin/env python3
# This collect the system metrics
import json
import socket
import time

import psutil

SRC_HOST = "SCADA"
SERVER = ("localhost", 3001)
SAMPLE_RATE = 1

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def main():
    previous_net = psutil.net_io_counters()

    while True:
        start_time = time.time()

        cpu_time = psutil.cpu_times_percent()
        memory = psutil.virtual_memory()
        current_net = psutil.net_io_counters()
        net_byte_rx = (current_net.bytes_recv - previous_net.bytes_recv) / SAMPLE_RATE
        net_byte_tx = (current_net.bytes_sent - previous_net.bytes_sent) / SAMPLE_RATE
        net_pkt_rx = (current_net.packets_recv - previous_net.packets_recv) / SAMPLE_RATE
        net_pkt_tx = (current_net.packets_sent - previous_net.packets_sent) / SAMPLE_RATE
        previous_net = current_net
        connections = psutil.net_connections()
        tcp_num = 0
        udp_num = 0
        tcp_listen_num = 0
        tcp_established_num = 0
        for conn in connections:
            if conn.type == socket.SOCK_STREAM:
                tcp_num += 1
                if conn.status == psutil.CONN_LISTEN:
                    tcp_listen_num += 1
                elif conn.status == psutil.CONN_ESTABLISHED:
                    tcp_established_num += 1
            elif conn.type == socket.SOCK_DGRAM:
                udp_num += 1

        sock.sendto(bytes(json.dumps({
            "src": SRC_HOST,
            "timestamp": round(time.time(), 3),
            "cpu_percent": psutil.cpu_percent(),
            "cpu_time": {
                "user": cpu_time.user,
                "sys": cpu_time.system,
                "idle": cpu_time.idle,
                "nice": cpu_time.nice,
                "iowait": cpu_time.iowait,
                "irq": cpu_time.irq,
                "softirq": cpu_time.softirq
            },
            "memory_percent": round((memory.total - memory.available) / memory.total * 100, 3),
            "net_byte": {"tx": net_byte_tx, "rx": net_byte_rx},
            "net_pkt": {"tx": net_pkt_tx, "rx": net_pkt_rx},
            "conn_count": {"tcp": tcp_num, "udp": udp_num},
            "tcp_state": {"listen": tcp_listen_num, "established": tcp_established_num}
        }), 'utf-8'), SERVER)
        time.sleep(SAMPLE_RATE - (time.time() - start_time))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("exit")
        pass
