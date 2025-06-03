# Beatiful Strava Route

This Python application utilizes the Strava GPX route data and visualizes it using OSMnx. An additional Plotly implementation is also provided for interactive maps.

## Overview

This application serves the purpose of plotting GPX routes recorded on Strava onto OpenStreetMap using OSMnx library. It provides an easy-to-use interface for fetching and displaying routes from Strava accounts.

## Features

- **Strava Integration:** Seamlessly connects to Strava API to access GPX route data.
- **GPX Parsing:** Parses GPX files fetched from Strava to extract route information.
- **OSMnx Visualization:** Utilizes OSMnx library to plot routes onto OpenStreetMap.
- **Interactive Interface:** Offers a user-friendly interface for selecting and displaying routes.
- **Plotly Visualization:** `plotly_route.py` allows generating interactive maps using Plotly.

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/meaguirre3/Beatifull_Strava.git
    ```

2. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

```bash
    streamlit run home.py
```

### Plotly example

To generate an interactive map of a GPX file using Plotly run:

```bash
python plotly_route.py <route.gpx>
```

## Contributions

Contributions are welcome! If you find any issues or have suggestions for improvements, meaguirre3@gmail.com


## Acknowledgements

- OSMnx: [OSMnx](https://osmnx.readthedocs.io/en/stable/) 


