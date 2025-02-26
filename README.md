# Weather Forecasting Exercise

---

## Table of Contents
1. [Project Structure](#project-structure)
2. [How to Run the Scripts](#how-to-run-the-scripts)

---

## Project Structure

The directory structure for this project is as follows:

```plaintext
weather/
│
├── data/
│   └── get_data.py
│   └── weather.db
│   └── weather.csv
|
├── api/
|       └── app.py
|       └── queries.sql
|       
├── README.md
|
├── report.txt
|
└── requirements.txt

```


### Using Conda

1. Create a new Conda environment:

```bash
    conda create --name weather python=3.9
```
2. Activate the environment:

```bash
    conda activate weather
```

3. Install the required dependencies:

```bash
    pip install -r requirements.txt
```
4. Verify the installation: Ensure that all required packages are installed successfully by running:   

```bash
    conda list
```

### Using Virtualenv

1. Create a new virtual environment:

```bash
    python -m venv weather
```
2. Activate the virtual environment:

- Windows:

```bash
    .\weather\Scripts\activate
```

- Linux/ MacOS:

```bash
    source env/bin/activate
```

3. Install the required dependencies:

```bash
    pip install -r requirements.txt
```
4. Verify the installation: Ensure that all required packages are installed successfully by running:   

```bash
    pip list
```

## How to Run the Scripts

1. Change the directory to the weather app directory:
```bash
    cd [path_to]/weather/
```

2. Activate the environment (if not already activated):

- Conda:

```bash
    conda activate weather
```
- Virtualenv:

```bash
    source weather/bin/activate  # or .\weather\Scripts\activate for Windows
```
3. Run data collection script (also creates weather.db and weather.csv):

```bash
    python .\data\get_data.py
```

4. Run the Flask app:

```bash
    python .\api\app.py
```

5. Assuming your Flask application is running on http://127.0.0.1:5000, here are example API calls:

All locations:
```bash
    http://127.0.0.1:5000/locations
```

Daily forecasts:
```bash
    http://127.0.0.1:5000/daily_forecasts
```

Average Temperatures:
```bash
    http://127.0.0.1:5000/avg_temp
```


Top 2 locations by temperature:
```bash
    http://127.0.0.1:5000/top_locations?metric=temperature&n=2
```

Top 3 locations by wind speed:
```bash
    http://127.0.0.1:5000/top_locations?metric=wind_speed&n=3
```

