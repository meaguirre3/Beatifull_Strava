import sys
import util as ut
import plotly.io as pio

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python plotly_route.py <route.gpx>")
        sys.exit(1)

    gpx_path = sys.argv[1]
    with open(gpx_path, "r") as f:
        route_df = ut.read_gpx_file(f)

    fig = ut.plot_route_plotly(route_df, title="Strava Route")
    fig.show()
