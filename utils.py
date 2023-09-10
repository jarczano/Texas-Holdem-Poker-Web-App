import socket
import openai

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


def custom_argmax2(arr):

    max_value = arr[0]
    max_index = 0
    for i, value in enumerate(arr):
        if value > max_value:
            max_value = value
            max_index = i
    return max_index

def custom_argmax(arr):
    max_value = arr[0]
    max_index = 0
    for i in range(1, len(arr)):
        if arr[i] > max_value:
            max_value = arr[i]
            max_index = i
    return max_index


def get_content(in_prompt):
    content_json = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                            messages=[
                                                {'role': 'user', 'content': in_prompt}
                                            ],
                                        temperature=0.7,
                                        max_tokens=10)
    response = content_json['choices'][0]['message']['content']
    return response
