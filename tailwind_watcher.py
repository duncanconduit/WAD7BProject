import subprocess
import threading

def run_tailwind_watch():
    command = [
        'npx',
        'tailwindcss',
        '-i', './static/css/input.css',
        '-o', './static/css/output.css',
        '--watch'
    ]
    process = subprocess.Popen(command)
    print('TailwindCSS watcher started.')
    return process

def start_tailwind_thread():
    thread = threading.Thread(target=run_tailwind_watch, daemon=True)
    thread.start()
