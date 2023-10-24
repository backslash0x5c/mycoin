import ecdsa
import filelock
import hashlib
import json

# トランザクションファイル（trans.txt）の読み込み
with filelock.FileLock('trans.lock', timeout=10):
    with open('trans.txt', 'r') as file:
        tx_list = json.load(file)

# 全トランザクションについて処理
for tx in tx_list:
    # 鍵と署名を16進数で表示
    print('in  hex:', tx['in'])
    print('out hex:', tx['out'])
    print('sig hex:', tx['sig'])

    # 鍵と署名をバイト列に変換
    tx_in = bytes.fromhex(tx['in'])
    tx_out = bytes.fromhex(tx['out'])
    tx_sig = bytes.fromhex(tx['sig'])

    # トランザクションハッシュの作成
    sha = hashlib.sha256()
    sha.update(tx_in)
    sha.update(tx_out)
    hash=sha.digest()

    # トランザクションハッシュの長さと内容を表示
    print('hash len:', len(hash))
    print('hash hex:', hash.hex())

    # トランザクションハッシュに対して署名の検証を実行
    key = ecdsa.VerifyingKey.from_string(tx_in, curve=ecdsa.SECP256k1)
    print('verify:', key.verify(tx_sig, hash))

    print()
