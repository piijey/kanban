import qrcode

url = "https://piijey.github.io/kanban/"

img = qrcode.make(url)
img.save("qrcode_url.png")

print(f"QRコードを保存しました！ {url}")
