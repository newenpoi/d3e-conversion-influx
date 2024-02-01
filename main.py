# main.py
import os
import colorama
from threading import Thread
from dotenv import load_dotenv
from colorama import Fore
from app import create_app
from app.utils.file_watcher import start_watching

# Initialize colorama.
colorama.init(autoreset = True)

def on_new_file_created(file_path):
    print(Fore.YELLOW + f"Un nouveau csv vient de pop dans le dossier à l'adresse : {file_path}.")

if __name__ == '__main__':
    # Création de l'application web.
    app = create_app()

    # Dans un thread de type daemon, signifie qu'il shutdown auto lorsque le programme est interrompu.
    # Libérant proprement les ressources allouées et évitant tout conflit.
    watcher_thread = Thread(target = start_watching, args = (app.config['CSV_FOLDER_PATH'], on_new_file_created, app.config['WATCHDOG_SLEEP_INTERVAL']), daemon = True)
    
    # Démarre le thread.
    watcher_thread.start()
    
    # Lance l'application et évite qu'un nouveau thread ne soit exécuté en cas de rechargement à chaud (hot reload) lorsque le debugger est actif.
    app.run(debug = app.config['DEBUG'], use_reloader = False)