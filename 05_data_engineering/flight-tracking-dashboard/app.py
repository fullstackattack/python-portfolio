from flask import Flask, render_template
from utils.fetch_opensky import fetch_opensky_data
from utils.map_helpers import create_aircraft_map

import plotly.io as pio

app = Flask(__name__)

@app.route("/")

def index():
    df = fetch_opensky_data()
    print(df.head())
    fig = create_aircraft_map(df)
    graph_html = pio.to_html(
    fig,
    full_html=False,
    include_plotlyjs=True   # <— forces Plotly JS into the page
)


    return render_template("index.html", graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True)
