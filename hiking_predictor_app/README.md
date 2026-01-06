# Hiking Time Predictor Web App

A Reflex-based web application that predicts hiking times from GPX files using your personalized speed model.

## Features

- **GPX File Upload**: Upload GPX track files from your local computer
- **Time Prediction**: Get personalized hiking time estimates based on your trained model
- **Interactive Visualizations**:
  - Distance over time progression
  - Speed and elevation profile

## Prerequisites

- **For Docker (Recommended)**:
  - Docker and Docker Compose installed
  - Your trained hiking speed model (`hiking_speed_model.pkl`) in the `data/` directory
  - GPX files from your GPS device or tracking app

- **For Local Development**:
  - Python 3.10 or higher
  - Your trained hiking speed model (`hiking_speed_model.pkl`) in the `data/` directory
  - GPX files from your GPS device or tracking app

## Quick Start with Docker (Recommended)

The easiest way to run the app is using Docker:

```bash
cd hiking_predictor_app
./build_and_run.sh
```

This will:
1. Build the Docker image
2. Start the container
3. Make the app available at `http://localhost:3000`

### Docker Commands

**Build and start:**
```bash
docker-compose up -d --build
```

**Stop the app:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

**Check status:**
```bash
docker-compose ps
```

**Rebuild after changes:**
```bash
docker-compose up -d --build
```

## Local Development (Without Docker)

If you prefer to run without Docker:

1. Navigate to the app directory:
```bash
cd hiking_predictor_app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure your model file is in the correct location:
```
hiking_predictor_app/data/hiking_speed_model.pkl
```

4. Initialize the Reflex app (first time only):
```bash
reflex init
```

5. Run the development server:
```bash
reflex run
```

6. Open your browser to `http://localhost:3000`

## Usage

1. **Open the App**: Navigate to `http://localhost:3000` in your browser

2. **Upload GPX File**:
   - Click "Select GPX File" or drag and drop a GPX file
   - GPX files can be exported from:
     - GaiaGPS (gaiagps.com)
     - Strava
     - Garmin Connect
     - AllTrails
     - Most GPS devices and hiking apps

3. **Analyze**: Click "Analyze Route" to process the GPX file

4. **View Results**: See your predictions including:
   - Estimated hiking time
   - Distance and elevation statistics
   - Speed and elevation profiles
   - Distance over time progression

5. **Upload Another**: Click "← Upload New Route" to analyze a different GPX file

## How It Works

The app:
1. Accepts GPX file uploads from your local computer
2. Parses the GPX data to extract track points with coordinates and elevation
3. Applies the same data cleaning and processing as your Jupyter notebook:
   - Smooths elevation data (100m window)
   - Calculates slope over 100m windows
   - Accounts for fatigue based on cumulative hiking time
4. Uses your trained gradient boosting model to predict speed at each segment
5. Visualizes the results with interactive charts

## Model Features

The prediction model considers:
- **Terrain slope** (uphill/downhill)
- **Fatigue** (cumulative hiking time)
- **Interaction effects** (how fatigue affects performance on slopes)
- **Non-linear relationships** (quadratic terms)

## Troubleshooting

### Model not found
Ensure `hiking_speed_model.pkl` exists at:
`hiking_predictor_app/data/hiking_speed_model.pkl`

### GPX file upload fails
- Ensure the file is a valid GPX format (XML-based)
- Check that the GPX file contains track data (not just waypoints)
- Verify the file includes elevation data for best results

### Prediction errors
- Ensure your GPX file has sufficient data points
- Check that elevation data is present in the GPX file
- Verify the model file is properly trained and not corrupted

## Getting GPX Files

### From GaiaGPS:
1. Login to gaiagps.com
2. Navigate to your route/track
3. Click "Export" and select "GPX" format
4. Download the file to your computer

### From Strava:
1. Login to strava.com
2. Go to your activity
3. Click the three dots menu → Export GPX
4. Download the file

### From Garmin Connect:
1. Login to connect.garmin.com
2. Select your activity
3. Click the gear icon → Export Original
4. Download the GPX file

### From AllTrails:
1. Login to alltrails.com
2. View your recorded hike
3. Click "Export" → GPX
4. Download the file

## Development

To modify the app:
- `hiking_predictor_app.py` - Main UI components and state management
- `model_utils.py` - Model loading and prediction logic

## Docker Deployment Details

### What's Included

The Docker setup includes:
- **Multi-stage build** for optimized image size
- **Persistent data storage** for the application database
- **Volume mounting** for the trained model
- **Network isolation** for security
- **Auto-restart** on failures
- **Non-root user** for enhanced security

### Ports

- `3000` - Frontend (web UI)
- `8000` - Backend API

### Volumes

- `./data` - Contains the trained model file
- Database is stored inside the container

### Environment Variables

You can customize the deployment by editing `docker-compose.yml`:

```yaml
environment:
  - REFLEX_DEPLOY_URL=http://0.0.0.0:3000
  - PYTHONUNBUFFERED=1
```

### User Permissions

The Docker container runs as a non-root user matching your host UID/GID to avoid permission issues:

```yaml
build:
  args:
    USER_ID: ${UID:-1000}
    GROUP_ID: ${GID:-1000}
```

## Production Deployment

For production deployment with Docker:

1. Ensure the model file is in place
2. Build and run with docker-compose:
```bash
docker-compose up -d --build
```

For other deployment options (without Docker), see the [Reflex deployment docs](https://reflex.dev/docs/hosting/deploy/).
