import osmnx as ox
import pandas as pd
import gpxpy
import gpxpy.gpx
from shapely.geometry import Polygon, Point

def read_gpx_file(gpx_file):
    """
    Reads a GPX (GPS Exchange Format) file and extracts latitude, longitude, and elevation information.
    """
    gpx = gpxpy.parse(gpx_file)
    route_info = [
        {"latitude": point.latitude, "longitude": point.longitude, "elevation": point.elevation}
        for track in gpx.tracks
        for segment in track.segments
        for point in segment.points
    ]
    return pd.DataFrame(route_info)


def find_centroid(route):
    """
    Finds the centroid of a polygon defined by the coordinates of a route.
    """
    polygon = Polygon(zip(route.longitude.values.tolist(), route.latitude.values.tolist()))
    centroid = polygon.centroid
    return centroid.y, centroid.x


def get_dist_graph(route, center):
    """
    Calculate the maximum distance from the specified center to the edges of the given route.

    This version is compatible with all OSMnx versions (<=1.2, 1.8.x, 1.9+).
    """
    import osmnx as ox
    import math

    def great_circle(lat1, lon1, lat2, lon2):
        """Fallback great circle distance in meters."""
        R = 6371000  # Earth radius in meters
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Detect correct OSMnx function dynamically
    if hasattr(ox, "distance") and hasattr(ox.distance, "great_circle_vec"):
        func = ox.distance.great_circle_vec
    elif hasattr(ox, "distance") and hasattr(ox.distance, "great_circle"):
        func = ox.distance.great_circle
    elif hasattr(ox, "utils_geo") and hasattr(ox.utils_geo, "great_circle_vec"):
        func = ox.utils_geo.great_circle_vec
    else:
        func = great_circle  # fallback to pure math version

    dist = []
    dist.append(func(center[0], center[1], route.latitude.max(), center[1]))
    dist.append(func(center[0], center[1], center[0], route.longitude.max()))
    dist.append(func(center[0], center[1], route.latitude.min(), center[1]))
    dist.append(func(center[0], center[1], center[0], route.longitude.min()))

    return max(dist) + 1000



def edge_line_color(G):
    """
    Generate lists of edge widths and colors based on edge characteristics.
    """
    data = [d for _, _, _, d in G.edges(keys=True, data=True)]
    roadColors, roadWidths = [], []

    for item in data:
        if "length" in item:
            length = item["length"]
            if length <= 100:
                linewidth, color = 0.10, "#a6a6a6"
            elif length <= 200:
                linewidth, color = 0.15, "#676767"
            elif length <= 400:
                linewidth, color = 0.25, "#454545"
            elif length <= 800:
                linewidth, color = 0.35, "#bdbdbd"
            else:
                linewidth, color = 0.45, "#d5d5d5"

            if "primary" in str(item.get("highway", "")):
                linewidth, color = 0.5, "#ffffff"
        else:
            linewidth, color = 0.10, "#a6a6a6"

        roadColors.append(color)
        roadWidths.append(linewidth)

    # Ajuste extra para footways
    for item in data:
        if "footway" in str(item.get("highway", "")):
            roadColors.append("#ededed")
            roadWidths.append(0.25)

    return roadWidths, roadColors


def linewidth(G):
    """
    Generate list of edge widths based on road lengths.
    """
    data = [d for _, _, _, d in G.edges(keys=True, data=True)]
    roadWidths = []

    for item in data:
        if "length" in item:
            length = item["length"]
            if length <= 100:
                lw = 0.10
            elif length <= 200:
                lw = 0.15
            elif length <= 400:
                lw = 0.25
            elif length <= 800:
                lw = 0.35
            else:
                lw = 0.45
            if "primary" in str(item.get("highway", "")):
                lw = 0.5
        else:
            lw = 0.10
        roadWidths.append(lw)

    return roadWidths


def plot_figure(global_variable, route_df, colorBackground, colorLines, colorRoute, title, colorText):
    """
    Plots a route on top of an OSM street graph.
    """
    linewidths = linewidth(global_variable)
    fig, ax = ox.plot_graph(
        global_variable,
        node_size=0,
        figsize=(27, 40),
        dpi=300,
        save=False,
        bgcolor=colorBackground,
        edge_color=colorLines,
        edge_alpha=1,
        show=False,
        edge_linewidth=linewidths,
    )

    # Dibujar la ruta sobre el gráfico
    ax.plot(
        route_df["longitude"],
        route_df["latitude"],
        color=colorRoute,
        linewidth=4.0,
    )

    # Agregar el título
    ax.text(
        0.5,
        0.03,
        title,
        ha="center",
        va="center",
        transform=ax.transAxes,
        fontsize=40,
        color=colorText,
        bbox=dict(facecolor=colorBackground, edgecolor=colorBackground, alpha=0.5),
    )

    return fig
