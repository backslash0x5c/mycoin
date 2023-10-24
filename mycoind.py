import os
import subprocess
# import socket
# import threading
# from concurrent.futures import ThreadPoolExecutor

def peer():
    subprocess.run(['python', os.path.join(dir, 'peer.py')])

# def handle_client(client_socket, client_address):
#     print("Connected to:", client_address)

#     # データの受信
#     data = client_socket.recv(1024).decode('utf-8')
#     print("Received data:", data)

#     # データの処理
#     if data == "request_public_key":
#         print("Request received.")
#         subprocess.run(['python', os.path.join(dir, 'key.py')])

#     # クライアントソケットのクローズ
#     client_socket.close()

# def client_thread():
#     client_socket, client_address = server_socket.accept()
#     client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
#     client_thread.start()

if __name__ == '__main__':
    # # ホストとポート設定
    # host = '0.0.0.0'  # 任意のホストアドレス
    # port = int(input('port: ')) # 開放しているポート番号

    # # ソケットの作成
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.bind((host, port))
    # server_socket.listen()
    # print("Waiting for connections...")

    dir = os.path.dirname(os.path.abspath(__file__))
    while True:
        peer()
        
        # with ThreadPoolExecutor() as executor:
        #     executor.submit(peer)
        #     executor.submit(client_thread)
        # rBaA8P8HgiuvZRfoghVzaZ8SdwdXYmP2gf11CwRuxz4
