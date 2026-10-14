# -*- coding: utf-8 -*-
"""
从 _imgs/ 的原始 PNG 重新生成网页用 WebP 立绘到 assets/gu/。
（不依赖 docs/，docs 已被清空）
"""
import os
from PIL import Image, ImageDraw, ImageFilter

SRC = "_imgs"
OUT = os.path.join("assets", "gu")
os.makedirs(OUT, exist_ok=True)

def square(im):
    s = max(im.size)
    c = Image.new("RGB", (s, s), (0, 0, 0))
    c.paste(im, ((s - im.size[0]) // 2, (s - im.size[1]) // 2))
    return c

def soft_frame(size, inset=0.055, feather=0.085):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    pad = int(size * inset)
    d.rounded_rectangle([pad, pad, size - 1 - pad, size - 1 - pad],
                        radius=int(size * 0.10), fill=255)
    return m.filter(ImageFilter.GaussianBlur(max(1, int(size * feather))))

ids = sorted(f[:-4] for f in os.listdir(SRC) if f.endswith(".png"))
total = 0
for sid in ids:
    im = square(Image.open(os.path.join(SRC, sid + ".png")).convert("RGB"))
    for size, prefix, q in ((512, "", 88), (160, "sm_", 82)):
        big = im.resize((size, size), Image.LANCZOS).convert("RGBA")
        big.putalpha(soft_frame(size))
        p = os.path.join(OUT, prefix + sid + ".webp")
        big.save(p, "WEBP", quality=q, method=6)
        total += os.path.getsize(p)
print("已生成 %d 个 WebP，合计 %.2f MB" % (len(ids) * 2, total / 1048576))
print("512px: %d 个 | 160px: %d 个"
      % (len([f for f in os.listdir(OUT) if not f.startswith('sm_')]),
         len([f for f in os.listdir(OUT) if f.startswith('sm_')])))
