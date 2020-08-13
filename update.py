import hashlib
import dropbox
import os
import subprocess

def getHash(path):
    algo = 'md5'

# ハッシュオブジェクトを作ります
    h = hashlib.new(algo)

    # 分割する長さをブロックサイズの整数倍に決めます
    Length = hashlib.new(algo).block_size * 0x800

    # 大きなバイナリデータを用意します
    with open(path,'rb') as f:
        BinaryData = f.read(Length)

        # データがなくなるまでループします
        while BinaryData:

            # ハッシュオブジェクトに追加して計算します。
            h.update(BinaryData)

            # データの続きを読み込む
            BinaryData = f.read(Length)

    # ハッシュオブジェクトを16進数で出力します
    return(algo,h.hexdigest())

def dbxDownload(path,lpath):
    with open(lpath, "wb") as f:
        metadata, res = dbx.files_download(path=path)
        f.write(res.content)
        
dbx = dropbox.Dropbox("XXj6O7ua0xAAAAAAAAAAheejSlBT5nPZg9jk1rnFy_7okIq8DdTt6AAZlxA1pDwL")
print("更新Check...")
oldHash = getHash("main.exe")
dbxDownload("/challocord/main.exe","tempmain.exe")
newHash = getHash("tempmain.exe")
if list(oldHash)[1] != list(newHash)[1]:
    print("更新確認")
    os.remove("main.exe")
    print("rename中...")
    os.rename("tempmain.exe","main.exe")
    print("rename完了")
    print("リリースノート表示...")
    dbxDownload("/challocord/note.txt","ReleaseNote.txt")
    subprocess.run("notepad {}".format('ReleaseNote.txt'))
else:
    os.remove("tempmain.exe")
    print("更新なし")
