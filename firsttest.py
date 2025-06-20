import numpy as np
import pandas as pd
from PIL import Image
from opencage.geocoder import OpenCageGeocode
from scipy.interpolate import RBFInterpolator

# === CONFIGURATION ===
IMAGE_PATH = "Vaisala Annual Lightning Report 2020 copydetailed.png"
CSV_PATH = "calibration_points.csv"
API_KEY = "7d7ce9e3f07440bfa3dfca76bc8cbd0a"  # <-- Replace this with your actual API key

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

# === FUNCTION 1: Geocode Address ===
def geocode_address(address):
    result = geocoder.geocode(address)
    if result and len(result) > 0:
        return result[0]['geometry']['lat'], result[0]['geometry']['lng']
    else:
        raise ValueError("Address not found.")

# === FUNCTION 2: Lat/Lon to Pixel ===
def latlon_to_pixel(lat, lon):
    point = np.array([[lat, lon]])
    x = float(interp_x(point))
    y = float(interp_y(point))
    return int(round(x)), int(round(y))

# === FUNCTION 3: Pixel to RGB ===
def get_rgb_from_pixel(x, y):
    r, g, b, a = image.getpixel((x, y))
    return r, g, b

# === FUNCTION 4: RGB to Category ===
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

# === FUNCTION 5: Full End-to-End Pipeline ===
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



def main():

    # === EXAMPLE USAGE ===
    result = category_from_address("Tampa, FL")
    print(result)


if __name__ == "__main__":
    main()