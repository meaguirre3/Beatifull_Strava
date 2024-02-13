import osmnx as ox
import pandas as pd
import gpxpy
import gpxpy.gpx
import polyline
from shapely.geometry import Polygon, Point

def read_gpx_file(path):
    """
    Reads a GPX (GPS Exchange Format) file and extracts latitude, longitude, and elevation information.

    Parameters:
    - path (str): The file path to the GPX file.

    Returns:
    - pandas.DataFrame: A DataFrame containing extracted information from the GPX file.
    """
    with open(path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    # extract in gpx file latitude, longitude  and elevation
    route_info = [{'latitude': point.latitude,'longitude': point.longitude,'elevation': point.elevation} 
                  for track   in gpx.tracks  
                  for segment in track.segments 
                  for point   in segment.points ]
    # route_df Dataframe
    route_df = pd.DataFrame(route_info)
    
    return route_df



def find_centroid(route):
    """
    Finds the centroid of a polygon defined by the coordinates of a route.

    Parameters:
    - route (DataFrame): A DataFrame containing the coordinates of the route.
    
    Returns:
    Tuple: A tuple containing the coordinates (latitude, longitude) of the centroid of the polygon.
    """
    # Crear un objeto de polígono con las coordenadas
    poligono = Polygon(zip(route.longitude.values.tolist(), route.latitude.values.tolist()))

    # Encontrar el centroide del polígono
    centroide = poligono.centroid

    # Obtener las coordenadas del centroide
    centroide_latitud, centroide_longitud = centroide.y, centroide.x

    return centroide_latitud, centroide_longitud


def get_dist_graph(route, center):
    """
    Calculate the maximum distance from the specified center to the edges of the given route.

    Parameters:
    - route (DataFrame): A DataFrame containing the coordinates of the route.
    - center (Tuple): A tuple containing the coordinates (latitude, longitude) of the center.

    Returns:
    float: The maximum distance from the center to any edge of the route, plus 500 meters.
    """
    dist = []

    # Calculate distance to the top edge of the route
    dist.append(ox.distance.great_circle_vec(center[0], center[1], route.latitude.max(), center[1]))

    # Calculate distance to the right edge of the route
    dist.append(ox.distance.great_circle_vec(center[0], center[1], center[0], route.longitude.max()))

    # Calculate distance to the bottom edge of the route
    dist.append(ox.distance.great_circle_vec(center[0], center[1], route.latitude.min(), center[1]))

    # Calculate distance to the left edge of the route
    dist.append(ox.distance.great_circle_vec(center[0], center[1], center[0], route.longitude.min()))

    # Return the maximum distance plus 500 meters
    return max(dist) + 1000


def edge_line_color(G):
    """
    Generate lists of edge widths and colors based on characteristics of the graph edges.

    Parameters:
    - G (networkx.Graph): The graph for which edge characteristics are to be determined.

    Returns:
    Tuple: A tuple containing two lists - `roadWidths` and `roadColors`.
        - `roadWidths` (list): List of edge widths corresponding to the edges in the graph.
        - `roadColors` (list): List of edge colors corresponding to the edges in the graph.
    """
    # Define data characteristics
    u = []
    v = []
    key = []
    data = []
    
    # Extract edge data
    for uu, vv, kkey, ddata in G.edges(keys=True, data=True):
        u.append(uu)
        v.append(vv)
        key.append(kkey)
        data.append(ddata)
    
    # Lists to store colors and widths
    roadColors = []
    roadWidths = []

    for item in data:
        if "length" in item.keys():
            if item["length"] <= 100:
                linewidth = 0.10
                color = "#a6a6a6" 

            elif 100 < item["length"] <= 200:
                linewidth = 0.15
                color = "#676767"

            elif 200 < item["length"] <= 400:
                linewidth = 0.25
                color = "#454545"

            elif 400 < item["length"] <= 800:
                color = "#bdbdbd"
                linewidth = 0.35
            else:
                color = "#d5d5d5"
                linewidth = 0.45

            if "primary" in item.get("highway", ""):
                linewidth = 0.5
                color = "#ffff"
        else:
            color = "#a6a6a6"
            linewidth = 0.10

        roadColors.append(color)
        roadWidths.append(linewidth)

    for item in data:
        if "footway" in item.get("highway", ""):
            color = "#ededed"
            linewidth = 0.25
        else:
            color = "#a6a6a6"
            linewidth = 0.5
        roadWidths.append(linewidth)

    return roadWidths, roadColors
