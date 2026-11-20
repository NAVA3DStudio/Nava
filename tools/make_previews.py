"""Создаёт облегчённые версии картинок портфолио.

Запуск из корня репозитория:  python tools/make_previews.py
Делает только недостающие файлы (существующие не трогает; --force пересоздаёт всё).

  thumbs/sm/<имя>.jpg  — 800px,  для плиток в сетке
  thumbs/<имя>.jpg     — 1280px, для плиток на больших экранах
  view/<имя>.jpg       — 2560px, для просмотра (увеличенная картинка)

Оригиналы остаются как есть и сайтом больше не загружаются.
"""
import os
import sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGETS = [("thumbs/sm", 800, 78), ("thumbs", 1280, 80), ("view", 2560, 82)]
force = "--force" in sys.argv

os.chdir(ROOT)
sources = sorted(f for f in os.listdir(".") if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")))
for folder, _, _ in TARGETS:
    os.makedirs(folder, exist_ok=True)

made = 0
for name in sources:
    todo = [(d, w, q) for d, w, q in TARGETS if force or not os.path.exists(f"{d}/{name}.jpg")]
    if not todo:
        continue
    with Image.open(name) as im:
        im.seek(0)
        im = im.convert("RGB")
        for folder, width, quality in todo:
            out = im
            if im.width > width:
                out = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            out.save(f"{folder}/{name}.jpg", "JPEG", quality=quality, optimize=True, progressive=True)
            made += 1
    print("ok", name)

print(f"готово: {made} файлов")
