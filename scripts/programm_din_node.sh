export DISPLAY=:0.0
arduino --board arduino:avr:mega:cpu=atmega2560 --port /dev/ttyACM0 --upload ../firmware/remote_unit/remote_unit.ino