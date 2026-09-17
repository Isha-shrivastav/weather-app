import tkinter as tk
from tkinter import messagebox
import requests

# ============================================================
# SIMPLE WEATHER APP
# Uses Open-Meteo API - NO API KEY REQUIRED
# ============================================================

def get_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning("Missing City", "Please enter a city name.")
        return

    search_button.config(state="disabled", text="Loading...")
    result_label.config(text="Fetching weather data...")
    root.update_idletasks()

    try:
        # ----------------------------------------------------
        # STEP 1: Find latitude and longitude of the city
        # ----------------------------------------------------
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )
        geo_response.raise_for_status()

        geo_data = geo_response.json()

        if "results" not in geo_data or not geo_data["results"]:
            messagebox.showerror(
                "City Not Found",
                f"Could not find '{city}'.\nTry another city name."
            )
            return

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")

        # ----------------------------------------------------
        # STEP 2: Get current weather
        # ----------------------------------------------------
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "weather_code,"
                "wind_speed_10m"
            ),
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )
        weather_response.raise_for_status()

        weather_data = weather_response.json()
        current = weather_data["current"]

        temperature = current["temperature_2m"]
        feels_like = current["apparent_temperature"]
        humidity = current["relative_humidity_2m"]
        wind_speed = current["wind_speed_10m"]
        weather_code = current["weather_code"]
        updated_time = current["time"]

        condition = get_weather_description(weather_code)
        icon = get_weather_icon(weather_code)

        # ----------------------------------------------------
        # STEP 3: Display result
        # ----------------------------------------------------
        result = (
            f"{icon}  {city_name}, {country}\n"
            f"{'─' * 34}\n\n"
            f"🌡  Temperature : {temperature} °C\n"
            f"🤔  Feels Like  : {feels_like} °C\n"
            f"💧  Humidity    : {humidity} %\n"
            f"💨  Wind Speed  : {wind_speed} km/h\n"
            f"☁️  Condition   : {condition}\n\n"
            f"🕐 Updated: {updated_time}"
        )

        result_label.config(text=result)

    except requests.exceptions.Timeout:
        messagebox.showerror(
            "Timeout",
            "The weather service took too long to respond.\nPlease try again."
        )
        result_label.config(text="Unable to fetch weather.")

    except requests.exceptions.ConnectionError:
        messagebox.showerror(
            "Internet Error",
            "Internet connection is required.\nPlease check your connection."
        )
        result_label.config(text="Unable to connect to weather service.")

    except requests.exceptions.HTTPError as error:
        messagebox.showerror(
            "API Error",
            f"Weather service returned an error:\n{error}"
        )
        result_label.config(text="Weather service error.")

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{error}"
        )
        result_label.config(text="Something went wrong.")

    finally:
        search_button.config(state="normal", text="🔍 Get Weather")


def get_weather_description(code):
    descriptions = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Rime Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Heavy Drizzle",
        56: "Light Freezing Drizzle",
        57: "Heavy Freezing Drizzle",
        61: "Light Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        66: "Light Freezing Rain",
        67: "Heavy Freezing Rain",
        71: "Light Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",
        77: "Snow Grains",
        80: "Light Rain Showers",
        81: "Moderate Rain Showers",
        82: "Heavy Rain Showers",
        85: "Light Snow Showers",
        86: "Heavy Snow Showers",
        95: "Thunderstorm",
        96: "Thunderstorm + Light Hail",
        99: "Thunderstorm + Heavy Hail"
    }

    return descriptions.get(code, "Unknown Weather")


def get_weather_icon(code):
    if code == 0:
        return "☀️"
    elif code in (1, 2):
        return "🌤️"
    elif code == 3:
        return "☁️"
    elif code in (45, 48):
        return "🌫️"
    elif code in (51, 53, 55, 56, 57):
        return "🌦️"
    elif code in (61, 63, 65, 66, 67, 80, 81, 82):
        return "🌧️"
    elif code in (71, 73, 75, 77, 85, 86):
        return "❄️"
    elif code in (95, 96, 99):
        return "⛈️"
    else:
        return "🌍"


def search_on_enter(event):
    get_weather()


# ============================================================
# GUI
# ============================================================

root = tk.Tk()
root.title("Weather App")
root.geometry("560x650")
root.resizable(False, False)
root.configure(bg="#eaf4ff")

# Header
header = tk.Frame(root, bg="#1769aa", height=120)
header.pack(fill="x")
header.pack_propagate(False)

title_label = tk.Label(
    header,
    text="🌤️ Weather App",
    font=("Arial", 28, "bold"),
    bg="#1769aa",
    fg="white"
)
title_label.pack(pady=(22, 3))

subtitle_label = tk.Label(
    header,
    text="Check current weather of any city",
    font=("Arial", 11),
    bg="#1769aa",
    fg="white"
)
subtitle_label.pack()

# Search area
search_frame = tk.Frame(root, bg="#eaf4ff")
search_frame.pack(pady=28)

city_entry = tk.Entry(
    search_frame,
    width=27,
    font=("Arial", 16),
    justify="center",
    relief="solid",
    bd=1
)
city_entry.pack(side="left", ipady=9, padx=(0, 10))
city_entry.insert(0, "Kanpur")

search_button = tk.Button(
    search_frame,
    text="🔍 Get Weather",
    font=("Arial", 11, "bold"),
    bg="#1769aa",
    fg="white",
    activebackground="#0d4f80",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=get_weather
)
search_button.pack(side="left", ipady=8, ipadx=8)

# Result card
card = tk.Frame(
    root,
    bg="white",
    bd=1,
    relief="solid"
)
card.pack(
    padx=35,
    pady=5,
    fill="both",
    expand=True
)

result_label = tk.Label(
    card,
    text="Enter a city and click\nGet Weather",
    font=("Arial", 15),
    bg="white",
    fg="#222222",
    justify="center",
    anchor="center"
)
result_label.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=30
)

# Information
info_label = tk.Label(
    root,
    text="Weather data: Open-Meteo  •  Internet connection required",
    font=("Arial", 9),
    bg="#eaf4ff",
    fg="#555555"
)
info_label.pack(pady=(12, 16))

# Enter key support
city_entry.bind("<Return>", search_on_enter)

# Put cursor in search box
city_entry.focus()

root.mainloop()
