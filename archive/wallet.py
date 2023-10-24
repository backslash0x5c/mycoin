import base58
import filelock
import json

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
amount = 0
for key in key_list:
    key_hex = base58.b58decode(key['public']).hex()
    if key_hex not in old_in:
        if key_hex in old_out:
            unspent.append(key)

            # 未支払い鍵の合計額を計算
            for block in block_list:
                for tx in block['tx']:
                    if tx['out'] == key_hex:
                        amount += tx['amount']
        else:
            unused.append(key)

# 残高、未支払い鍵の個数と一覧を表示
print(amount, 'coins in unspent keys')
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
