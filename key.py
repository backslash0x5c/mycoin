import base58
import ecdsa
import filelock
import json

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
