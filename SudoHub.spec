# -*- mode: python ; coding: utf-8 -*-
#
# SudoHub.spec — PyInstaller конфиг для сборки проекта.
#
# ВАЖНО: модель (Models/ai-forever/rugpt3small_based_on_gpt2) НЕ включается
# в .exe — она слишком большая (~500 МБ). При первом запуске приложение
# скачает её само (если есть интернет) и сохранит рядом с .exe в папку Models/.
#
# Запуск сборки:
#   pip install pyinstaller
#   pyinstaller SudoHub.spec

import sys
from pathlib import Path
import site

# ── Авто-поиск пакетов в текущем окружении ─────────────────────────────────
def pkg_path(name):
    """Возвращает путь к установленному пакету."""
    for sp in site.getsitepackages():
        p = Path(sp) / name
        if p.exists():
            return str(p)
    # fallback: importlib
    import importlib.util
    spec = importlib.util.find_spec(name)
    if spec and spec.submodule_search_locations:
        return str(list(spec.submodule_search_locations)[0])
    raise FileNotFoundError(f"Пакет не найден: {name}")


block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[
        # Скомпилированная C-библиотека (раскомментируйте если используете alg_wrapper)
        ('Clib/Windows/alg_wrapper.cp311-win_amd64.pyd', '.'),
    ],
    datas=[
        # Статические ресурсы проекта
        ('Assets',              'Assets'),
        ('Data',                'Data'),

        # Данные пакетов (без них PyInstaller их не найдёт)
        (pkg_path('customtkinter'),  'customtkinter'),
        (pkg_path('tkinterdnd2'),    'tkinterdnd2'),
    ],
    hiddenimports=[
        # GUI
        'customtkinter',
        'tkinterdnd2',
        'PIL._tkinter_finder',

        # Нейросеть
        'transformers',
        'transformers.models.gpt2',
        'transformers.models.gpt2.modeling_gpt2',
        'transformers.models.gpt2.tokenization_gpt2',
        'transformers.models.gpt2.tokenization_gpt2_fast',
        'torch',
        'torch.nn',
        'torch.nn.functional',

        # Сеть / Wikipedia
        'requests',
        'urllib3',
        'wikipedia',
        'charset_normalizer',

        # PDF / DOCX
        'fitz',
        'docx',

        # Стандартная библиотека (иногда нужно явно)
        'asyncio',
        'threading',
        'math',
        'pathlib',
        'socket',
        'pymorphy3'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Не нужны в проекте — уменьшают размер
        'matplotlib',
        'numpy.testing',
        'IPython',
        'jupyter',
        'notebook',
        'pytest',
        'setuptools',
        'distutils',
        'tkinter.test',
         #'unittest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,    # Добавлено сюда
    a.zipfiles,    # Добавлено сюда
    a.datas,       # Добавлено сюда
    exclude_binaries=False,      # onedir: бинарники рядом, не внутри exe
    name='SudoHub',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                   # сжатие (нужен UPX: https://upx.github.io/)
    console=False,              # False = без чёрного окна консоли
    icon='Assets/Images/SudoHub.ico',
)
