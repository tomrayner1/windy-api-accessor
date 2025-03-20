# Windy API Accessor

### Building (Windows)

1. `py -m venv .venv`
2. `.venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. Create a `keys.txt` file in the repository root and add windy api keys to it.
5. `py -m src`

### Building (Mac)

1. `python3 -m venv .venv`
2. `chmod +x .venv/bin/activate`
3. `.venv/bin/activate`
4. `pip install -r requirements.txt`
5. Create a `keys.txt` file in the repository root and add windy api keys to it.
6. `python3 -m src`

### Data stored

Parameters: Date, Temp, ptype, precip, wind, windGust, lclouds, mclouds, hclouds

### Data cleaning

Data cleaning is now done automatically.