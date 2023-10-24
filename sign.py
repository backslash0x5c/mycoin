import base58
import ecdsa
import filelock
import hashlib
import json
import sys

# コマンドライン引数の処理
if len(sys.argv) != 5:
    print('usage:', sys.argv[0], 'in-private in-public out-public amount')
    exit()

# 鍵（入力の秘密鍵、入力の公開鍵、出力の公開鍵）をBase58形式からバイト列に変換
tx_key = base58.b58decode(sys.argv[1])
tx_in  = base58.b58decode(sys.argv[2])
tx_out = base58.b58decode(sys.argv[3])
# 送金額を整数に変換
amount = int(sys.argv[4])

# トランザクションハッシュの作成
sha = hashlib.sha256()  # SHA-256のオブジェクトを作成
sha.update(tx_in)       # tx_inを使ってハッシュを更新
sha.update(tx_out)      # tx_outを使ってハッシュを更新
hash = sha.digest()     # 結果のハッシュを求めてhashに代入

# トランザクションハッシュに対して署名を実行
key = ecdsa.SigningKey.from_string(tx_key, curve=ecdsa.SECP256k1)
sig = key.sign(hash)

# トランザクションをtrans.txtに出力
with filelock.FileLock('trans.lock', timeout=10):
    try:
        with open('trans.txt', 'r') as file:
            tx_list = json.load(file)
    except:
        tx_list = []

    tx_list.append({
        'in': tx_in.hex(),
        'out': tx_out.hex(),
        'sig': sig.hex(),
        'amount': amount
    })

    with open('trans.txt', 'w') as file:
        json.dump(tx_list, file, indent=2)
