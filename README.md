# Tailwind Setup

Tailwind is a powerful CSS framework it basically makes websites look very pretty very easily. The Moodle Info recommends using a CSS framework, and Tailwind is one of the best.

[Tailwind Docs](https://v3.tailwindcss.com/docs)

Steps:

1. Make sure Node.js is installed.
2. Run:

    ```bash
        npm install tailwindcss@3.4.17
    ```

3. During DEBUG, the watcher updates CSS changes automatically and applies them upon page reload. 


### Additional Setup

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```


## Optional: Tailwind Watcher

1.  Create a `.env` file at the project root containing:

    ```bash
    TAILWIND_WATCHER=True
    ```

If you prefer not to use the Tailwind watcher, simply omit or remove the `.env` file (or set `TAILWIND_WATCHER=False`).