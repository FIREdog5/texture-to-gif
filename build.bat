mv --backup=numbered dist/texture-to-gif.exe old_dists/texture-to-gif.exe
pyinstaller --onefile --noconsole main.py
mv dist/main.exe dist/texture-to-gif.exe
