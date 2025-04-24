import subprocess
import os

# Konfiguration
MULTI_MONITOR_TOOL_PATH = r"C:\Users\rosep\Desktop\Multimonitortool\multimonitortool-x64\MultiMonitorTool.exe"  # Pfad anpassen
MONITOR_INDEX = 3  # Index des Monitors (1 = erster Monitor)

def get_monitor_status():
    """Ermittelt den Status des Monitors"""
    try:
        result = subprocess.run([MULTI_MONITOR_TOOL_PATH, "/scomma"],
                              capture_output=True, text=True, check=True, shell=True)
        lines = result.stdout.split('\n')
        for line in lines[1:]:  # Kopfzeile überspringen
            if line.strip():
                parts = line.split(',')
                if len(parts) > 2 and parts[0].strip() == str(MONITOR_INDEX):
                    return parts[2].strip() == "1"
        return False
    except Exception as e:
        print(f"Fehler beim Abrufen des Monitorstatus: {e}")
        return None

def toggle_monitor():
    """Schaltet den Monitor um"""
    status = get_monitor_status()
    if status is None:
        return

    try:
        if status:
            print(f"Deaktiviere Monitor {MONITOR_INDEX}...")
            subprocess.run([MULTI_MONITOR_TOOL_PATH, "/disable", str(MONITOR_INDEX)],
                         check=True, shell=True)
        else:
            print(f"Aktiviere Monitor {MONITOR_INDEX}...")
            subprocess.run([MULTI_MONITOR_TOOL_PATH, "/enable", str(MONITOR_INDEX)],
                         check=True, shell=True)
        print("Erfolgreich ausgeführt!")
    except Exception as e:
        print(f"Fehler beim Umschalten: {e}")

if __name__ == "__main__":
    if not os.path.exists(MULTI_MONITOR_TOOL_PATH):
        print(f"Tool nicht gefunden unter: {MULTI_MONITOR_TOOL_PATH}")
    else:
        toggle_monitor()