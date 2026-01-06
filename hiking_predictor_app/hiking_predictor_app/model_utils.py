"""
Hiking speed prediction model utilities.
Loads and uses the trained model to predict hiking times.
"""

import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from geopy.distance import geodesic
from typing import Tuple, Dict, Optional
import gpxpy.gpx


def load_model(model_path: str) -> Tuple[object, list]:
    """
    Load the trained hiking speed model.

    Args:
        model_path: Path to the pickled model file

    Returns:
        Tuple of (model, feature_columns)
    """
    try:
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
            return model_data['model'], model_data['feature_cols']
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None


def smooth_elevation(elevations: np.ndarray, distances: np.ndarray, window_m: float = 100.0) -> np.ndarray:
    """
    Smooth elevation data using distance-based Gaussian weighting.

    Args:
        elevations: Array of elevation values
        distances: Array of cumulative distances
        window_m: Distance window for smoothing in meters

    Returns:
        Smoothed elevation array
    """
    smoothed = np.zeros_like(elevations)

    for i in range(len(elevations)):
        current_dist = distances[i]

        # Find points within window
        weights = []
        values = []

        for j in range(len(elevations)):
            dist_diff = abs(distances[j] - current_dist)
            if dist_diff <= window_m:
                weight = np.exp(-(dist_diff**2) / (2 * (window_m/3)**2))
                weights.append(weight)
                values.append(elevations[j])

        if weights:
            smoothed[i] = np.average(values, weights=weights)
        else:
            smoothed[i] = elevations[i]

    return smoothed


def calculate_slope_window(elevations_smoothed: np.ndarray, distances: np.ndarray,
                           index: int, window_m: float = 100.0) -> float:
    """
    Calculate slope over a distance window.

    Args:
        elevations_smoothed: Smoothed elevation array
        distances: Cumulative distance array
        index: Current point index
        window_m: Distance window for slope calculation

    Returns:
        Slope percentage
    """
    current_dist = distances[index]
    half_window = window_m / 2

    # Find point behind
    back_idx = index
    for j in range(index - 1, -1, -1):
        if current_dist - distances[j] >= half_window:
            back_idx = j
            break

    # Find point ahead
    forward_idx = index
    for j in range(index + 1, len(distances)):
        if distances[j] - current_dist >= half_window:
            forward_idx = j
            break

    # Calculate slope
    if forward_idx != back_idx:
        dist_span = distances[forward_idx] - distances[back_idx]
        elev_span = elevations_smoothed[forward_idx] - elevations_smoothed[back_idx]
        slope_percent = (elev_span / dist_span * 100) if dist_span > 0 else 0
    else:
        slope_percent = 0

    return slope_percent


def prepare_features(slope: float, cumulative_hours: float) -> Dict[str, float]:
    """
    Prepare feature dictionary for model prediction.

    Args:
        slope: Slope percentage
        cumulative_hours: Cumulative hiking time in hours

    Returns:
        Dictionary of features
    """
    features = {
        'slope': slope,
        'fatigue': cumulative_hours,
        'uphill': max(0, slope),
        'downhill': abs(min(0, slope)),
        'downhill_fatigue': abs(min(0, slope)) * cumulative_hours,
        'uphill_fatigue': max(0, slope) * cumulative_hours,
        'slope_squared': slope ** 2,
        'fatigue_squared': cumulative_hours ** 2,
    }
    return features


def predict_hike_time(gpx: gpxpy.gpx.GPX, model, feature_cols: list) -> Dict:
    """
    Predict hiking time for a GPX route.

    Args:
        gpx: Parsed GPX object
        model: Trained prediction model
        feature_cols: List of feature column names

    Returns:
        Dictionary with prediction results
    """
    # Extract points from GPX (support both tracks and routes)
    points = []

    # Extract from tracks
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation if point.elevation else 0,
                })

    # Extract from routes (if no tracks found)
    if len(points) == 0:
        for route in gpx.routes:
            for point in route.points:
                points.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation if point.elevation else 0,
                })

    if len(points) < 2:
        return {
            'success': False,
            'error': 'Route has too few points'
        }

    # Calculate distances
    distances = [0.0]
    elevations = [points[0]['elevation']]

    for i in range(1, len(points)):
        coord1 = (points[i-1]['latitude'], points[i-1]['longitude'])
        coord2 = (points[i]['latitude'], points[i]['longitude'])
        dist = geodesic(coord1, coord2).meters
        distances.append(distances[-1] + dist)
        elevations.append(points[i]['elevation'])

    distances = np.array(distances)
    elevations = np.array(elevations)

    # Smooth elevations
    elevations_smoothed = smooth_elevation(elevations, distances, window_m=100.0)

    # Calculate predictions for each segment
    segments = []
    cumulative_time_hours = 0

    for i in range(len(points) - 1):
        segment_distance_m = distances[i+1] - distances[i]

        if segment_distance_m < 1:
            continue

        # Calculate slope
        slope_percent = calculate_slope_window(elevations_smoothed, distances, i, window_m=100.0)

        # Prepare features
        features = prepare_features(slope_percent, cumulative_time_hours)
        X = pd.DataFrame([features])[feature_cols]

        # Predict speed
        predicted_speed_kmh = model.predict(X)[0]
        predicted_speed_kmh = max(0.5, predicted_speed_kmh)  # Minimum 0.5 km/h

        # Calculate time for this segment
        segment_time_hours = (segment_distance_m / 1000) / predicted_speed_kmh

        cumulative_time_hours += segment_time_hours

        segments.append({
            'distance_km': distances[i] / 1000,
            'elevation_m': elevations_smoothed[i],
            'slope_percent': slope_percent,
            'predicted_speed_kmh': predicted_speed_kmh,
            'cumulative_time_hours': cumulative_time_hours,
            'cumulative_distance_km': distances[i] / 1000,
        })

    # Calculate summary statistics
    total_distance_km = distances[-1] / 1000
    total_time_hours = cumulative_time_hours
    elevation_gain_m = sum(max(0, elevations_smoothed[i+1] - elevations_smoothed[i])
                          for i in range(len(elevations_smoothed) - 1))
    elevation_loss_m = sum(max(0, elevations_smoothed[i] - elevations_smoothed[i+1])
                          for i in range(len(elevations_smoothed) - 1))

    return {
        'success': True,
        'total_distance_km': total_distance_km,
        'total_time_hours': total_time_hours,
        'elevation_gain_m': elevation_gain_m,
        'elevation_loss_m': elevation_loss_m,
        'average_speed_kmh': total_distance_km / total_time_hours if total_time_hours > 0 else 0,
        'segments': segments,
    }
