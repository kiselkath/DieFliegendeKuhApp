"""Встраивает картинки из verb-images/ в DieFliegendeKuhApp.html (base64, WebP).

Запуск из корня репозитория:  python tools/embed-verb-images.py

Берёт все файлы verb-images/NNN-*.webp, где NNN — номер глагола, и записывает их
в объект VERB_IMAGES между маркерами VERB_IMAGES:BEGIN / VERB_IMAGES:END.
Повторный запуск полностью перезаписывает этот блок, так что после добавления
новых картинок достаточно запустить скрипт ещё раз.
Сама папка verb-images/ в репозиторий не попадает (см. .gitignore).
"""
import base64, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "DieFliegendeKuhApp.html")
IMG_DIR = os.path.join(ROOT, "verb-images")
BEGIN, END = "/* VERB_IMAGES:BEGIN */", "/* VERB_IMAGES:END */"

def main():
    html = open(APP, encoding="utf-8").read()
    if html.count(BEGIN) != 1 or html.count(END) != 1:
        sys.exit("Маркеры VERB_IMAGES не найдены в " + APP)
    entries = {}
    for name in sorted(os.listdir(IMG_DIR)):
        m = re.match(r"^(\d{3})-.+\.webp$", name)
        if not m:
            continue
        num = int(m.group(1))
        if num in entries:
            sys.exit(f"Два файла для глагола №{num}: {name}")
        data = base64.b64encode(open(os.path.join(IMG_DIR, name), "rb").read()).decode("ascii")
        entries[num] = f'{num}:"data:image/webp;base64,{data}"'
    block = BEGIN + "\nconst VERB_IMAGES = {\n" + ",\n".join(entries[k] for k in sorted(entries)) + "\n};\n" + END
    a = html.index(BEGIN); b = html.index(END) + len(END)
    html = html[:a] + block + html[b:]
    open(APP, "w", encoding="utf-8", newline="").write(html)
    print(f"Встроено картинок: {len(entries)} (№ {', '.join(map(str, sorted(entries)))})")

if __name__ == "__main__":
    main()
