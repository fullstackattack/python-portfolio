from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

# Force load the .env file directly
load_dotenv(dotenv_path="/Users/millimanspostulate/Documents/NASA_APOD_API/.env")

app = Flask(__name__)

NASA_KEY = os.getenv("NASA_KEY")
print("Loaded NASA KEY:", NASA_KEY)

@app.route("/")
def home():
    return jsonify({
        "message": "NASA APOD API Wrapper",
        "usage": {
            "/apod": "Get today's Astronomy Picture of the Day",
            "/apod?date=YYYY-MM-DD": "Get APOD for a specific date"
        }
    })


@app.route("/apod")
def get_apod():
    nasa_url = "https://api.nasa.gov/planetary/apod"

    # Get ?date=YYYY-MM-DD
    date = request.args.get("date")

    params = {"api_key": NASA_KEY}

    if date:
        params["date"] = date

    # Request NASA APOD data
    response = requests.get(nasa_url, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch NASA data"}), response.status_code

    data = response.json()

    return jsonify({
        "title": data.get("title"),
        "date": data.get("date"),
        "description": data.get("explanation"),
        "image_url": data.get("hdurl") or data.get("url")
    })




# EARTH EPIC IMAGES

@app.route("/epic")
def epic():
    date = request.args.get("date")

    if not date:
        return jsonify({"error": "Please provide a date=YYYY-MM-DD"}), 400

    url = "https://api.nasa.gov/EPIC/api/natural/date/{date}"

    response = requests.get(url, params={"api_key": NASA_KEY})

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch EPIC Earth data"}), response.status_code

    data = response.json()

    cleaned = []
    for item in data:
        image = item["image"]
        year, month, day = date.split("-")
        image_url = "https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/png/{image}.png"

        cleaned.append({
            "identifier": item["identifier"],
            "caption": item.get("caption"),
            "image_url": image_url
        })

    return jsonify({
        "date": date,
        "image_count": len(cleaned),
        "images": cleaned
    })

# NEO – Near Earth Objects (Asteroids)

@app.route("/neo")
def neo():
    start = request.args.get("start")
    end = request.args.get("end")

    if not start or not end:
        return jsonify({"error": "Provide start=YYYY-MM-DD and end=YYYY-MM-DD"}), 400

    url = "https://api.nasa.gov/neo/rest/v1/feed"

    params = {
        "start_date": start,
        "end_date": end,
        "api_key": NASA_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch NEO data"}), response.status_code

    data = response.json()["near_earth_objects"]

    asteroids = []

    for date, objs in data.items():
        for asteroid in objs:
            asteroids.append({
                "name": asteroid["name"],
                "date": date,
                "diameter_km": asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
                "hazardous": asteroid["is_potentially_hazardous_asteroid"]
            })

    return jsonify({
        "asteroid_count": len(asteroids),
        "asteroids": asteroids
    })



#5. NASA Image & Video Library Search
@app.route("/images")
def image_search():
    query = request.args.get("query")

    if not query:
        return jsonify({"error": "Provide query=term"}), 400

    url = "https://images-api.nasa.gov/search"

    response = requests.get(url, params={"q": query})

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch NASA image data"}), response.status_code

    data = response.json().get("collection", {}).get("items", [])

    cleaned = []

    for item in data[:25]:  # return first 25 results
        title = item["data"][0].get("title")
        img_links = item.get("links", [])

        image_url = img_links[0]["href"] if img_links else None

        cleaned.append({
            "title": title,
            "image_url": image_url
        })

    return jsonify({
        "query": query,
        "result_count": len(cleaned),
        "results": cleaned
    })


from flask import render_template, request

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/dashboard/apod")
def dashboard_apod():
    url = "https://api.nasa.gov/planetary/apod?api_key={NASA_KEY}"
    response = requests.get(url)
    data = response.json()
    return render_template("apod.html", data=data)


@app.route("/dashboard/epic", methods=["GET", "POST"])
def dashboard_epic():
    images = None
    date = None

    if request.method == "POST":
        date = request.form.get("date")
        url = f"https://api.nasa.gov/EPIC/api/natural/date/{date}"
        response = requests.get(url, params={"api_key": NASA_KEY})

        if response.status_code == 200:
            data = response.json()
            year, month, day = date.split("-")
            images = [
                f"https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/png/{item['image']}.png"
                for item in data
            ]

    return render_template("epic.html", images=images, date=date)


@app.route("/dashboard/images", methods=["GET", "POST"])
def dashboard_images():
    results = None
    query = None

    if request.method == "POST":
        query = request.form.get("query")
        url = f"https://images-api.nasa.gov/search?q={query}"
        response = requests.get(url)
        data = response.json()
        results = []
        for item in data.get("collection", {}).get("items", []):
            title = item["data"][0]["title"]
            links = item.get("links", [])
            if links:
                results.append({"title": title, "img": links[0]["href"]})

    return render_template("images.html", query=query, results=results)


@app.route("/dashboard/neo", methods=["GET", "POST"])
def dashboard_neos():
    asteroids = None
    start = None
    end = None

    if request.method == "POST":
        start = request.form.get("start")
        end = request.form.get("end")

        url = "https://api.nasa.gov/neo/rest/v1/feed"
        params = {
            "start_date": start,
            "end_date": end,
            "api_key": NASA_KEY
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            raw = response.json().get("near_earth_objects", {})

            asteroids = []
            for date, objs in raw.items():
                for asteroid in objs:
                    asteroids.append({
                        "name": asteroid["name"],
                        "date": date,
                        "diameter_km": asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
                        "hazardous": asteroid["is_potentially_hazardous_asteroid"]
                    })

    return render_template(
        "neo.html",
        asteroids=asteroids,
        start=start,
        end=end
    )


if __name__ == "__main__":
    app.run(debug=True)
