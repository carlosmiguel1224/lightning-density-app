# app.py
import os
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from PIL import Image
from opencage.geocoder import OpenCageGeocode
from scipy.interpolate import RBFInterpolator
from dotenv import load_dotenv
load_dotenv()

# === CONFIGURATION ===
IMAGE_PATH = "Vaisala Annual Lightning Report 2020 copydetailed.png"
CSV_PATH = "calibration_points.csv"
API_KEY = os.getenv("OPENCAGE_API_KEY")  # Load API key from environment

# === LOAD CALIBRATION DATA ===
df = pd.read_csv(CSV_PATH)
latlons = df[["latitude", "longitude"]].values
pixels = df[["pixel_x", "pixel_y"]].values

# === TRAIN INTERPOLATORS ===
interp_x = RBFInterpolator(latlons, pixels[:, 0], kernel='thin_plate_spline')
interp_y = RBFInterpolator(latlons, pixels[:, 1], kernel='thin_plate_spline')

# === LOAD IMAGE ===
image = Image.open(IMAGE_PATH).convert("RGBA")

# === SET UP GEOCODER ===
geocoder = OpenCageGeocode(API_KEY)

# === LEGEND COLORS AND CATEGORIES ===
legend_colors = [
    ("up to 0.1",     (181, 188, 215)),
    ("0.1 to 0.5",    (30, 0, 182)),
    ("0.5 to 1",      (111, 175, 241)),
    ("1 to 2",        (130, 215, 217)),
    ("2 to 3",        (143, 242, 202)),
    ("3 to 4",        (152, 244, 110)),
    ("4 to 5",        (186, 243, 106)),
    ("5 to 6",        (250, 241, 91)),
    ("6 to 8",        (250, 241, 91)),
    ("8 to 10",       (219, 122, 43)),
    ("10 to 12",      (203, 15, 3)),
    ("12 and up",     (220, 128, 243))
]

# === FLASK APP ===
app = Flask(__name__)

# === HELPERS ===
def geocode_address(address):
    result = geocoder.geocode(address)
    if result and len(result) > 0:
        return result[0]['geometry']['lat'], result[0]['geometry']['lng']
    else:
        raise ValueError("Address not found.")

def latlon_to_pixel(lat, lon):
    point = np.array([[lat, lon]])
    x = float(interp_x(point))
    y = float(interp_y(point))
    return int(round(x)), int(round(y))

def get_rgb_from_pixel(x, y):
    r, g, b, a = image.getpixel((x, y))
    return r, g, b

def rgb_to_category(r, g, b):
    input_color = np.array([r, g, b])
    min_dist = float("inf")
    closest_category = None
    for category, rgb in legend_colors:
        dist = np.linalg.norm(input_color - np.array(rgb))
        if dist < min_dist:
            min_dist = dist
            closest_category = category
    return closest_category



def category_from_address(address):
    lat, lon = geocode_address(address)
    x, y = latlon_to_pixel(lat, lon)
    r, g, b = get_rgb_from_pixel(x, y)
    category = rgb_to_category(r, g, b)
    return {
        "address": address,
        "latitude": lat,
        "longitude": lon,
        "pixel_x": x,
        "pixel_y": y,
        "rgb": (r, g, b),
        "category": category
    }


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        address = request.form.get("address")
        try:
            result = category_from_address(address)
        except Exception as e:
            result = {"error": str(e)}
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
