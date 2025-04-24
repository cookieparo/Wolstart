import subprocess
import os
import sys
import time
import ctypes

MMT_TOOL = r"C:\Users\rosep\Desktop\Multimonitortool\multimonitortool-x64\MultiMonitorTool.exe"
CONFIG_FILE = os.path.join(os.getcwd(), "monitor_config.cfg")

def is_admin():
    """Überprüft Admin-Rechte"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """Startet das Skript als Admin neu"""
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1)
        sys.exit()


def save_monitor_config():
    """Speichert aktuelle Monitor-Konfiguration"""
    try:
        subprocess.run(
            [MMT_TOOL, "/SaveConfig", CONFIG_FILE],
            check=True,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print("Fehler beim Speichern der Monitor-Konfiguration")


def set_primary_monitor(monitor_num=3):
    """Setzt den primären Monitor"""
    try:
        subprocess.run(
            [MMT_TOOL, "/SetPrimary", str(monitor_num)],
            check=True,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"Primärer Monitor auf Display {monitor_num} gesetzt")
    except subprocess.CalledProcessError:
        print("Fehler beim Wechseln des primären Monitors")


def start_steam_bigpicture():
    """Startet Steam Big Picture"""
    try:
        os.startfile("steam://open/bigpicture")
        print("Steam Big Picture wird gestartet...")
        time.sleep(5)  # Wartezeit für Steam-Start
    except Exception as e:
        print(f"Fehler beim Starten von Steam: {e}")


def is_steam_running():
    """Überprüft ob Steam läuft"""
    try:
        output = subprocess.check_output(
            'tasklist /fi "imagename eq steam.exe"',
            shell=True,
            stderr=subprocess.DEVNULL
        ).decode('utf-8', 'ignore')
        return "steam.exe" in output.lower()
    except:
        return False


def restore_monitor_config():
    """Stellt ursprüngliche Monitor-Konfiguration wieder her"""
    if os.path.exists(CONFIG_FILE):
        try:
            subprocess.run(
                [MMT_TOOL, "/LoadConfig", CONFIG_FILE],
                check=True,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            os.remove(CONFIG_FILE)
            print("Originale Monitor-Konfiguration wiederhergestellt")
        except subprocess.CalledProcessError:
            print("Fehler beim Wiederherstellen der Monitor-Konfiguration")

def audiosignal(index):
    subprocess.run(
        [f"powershell", "-Command", f"Set-AudioDevice -Index {index}"],
        check=True,
        shell=True
    )
def main():
    run_as_admin()

    try:
        save_monitor_config()
        set_primary_monitor(3)  # Monitor-Nummer anpassen
        audiosignal(1)
        start_steam_bigpicture()

        # Warten bis Steam beendet ist
        while is_steam_running():
            time.sleep(1)
        audiosignal(4)
    except KeyboardInterrupt:
        print("\nSkript wurde manuell beendet")
    except Exception as e:
        print(f"Unbehandelter Fehler: {e}")
    finally:
        restore_monitor_config()


if __name__ == "__main__":
    # PyCharm Debugging-Fix
    if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
        time.sleep(1)  # Verzögerung für Debugger
    main()