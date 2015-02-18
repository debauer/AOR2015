cd ..\firmware\remote_unit
ino.py build -m mega2560
ino.py upload -m mega2560 -p COM7
cd ..\..\scripts
