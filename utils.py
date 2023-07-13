import socket


def get_ipv4_address():
    """
    Function return local ip address
    :return: local ip address
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        local_ip_address = sock.getsockname()[0]
    finally:
        sock.close()
    return local_ip_address
