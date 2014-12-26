AOR2015 - Fahrzeug Sensorik und Musik
=======

Trikots für Kids - Allgäu Orient Rallye 2015

https://www.facebook.com/trikotsfuerkids

http://www.trikots-fuer-kids.de/

## Ziele

  * Fahrzeug Sensoren Zentral überwachen
  * Messwert Archivierung und aufarbeitung
  * Musik komfortabel abspielen
  * Weiter Nutzung der entwicklung in unsern Privaten Fahrzeugen nach der Rallye
  * Geschützt vor Umwelteinflüssen
  
## Beweggründe

  * Spieltrieb
  * for fucking science

## Hardware

### Fahrzeug 1

  * Zentraler Linux Rechner (Raspberry PI) 
    - SSD in USB Case für Musik
    - USB Soundkarte für den guten Klang
    - USB WLan Stick um Access Point zu realisieren 
    - RTC weil es ja kein NTP im Netz gibt :>
  * Info LCD via USB an Raspberry
    - Arduino 
    - 4x20 Zeichen LCD mit HD44 Chipsatz
  * Arduino Sensor Node
    - 1 Wire Temperatur
    - Gyro
    - GPS
    - Kompass
    - G Kraft

### Fahrzeug 2

  * Arduino Sensor Node
    - ESP8266 WLAN Modul
    - 1 Wire Temperatur
    - Gyro
    - Kompass
    - G Kraft

### Fahrzeug 3

  * Arduino Sensor Node
    - ESP8266 WLAN Modul
    - 1 Wire Temperatur
    - Gyro
    - GPS
    - Kompass
    - G Kraft

## Software

### Musik

MPD auf Raspberry und Steuerung via Laptop/Tablet/Handy.

### Sensor Daten Erfassung/Speicherung

Die Sensor Daten werden von Arduinos erfasst und via USB oder WLan an den Raspberry übertragen. Dort werden diese verarbeitet und in einer geeigneten Datenbank Archiviert. 
Dieser Part wird vorraussichtlich in Python umgesetzt. 

Daten Archivierung geschieht in CSV Files. Dabei geht es rein darum die Daten zu Sichern und nicht auszuwerten.
Damit wir unterwegs auch Graphen auswerten können setzen wir parallel RRDTool ein. 
Die aktuellen Messwerte werden file based abgelegt um mit Linux Board mittel und eigentlich jeder andern Programmiersprache darauf zugreifen zu können.

### Sensor Visualisierung

Die in einer Datenbank erfassten Sensor Daten werden mit einer Node.JS APP auf Handy/Tablet verfügbar gemacht. Zum Einsatz kommt SocketStream, ein Node.JS Framework für Realtime Web Apps.
Das Framework liefert die erstellten Graphen aus und aktuallisiert in Realtime die Sensordaten.
