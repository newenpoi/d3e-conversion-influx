# main.py
import colorama
from threading import Thread
from colorama import Fore
from app import create_app
from app.utils.file_watcher import start_watching

# Initialize colorama (=~ méthode statique).
colorama.init(autoreset = True)

# La fonction (callback) déclenchée par le watch dog (reste à compléter la logique).
def on_new_file_created(file_path):
    print(Fore.YELLOW + f"Un nouveau csv vient de pop dans le dossier à l'adresse : {file_path}.")

if __name__ == '__main__':
    # Création de l'application web.
    app = create_app()

    # Notre thread prend une cible en argument, ainsi qu'un tuple d'arguments (sorte de liste) qui correpsondent à la signature de la cible.
    # Un thread de type daemon, signifie qu'il shutdown auto lorsque le programme est interrompu et libère les ressources allouées en évitant tout conflit.
    watcher_thread = Thread(target = start_watching, args = (app.config['CSV_FOLDER_PATH'], on_new_file_created, app.config['WATCHDOG_SLEEP_INTERVAL']), daemon = True)
    
    # Démarre le thread.
    watcher_thread.start()
    
    # Lance l'application et évite qu'un nouveau thread ne soit exécuté en cas de rechargement à chaud (hot reload) lorsque le debugger est actif.
    app.run(debug = app.config['DEBUG'], use_reloader = False)