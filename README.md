# 🌤️ Simple Python Weather App

This is a complete beginner-friendly desktop Weather App made with Python and Tkinter.

## Features

- GUI using Tkinter
- Search weather by city name
- Temperature
- Feels-like temperature
- Humidity
- Wind speed
- Weather condition
- Weather icons
- Error handling
- Press Enter to search
- No API key required

## Requirements

- Python 3.10 or newer
- Internet connection
- `requests` package

## Installation

Open the project folder in VS Code.

Open Terminal and run:

```bash
pip install requests
```

Or:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

## If `python` does not work

Try:

```bash
py app.py
```

## Important

This app uses the Open-Meteo geocoding and weather APIs. An internet connection is required.

## Project Structure

```text
weather_app_complete/
│
├── app.py
├── requirements.txt
└── README.md
```

## Common Error

### ModuleNotFoundError: No module named 'requests'

Run:

```bash
python -m pip install requests
```

Then run:

```bash
python app.py
```
