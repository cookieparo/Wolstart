import ctypes
import os
import time

# Konfiguration
RICHTUNG = "rechts"  # "links" oder "rechts"
WARTEZEIT = 6  # Sekunden bis Big Picture geladen ist
WIEDERHOLUNGEN = 2  # Wie oft die Tastenkombination gesendet wird

# WinAPI Setup
user32 = ctypes.windll.user32
KEYEVENTF_KEYUP = 0x0002

# Tastencodes
WIN = 0x5B
SHIFT = 0x10
LINKS = 0x25
RECHTS = 0x27


def verschiebe_fenster():
    pfeil = RECHTS if RICHTUNG == "rechts" else LINKS

    for _ in range(WIEDERHOLUNGEN):
        # Tastenkombination senden
        user32.keybd_event(WIN, 0, 0, 0)
        user32.keybd_event(SHIFT, 0, 0, 0)
        user32.keybd_event(pfeil, 0, 0, 0)

        time.sleep(0.15)  # Kurze Haltezeit

        # Tasten loslassen
        user32.keybd_event(pfeil, 0, KEYEVENTF_KEYUP, 0)
        user32.keybd_event(SHIFT, 0, KEYEVENTF_KEYUP, 0)
        user32.keybd_event(WIN, 0, KEYEVENTF_KEYUP, 0)

        time.sleep(0.5)  # Pause zwischen Wiederholungen


# Hauptprogramm

os.startfile("steam://open/bigpicture")
print(f"Warte {WARTEZEIT} Sekunden...")
time.sleep(WARTEZEIT)

verschiebe_fenster()
print(f"Fenster {WIEDERHOLUNGEN}x verschoben!")