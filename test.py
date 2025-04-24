import subprocess
import json


def switch_to_sony_tv():
    """Schaltet das Audio-Ausgabegerät automatisch auf den Sony-Fernseher (Index 1)."""
    try:
        # 1. PowerShell-Befehl: Wechsel zu Index 1 (Sony TV)
        subprocess.run(
            ["powershell", "-Command", "Set-AudioDevice -Index 1"],
            check=True,
            shell=True
        )
        print("✅ Erfolg: Audio wurde auf den Sony-Fernseher (Index 1) umgeleitet.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler: Umschalten fehlgeschlagen ({e}). Stelle sicher, dass:")
        print("- 'AudioDeviceCmdlets' installiert ist (Install-Module -Name AudioDeviceCmdlets -Force)")
        print("- Der Sony-Fernseher unter Index 1 in PowerShell gelistet ist (Get-AudioDevice -List)")


if __name__ == "__main__":
    switch_to_sony_tv()  # Sofortiger Wechsel bei Ausführung