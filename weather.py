from flask import Flask, render_template, request
import requests
import os

# Absolute path configurations so Flask never loses your files
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)

# Replace with your actual OpenWeatherMap API Key
API_KEY = "YOUR_API_KEY_HERE"

@app.route("/", methods=["GET", "POST"])
def index():
    # Python sets a default neutral background image for the initial page load
    bg_image = "https://unsplash.com"
    html_output = ""

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"http://openweathermap.org{city}&appid={API_KEY}&units=metric"
            response = requests.get(url).json()

            if response.get("cod") == 200:
                condition = response["weather"][0]["main"].lower()
                temp = round(response["main"]["temp"])
                desc = response["weather"][0]["description"].capitalize()
                name = response["name"]

                # Python decides the background image asset natively
                if "clear" in condition:
                    bg_image = "https://unsplash.com"
                elif "cloud" in condition:
                    bg_image = "https://unsplash.com"
                elif "rain" in condition or "drizzle" in condition or "thunderstorm" in condition:
                    bg_image = "https://unsplash.com"
                elif "snow" in condition:
                    bg_image = "https://unsplash.com"
                elif "mist" in condition or "fog" in condition or "haze" in condition:
                    bg_image = "https://unsplash.com"

                # Python constructs the interface components directly
                html_output = f"""
                    <div class='weather-display'>
                        <h3 style='font-size: 1.4rem; margin: 0; font-weight: 500;'>{name}</h3>
                        <h1 class='temp-display'>{temp}°C</h1>
                        <p style='text-transform: capitalize; margin: 5px 0 0 0;'>{desc}</p>
                    </div>
                """
            else:
                html_output = "<p class='error-message'>City not found! Please try again.</p>"

    return render_template("index.html", content=html_output, background=bg_image)

if __name__ == "__main__":
    app.run(debug=True)
