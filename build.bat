@echo off
echo ============================================
echo   SudoHub Build Script
echo ============================================

python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found.
    pause & exit /b 1
)

echo.
echo [1/3] Installing dependencies...
pip install pyinstaller customtkinter tkinterdnd2 Pillow PyMuPDF python-docx transformers requests wikipedia cython setuptools
if errorlevel 1 (
    echo ERROR: pip install failed.
    pause & exit /b 1
)

pip install torch --index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 (
    echo ERROR: torch install failed.
    pause & exit /b 1
)

echo.
echo [2/3] Compiling alg_wrapper...
cd Clib\ToolsForCompile
python setup_windows.py build_ext --inplace
if errorlevel 1 (
    echo WARNING: alg_wrapper build failed, skipping.
) else (
    echo OK: alg_wrapper compiled.
    for %%f in (alg_wrapper*.pyd) do (
        copy "%%f" "..\Windows\%%f" > nul
    )
)
cd ..\..

echo.
echo [3/3] Building exe with PyInstaller...
pyinstaller SudoHub.spec --clean --noconfirm
if errorlevel 1 (
    echo ERROR: PyInstaller failed.
    pause & exit /b 1
)

echo.
echo ============================================
echo   DONE: dist\SudoHub\SudoHub.exe
echo   NOTE: AI model (~500 MB) downloads on
echo   first launch into Models\ folder.
echo ============================================
pause
