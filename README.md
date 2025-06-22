# ⚡ Lightning Density Lookup Web App

This Flask-based web app allows users to enter a location (address or coordinates) and receive an estimated lightning flash density for that area, based on a calibrated heatmap image. It visually assists in lightning risk awareness and planning, especially in industries like infrastructure, energy, and aerospace.

---

## 🌐 Live Demo
> 🚫 Not deployed yet. Want to see it in action? [Contact me](mailto:carlos33381224@gmail.com) or [connect on LinkedIn](https://www.linkedin.com/in/carlos-mata2).

---

## 🧠 How It Works

1. User inputs an address
2. The app geocodes it into latitude & longitude
3. These coordinates are mapped to a calibrated lightning density heatmap
4. The pixel color at that location is matched to a flash density category (e.g., flashes/km²/year)
5. The result is shown in a clean UI

> ⚠️ Note: Due to data licensing restrictions, the original heatmap image used in this app is not included in the repository.

---

## 🚀 Features

- 📍 Accepts addresses or coordinates
- 🗺️ Maps real-world locations to a heatmap overlay
- 🎯 Returns estimated lightning flash density
- ⚙️ Built with Flask and OpenCage Geocoding API
- 🧼 Clean and responsive front-end (HTML/CSS)

---

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3 (with embedded styling)
- **Geocoding**: OpenCage API (or similar)
- **Deployment-ready**: Includes a `Procfile` for platforms like Heroku

---

## 📂 Repository Contents

| File / Folder         | Description                              |
|-----------------------|------------------------------------------|
| `app.py`              | Main Flask application (clean + safe)    |
| `templates/index.html`| HTML frontend with Jinja placeholders    |
| `static/`             | Color legend image (if non-restricted)   |
| `Procfile`            | Deployment configuration for Heroku      |
| `requirements.txt`    | Python dependencies                      |
| `.gitignore`          | Excludes `.env` and Python bytecode      |

---

## 🔐 Sensitive Files Omitted

This repo excludes:
- `.env` file with API keys
- Calibrated lightning heatmap image (licensed)
- Raw calibration data or processing logic

These are retained privately due to licensing or security.

---

## 👤 Author

**Carlos Mata**  
B.S. Computer Science — University of Central Florida  
[GitHub](https://github.com/carlosmiguel1224) | [LinkedIn](https://www.linkedin.com/in/carlos-mata2)

---

## 📬 Contact

Interested in seeing a demo, collaborating, or learning more?  
📩 Email: [carlos33381224@gmail.com](mailto:carlos33381224@gmail.com)  
🔗 LinkedIn: [linkedin.com/in/carlos-mata2](https://www.linkedin.com/in/carlos-mata2)

