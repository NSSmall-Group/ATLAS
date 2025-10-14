# CLIENT_RECEIVE.py

import socket
import os
import time
def receive_files_from_server(server_ip='127.0.0.1', port=12344, save_dir='received_from_server'):
    os.makedirs(save_dir, exist_ok=True)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print(f"[客户端] 已连接到发送方：{server_ip}:{port}")
    time1 = time.time()
    while True:
        # 1. 接收文件名
        filename = client_socket.recv(1024).decode()
        if filename == 'DONE':
            print("[客户端] 所有文件接收完毕")
            break

        print(f"[客户端] 正在接收文件：{filename}")
        client_socket.sendall(b'OK')  # 确认收到文件名

        # 2. 接收文件大小
        filesize = int(client_socket.recv(1024).decode())
        client_socket.sendall(b'OK')  # 确认收到大小

        # 3. 接收文件内容
        filepath = os.path.join(save_dir, filename)
        received = 0
        with open(filepath, 'wb') as f:
            while received < filesize:
                chunk = client_socket.recv(min(4096, filesize - received))
                if not chunk:
                    break
                f.write(chunk)
                received += len(chunk)

        print(f"[客户端] 文件 {filename} 接收完成（{filesize} 字节）")
        client_socket.sendall(b'FILE RECEIVED')

    client_socket.close()
    print(time.time()-time1)
if __name__ == '__main__':
    receive_files_from_server()
