# Windy API Accessor

The main branch may not work, use a release branch instead for production code.

Always make sure to check if you are using the testing or production table, this can be found in `src/database/models.py`.

### Building (Windows)

1. `py -m venv .venv`.
2. `.venv\Scripts\activate`.
3. `pip install -r requirements.txt`.
4. Create a `keys.txt` file in the repository root and add windy api keys to it.
5. Create a `.env` file in the repository root using the `.env.example` template and add MySQL database details.

### Building (Unix based)

1. `python3 -m venv .venv`.
2. `chmod +x .venv/bin/activate`.
3. `.venv/bin/activate`.
4. `pip install -r requirements.txt`.
5. Create a `keys.txt` file in the repository root and add windy api keys to it.
6. Create a `.env` file in the repository root using the `.env.example` template and add MySQL database details.

### Running

When running on Unix based, use `python3` whereas on Windows, use `py`.

To run the program once, use `py/python3 -m src` whereas if you want to run it on a 6 hour loop forever, use `py/python3 run.py`.