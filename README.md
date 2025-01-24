# Music Dashboard with TAPAS Model Integration

This project provides an interactive music dashboard built with **Streamlit** for data visualization and analysis of music datasets. It uses the **TAPAS model** for question answering on the music data.

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Features](#features)
- [Deployed Application](#deployed-application)

## Overview

This application allows users to:
- Analyze music popularity by genre and artist.
- Investigate the relationship between music features (such as energy, loudness, tempo, etc.) and genres.
- Utilize a TAPAS-based model for answering questions related to music data.
  
The dashboard is fully interactive, providing various options to filter and visualize the data based on different attributes.

## Getting Started

### Installation
To get started with this project, you need to clone this repository and install the required dependencies:

```bash
git clone https://github.com/aichaa28/app_analyse_musicale.git
pip install -r requirements.txt
streamlit run app.py
```
## Project Structure

Here is the structure of the project:

- `.github/`
  - `workflows/`                    Contains GitHub actions for continuous integration
- `__pycache__/`                    Compiled Python files
- `README.md`                       This file
- `app.py`                          The main Streamlit app file that integrates the dashboard and question answering functionality
- `column_description.txt`          Describes the columns in the dataset
- `dashboard.py`                    Contains functions for creating visualizations of the music data
- `data_cleaning.ipynb`             Jupyter notebook used for cleaning and preprocessing the dataset
- `dataset.csv`                     The dataset file containing music data used in the dashboard
- `home_page.py`                    Handles the home page layout and features of the dashboard
- `requirements.txt`                A list of required Python packages
- `song_page.py`                    Displays details related to songs and artists
- `tapas_model_code.py`             Contains the integration of the TAPAS model for question answering on the music data
- `test_dashboard.py`               Contains test cases for ensuring the functionality of the dashboard

## Features

- **Popularity by Genre**: Visualizes the average popularity of tracks by genre.
- **Top Artists by Popularity**: Displays the top artists based on average popularity.
- **Track Features by Genre**: Shows how features like energy, tempo, and valence differ by genre.
- **TAPAS Question Answering**: Provides an interface for asking questions about the music data, powered by the TAPAS model.

## Deployed Application
You can access the deployed application via the following link:  
[Go to the Deployed Application](https://aichaa28-app-analyse-musicale-app-sasvso.streamlit.app/)

