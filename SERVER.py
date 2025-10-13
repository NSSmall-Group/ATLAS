# SERVER_SEND.py

import socket
import os

def send_files_to_client(host='0.0.0.0', port=12344):
    files_to_send = ['x_test.pkl','z_test.pkl','user_artifact.txt' ]
    # files_to_send = ['visseq_graph_testing_preprocessed_logs_S2-CVE-2015-3105_windows.dot.txt.html']
    file_dir = r'C:/Users/GAOXIANG/Desktop/ATLAS-S2/output'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[服务端] 等待接收方连接: {host}:{port}...")

    conn, addr = server_socket.accept()
    print(f"[服务端] 接收方已连接：{addr}")

    for filename in files_to_send:
        filepath = os.path.join(file_dir, filename)
        if not os.path.isfile(filepath):
            print(f"[服务端] 文件不存在，跳过：{filename}")
            continue

        # 1. 发送文件名
        conn.sendall(filename.encode())
        ack = conn.recv(1024).decode()
        if ack != 'OK':
            print(f"[服务端] {filename}：接收方未确认")
            continue

        # 2. 发送文件大小
        filesize = os.path.getsize(filepath)
        conn.sendall(str(filesize).encode())
        ack = conn.recv(1024).decode()
        if ack != 'OK':
            print(f"[服务端] {filename}：文件大小确认失败")
            continue

        # 3. 发送文件内容
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                conn.sendall(chunk)

        # 4. 等待确认
        ack = conn.recv(1024).decode()
        if ack == 'FILE RECEIVED':
            print(f"[服务端] {filename} 发送成功")
        else:
            print(f"[服务端] {filename} 发送失败")

    # 5. 通知传输完毕
    conn.sendall(b'DONE')
    conn.close()
    server_socket.close()
    print("[服务端] 所有文件发送完成")

if __name__ == '__main__':
    send_files_to_client()
