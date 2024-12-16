import os
import subprocess
import threading
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image

# Configuración
KOMETA_SCRIPT = r".\kometa-venv\Scripts\python.exe"
KOMETA_FILE = r".\kometa.py"
KOMETA_TIMES = "22:00,03:00"  # Horas programadas
ICON_PATH = r".\iconKC.png"  # Ruta del ícono

# Variable global para el proceso
kometa_process = None

def load_icon():
    """Carga el ícono proporcionado."""
    return Image.open(ICON_PATH)

def start_kometa(icon, item):
    """Inicia el script kometa.py en segundo plano."""
    global kometa_process
    if kometa_process is None or kometa_process.poll() is not None:
        kometa_process = subprocess.Popen(
            [KOMETA_SCRIPT, KOMETA_FILE, "--times", KOMETA_TIMES],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        icon.notify(f"Kometa Started.\nWill execute at {KOMETA_TIMES}", "Kometa Control")
        icon.update_menu()  # Actualiza menú
    else:
        icon.notify("Kometa still running.", "KometaControl")

def stop_kometa(icon, item):
    """Detiene Kometa si está en ejecución."""
    global kometa_process
    if kometa_process and kometa_process.poll() is None:
        kometa_process.terminate()
        kometa_process = None
        icon.notify("Kometa stopped.", "Kometa Control")
        icon.update_menu()  # Actualiza menú

def quit_app(icon, item):
    """Cierra la aplicación y detiene el script si está activo."""
    global kometa_process
    if kometa_process and kometa_process.poll() is None:
        kometa_process.terminate()
    icon.stop()

def is_kometa_running():
    """Verifica si Kometa está en ejecución."""
    return kometa_process and kometa_process.poll() is None

def kometa_status():
    """Devuelve el estado de Kometa para el menú."""
    if is_kometa_running():
        return f"Kometa running | Will execute at: {KOMETA_TIMES}"
    return "Kometa Stopped"

# Menú dinámico del ícono
def generate_menu():
    return Menu(
        MenuItem(lambda text: kometa_status(), None, enabled=False),  # Botón informativo
        MenuItem("Start Kometa", start_kometa, enabled=lambda item: not is_kometa_running()),
        MenuItem("Stop Kometa", stop_kometa, enabled=lambda item: is_kometa_running()),
        MenuItem("Exit Kometa Control", quit_app)
    )

# Crear el ícono
icon = Icon("KometaControl", load_icon(), "KometaControl", generate_menu())

# Ejecutar el ícono en un hilo
def run_tray():
    icon.run()

if __name__ == "__main__":
    threading.Thread(target=run_tray).start()
