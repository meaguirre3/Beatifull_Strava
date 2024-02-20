# Beatifull Strava Route

This Python application utilizes the Strava gpx route data visualizes it using OSMnx.

## Overview

This application serves the purpose of plotting GPX routes recorded on Strava onto OpenStreetMap using OSMnx library. It provides an easy-to-use interface for fetching and displaying routes from Strava accounts.

## Features

- **Strava Integration:** Seamlessly connects to Strava API to access GPX route data.
- **GPX Parsing:** Parses GPX files fetched from Strava to extract route information.
- **OSMnx Visualization:** Utilizes OSMnx library to plot routes onto OpenStreetMap.
- **Interactive Interface:** Offers a user-friendly interface for selecting and displaying routes.

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

1. Obtain Strava API credentials by creating a Strava API application.
2. Set your Strava API credentials (client ID and client secret) in the `config.py` file.
3. Run the application:

    ```bash
    streamlit run home.py
    ```

## Contributions

Contributions are welcome! If you find any issues or have suggestions for improvements, meaguirre3@gmail.com


## Acknowledgements

- OSMnx: [OSMnx](https://osmnx.readthedocs.io/en/stable/) 


