import base58
import ecdsa
import filelock
import hashlib
import json
import os
import subprocess
import sys
import socket
import urllib.request
import time

# デバッグ用表示フラグ
debug = True

# 鍵ペアの一覧をkey.txtから入力
with filelock.FileLock('key.lock', timeout=10):
    try:
        with open('key.txt', 'r') as file:
            key_list = json.load(file)
    except:
        key_list = []

# ブロックチェーンをblock.txtから入力
with filelock.FileLock('block.lock', timeout=10):
    try:
        with open('block.txt', 'r') as file:
            block_list = json.load(file)
    except:
        block_list = []

# 既存のトランザクション入出力リストを作成
old_in = []
old_out = []
for block in block_list:
    for tx in block['tx']:
        old_in.append(tx['in'])
        old_out.append(tx['out'])

# 未支払い鍵と未使用鍵のリストを作成
unspent = []
unused = []
keyamount_list = []
balance = 0

for key in key_list:
    key_hex = base58.b58decode(key['public']).hex()
    if key_hex not in old_in:
        if key_hex in old_out:
            unspent.append(key)

            # 鍵ペアと金額の対応リスト作成、未支払い鍵の合計額を計算
            for block in block_list:
                for tx in block['tx']:
                    if tx['out'] == key_hex:
                        keyamount_list.append({
                            'private': key['private'],
                            'public': key['public'],
                            'amount' : tx['amount']
                        })
                        balance += tx['amount']
        else:
            unused.append(key)

# 残高、未支払い鍵の個数と一覧を表示
print(balance, 'coins in unspent keys')
print()

print(len(unspent), 'unspent keys:')
for key in unspent:
    print('private:', key['private'])
    print('public :', key['public'])
print()

# 未使用鍵の個数と一覧を表示
print(len(unused), 'unused keys:')
for key in unused:
    print('private:', key['private'])
    print('public :', key['public'])
print()

# 未支払い鍵がない場合は送金不可
if(balance <= 0):
    print("There is no coin.")
    sys.exit()

# # 送金先（サーバーのホストとポート番号）と金額を入力
# server_host = input("Enter IP Address or \"exit\": ")
# # exitが入力された場合は送金せず終了
# if server_host == "exit":
#     sys.exit()

# server_port = int(input("Enter Port : "))

while True:
    input_str = input("Enter the amount to send OR \"exit\": ")
    if input_str == "exit":
        sys.exit()
    # 送金額が0より大きく、残高以下の場合は送金可能
    elif int(input_str) > 0 and int(input_str) <= balance:
        send_amount = int(input_str)
        break
    # 送金額が不正な場合は送金不可
    else:
        print("You don't have enough coin.")

total = 0
selected = []
dir = os.path.dirname(os.path.abspath(__file__))

# # リクエストデータ
# request_data = "request_public_key"
# # ソケットの作成
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # サーバーに接続
# client_socket.connect((server_host, server_port))

# send_amount以上になるまで未支払い鍵を選択
for key in keyamount_list:
    total += key['amount']
    
    # # リクエスト送信 -> 相手に公開鍵を生成してもらう
    # client_socket.send(request_data.encode('utf-8'))
    # if debug:
    #     print("Request sent.")
    
    # time.sleep(1)
    # url = 'http://' + server_host + ':' + str(server_port) + '/unused_public_key.txt'
    # if debug:
    #     print('URL is : ' + url)

    # try:
    #     with urllib.request.urlopen(url) as file:
    #         unused_public_key_list = json.load(file)
    #         if debug:
    #             print("Access succeeded!")
    #             print("public_key : " + unused_public_key_list[-1]['public'])
    #         unused_public_key = unused_public_key_list[-1]['public']
    # except:
    #     unused_public_key_list = []
    #     if debug:
    #         print("Access failed!")
    #     unused_public_key = input("Enter unused public key : ")
    unused_public_key = input("Enter unused public key : ")
    
    if total <= send_amount:
        # 受け取りアドレスにあたる公開鍵 unused_public_key は随時変わる
        subprocess.run(['python', os.path.join(dir, 'sign.py'), key['private'], key['public'], unused_public_key, str(key['amount'])])

        if total == send_amount:
            break
        
    elif total > send_amount:
        # key['amount']のうち、未支払い分は相手に、残り（おつり）は新たな鍵を生成して自分に送る
        subprocess.run(['python', os.path.join(dir, 'sign.py'), key['private'], key['public'], unused_public_key, str(key['amount'] - (total - send_amount))])

        # 秘密鍵と公開鍵の生成
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        public_key = private_key.get_verifying_key()

        # 秘密鍵と公開鍵を文字列に変換
        private_key = private_key.to_string()
        public_key = public_key.to_string()

        # 秘密鍵と公開鍵をBase58形式に変換
        private_b58 = base58.b58encode(private_key).decode('ascii')
        public_b58 = base58.b58encode(public_key).decode('ascii')

        # 秘密鍵と公開鍵をkey.txtに出力
        with filelock.FileLock('key.lock', timeout=10):
            try:
                with open('key.txt', 'r') as file:
                    key_list = json.load(file)
            except:
                key_list = []

            key_list.append({
                'private': private_b58,
                'public' : public_b58
            })

            with open('key.txt', 'w') as file:
                json.dump(key_list, file, indent=2)

        subprocess.run(['python', os.path.join(dir, 'sign.py'), key['private'], key['public'], public_b58, str(total - send_amount)])
        break