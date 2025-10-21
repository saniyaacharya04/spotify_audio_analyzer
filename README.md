Perfect! Here’s an **updated README** with a concise **Quick Demo section** that clearly shows how to run the app and what outputs to expect—without using any screenshots:

---

# Spotify Audio Feature Analyzer

A comprehensive Python application to analyze Spotify playlists using audio features. This project allows you to visualize and cluster songs interactively using **Streamlit**, **Plotly**, **Matplotlib**, and **KMeans clustering** from scikit-learn. It’s designed for music enthusiasts, data analysts, and portfolio projects.

---

## Features

1. **Fetch Spotify Playlist Tracks**

   * Input either a Spotify Playlist ID or full URL.
   * Fetches all tracks (supports playlists with 100+ tracks).

2. **Audio Feature Extraction**

   * Uses the Spotify API to retrieve detailed audio features for each track, including:

     * Danceability, Energy, Key, Loudness, Mode, Speechiness
     * Acousticness, Instrumentalness, Liveness, Valence, Tempo
     * Duration, Time Signature

3. **Interactive Visualizations**

   * **2D Scatter Plots**: Compare any two features.

     * Matplotlib: Static scatter plots with color-coded values.
     * Plotly: Interactive scatter plots with hover labels.
   * **3D Clustering**: Visualize KMeans clusters in 3D or 2D depending on features selected.
   * **Radar Charts**: Compare average feature values across clusters.

4. **Dynamic Clustering**

   * Select features for KMeans clustering dynamically.
   * Choose the number of clusters (2–10).
   * Highlights which tracks belong to each cluster.

5. **Cluster Summary Dashboard**

   * Shows average feature values per cluster.
   * Displays cluster sizes.
   * Automatically color-coded table for high/low values.
   * Lists **top songs per cluster**.

6. **Download Data**

   * Export full playlist features and cluster info as CSV.

---

## Tech Stack

* **Python 3.13**
* **Spotipy** – Spotify Web API wrapper
* **Streamlit** – Interactive web dashboard
* **Pandas** – Data manipulation
* **Matplotlib & Plotly** – Data visualization
* **Scikit-learn** – KMeans clustering

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/saniyaacharya04/spotify_audio_analyzer.git
cd spotify_audio_analyzer
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set Spotify API credentials as environment variables**

```bash
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
```

> For Windows PowerShell:

```powershell
$env:SPOTIFY_CLIENT_ID="your_client_id"
$env:SPOTIFY_CLIENT_SECRET="your_client_secret"
```

---

## Usage

### Run as a Python Script

```bash
python analyzer.py
```

* Enter a **Spotify Playlist ID** or URL when prompted.
* The script fetches tracks, audio features, and displays static 2D scatter plots, 3D clustering, and cluster info.

### Run as a Streamlit Web App

```bash
streamlit run app.py
```

* Open your browser to the local URL shown by Streamlit.
* Enter playlist ID/URL and use sidebar controls to:

  * Select features for visualization
  * Set number of clusters
  * Toggle between Matplotlib and Plotly
  * Generate radar charts and summary tables
* Download full audio features CSV using the “Download Data” tab.

---

## Quick Demo

1. **Launch the app:**

```bash
streamlit run app.py
```

2. **Enter a playlist URL or ID** (example):

```
https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
```

3. **Use sidebar to select:**

   * Number of clusters (K)
   * X/Y features for 2D plots
   * Bubble size and color features
   * Features for clustering and radar charts

4. **Expected outputs:**

   * **2D Scatter Plots:** Tempo vs Energy or any selected features
   * **3D Clustering:** Interactive 3D or 2D clusters
   * **Cluster Summary:** Average feature values per cluster with top songs listed
   * **Radar Chart:** Comparison of selected features across clusters
   * **CSV Download:** Export all features with cluster info

---

## File Structure

```
spotify_audio_analyzer/
│
├─ analyzer.py          # Command-line Python script for playlist analysis
├─ app.py               # Streamlit web app with interactive dashboard
├─ requirements.txt     # Python dependencies
├─ README.md            # Project documentation
├─ venv/                # Python virtual environment
└─ __pycache__/         # Cached Python files
```

---

## Notes

* Requires **Spotify Developer Account** to get `client_id` and `client_secret`.
* Designed for playlists of any size, automatically handles pagination.
* All clustering and plots are dynamic and configurable via sidebar controls in Streamlit.
* Includes error handling for invalid playlist URLs or empty playlists.

---

## Dependencies

Key dependencies (see `requirements.txt` for full list):

```text
streamlit==1.50.0
spotipy==2.25.1
pandas==2.3.3
matplotlib==3.10.7
plotly==6.3.1
scikit-learn==1.7.2
python-dotenv==1.1.1
numpy==2.3.4
requests==2.32.5
```

---

## Portfolio Highlights

* Fully interactive dashboard with **dynamic clustering**
* Feature selection for plots and clustering
* Radar chart summaries per cluster
* Downloadable CSV data
* Professional-looking visualizations for portfolio showcase

---

## License

This project is **MIT License** — free to use and modify for personal projects or portfolios.

---

If you want, I can also **add a “Tips & Tricks” section** with suggestions for customizing the dashboard and improving cluster analysis, which will make it look ultra-professional for your portfolio.

Do you want me to add that next?
