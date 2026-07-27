import json
import urllib.request
import tkinter as tk
from tkinter import messagebox

def fetch_weather_and_update():
    city = city_input.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please type a city name first!")
        return

    # STEP 1: Convert the typed city name into geographical coordinates
    geo_url = f"https://open-meteo.com{city}&count=1&language=en&format=json"
    
    try:
        req_geo = urllib.request.Request(geo_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_geo) as geo_res:
            geo_data = json.loads(geo_res.read().decode())
            
            if 'results' not in geo_data or not geo_data['results']:
                messagebox.showerror("Error", f"Could not find coordinates for '{city}'. Check spelling!")
                return
                
            lat = geo_data['results'][0]['latitude']
            lon = geo_data['results'][0]['longitude']
            official_name = geo_data['results'][0]['name']

        # STEP 2: Use the precise coordinates to pull current ambient conditions
        weather_url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true"
        req_weather = urllib.request.Request(weather_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req_weather) as weather_res:
            data = json.loads(weather_res.read().decode())
            current = data['current_weather']
            temp_c = int(current['temperature'])
            
            # Map simple descriptions to basic criteria profiles
            if temp_c < 15:
                bg_color = "#34495E"      # Deep Dark Rainy Slate
                text_color = "#FFFFFF"    # White Text
                vibe_text = f"It's Cold! 🥶\n{temp_c}°C | Chilly atmosphere"
            elif temp_c < 25:
                bg_color = "#2ECC71"      # Soft Pleasant Green Canvas
                text_color = "#111111"    # Dark Text
                vibe_text = f"It's Pleasant! 😊\n{temp_c}°C | Clear skies"
            else:
                bg_color = "#E67E22"      # Sunset Warm Orange/Red
                text_color = "#FFFFFF"    # White Text
                vibe_text = f"It's Hot! 🔥\n{temp_c}°C | Sunny environment"

            # Apply layout adjustments directly over interface fields
            canvas.config(bg=bg_color)
            canvas.itemconfig(city_title_text, text=official_name.upper(), fill=text_color)
            canvas.itemconfig(weather_display_text, text=vibe_text, fill=text_color)
                
    except Exception as e:
        messagebox.showerror("Network Connection", f"API connection dropped:\n{e}")

# --- SETUP THE GRAPHICAL WINDOW INTERFACE ---
root = tk.Tk()
root.title("Weather Vibe Dashboard")
root.geometry("500x450")
root.resizable(False, False)

# Top Bar Interface Panel Configuration Settings
top_frame = tk.Frame(root, pady=10)
top_frame.pack(side=tk.TOP, fill=tk.X)

tk.Label(top_frame, text="Enter City:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
city_input = tk.Entry(top_frame, font=("Arial", 11), width=22)
city_input.pack(side=tk.LEFT, padx=5)
city_input.insert(0, "London") 

search_btn = tk.Button(top_frame, text="Check Vibe 🔍", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", command=fetch_weather_and_update)
search_btn.pack(side=tk.LEFT, padx=10)

# Main Application Dynamic Canvas Frame
canvas = tk.Canvas(root, width=500, height=400, bg="#2C3E50", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Typography Layout Components
city_title_text = canvas.create_text(250, 80, text="WEATHER DASHBOARD", font=("Arial", 20, "bold"), fill="#FFFFFF", justify="center")
weather_display_text = canvas.create_text(250, 220, text="Click 'Check Vibe' to update...", font=("Arial", 14, "bold"), fill="#FFFFFF", justify="center")

root.mainloop()
