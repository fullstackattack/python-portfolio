import plotly.express as px

def create_aircraft_map(df):
    fig = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="callsign",
        hover_data=["origin_country", "velocity", "baro_altitude"],
        color="baro_altitude",
        color_continuous_scale="Turbo",
        size_max=8,
        projection="natural earth",
    )

    fig.update_layout(
        mapbox_style="mapbox://styles/mapbox/light-v10",
        mapbox_accesstoken="pk.eyJ1IjoiYW1hbmRhc3RhbmxleTkwIiwiYSI6ImNtaW1meXpjODFtY2Qzam9jYzMzenJnbmgifQ.ZwW164ZxdE_SkMlVyUdLfQ",
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    return fig
