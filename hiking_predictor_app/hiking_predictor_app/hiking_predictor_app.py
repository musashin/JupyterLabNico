"""
Hiking Time Predictor - Reflex Web Application
Upload GPX files to predict hiking times using a trained ML model.
"""

import reflex as rx
from typing import List, Dict, Optional
import plotly.graph_objects as go
from pathlib import Path
import gpxpy
import gpxpy.gpx

from .model_utils import load_model, predict_hike_time


class State(rx.State):
    """Application state management."""

    # File upload
    uploaded_files: List[str] = []
    current_gpx_name: str = ""

    # Prediction results
    prediction_results: Optional[Dict] = None
    is_loading: bool = False
    error_message: str = ""

    def get_model_data(self) -> tuple:
        """Load the trained hiking speed model."""
        if not hasattr(State, '_model_data_instance'):
            # Look for model in data directory
            model_path = Path(__file__).parent.parent / "data" / "hiking_speed_model.pkl"

            if model_path.exists():
                model, feature_cols = load_model(str(model_path))
                if model is None:
                    self.error_message = "Failed to load prediction model"
                    State._model_data_instance = (None, None)
                else:
                    State._model_data_instance = (model, feature_cols)
            else:
                self.error_message = f"Model not found at {model_path}"
                State._model_data_instance = (None, None)
        return State._model_data_instance

    @rx.var
    def formatted_time(self) -> str:
        """Format predicted time as 'Xh Ym'."""
        if self.prediction_results is None:
            return "N/A"
        total_hours = self.prediction_results.get('total_time_hours', 0)
        hours = int(total_hours)
        minutes = int((total_hours % 1) * 60)
        return f"{hours}h {minutes}m"

    @rx.var
    def formatted_distance(self) -> str:
        """Format distance."""
        if self.prediction_results is None:
            return "N/A"
        return f"{self.prediction_results.get('total_distance_km', 0):.2f} km"

    @rx.var
    def formatted_speed(self) -> str:
        """Format average speed."""
        if self.prediction_results is None:
            return "N/A"
        return f"{self.prediction_results.get('average_speed_kmh', 0):.2f} km/h"

    @rx.var
    def formatted_elevation_gain(self) -> str:
        """Format elevation gain."""
        if self.prediction_results is None:
            return "N/A"
        return f"{self.prediction_results.get('elevation_gain_m', 0):.0f} m"

    @rx.var
    def distance_chart_data(self) -> go.Figure:
        """Generate distance over time chart."""
        fig = go.Figure()

        if self.prediction_results and 'segments' in self.prediction_results:
            segments = self.prediction_results['segments']
            times = [seg['cumulative_time_hours'] for seg in segments]
            distances = [seg['cumulative_distance_km'] for seg in segments]

            fig.add_trace(go.Scatter(
                x=times,
                y=distances,
                mode='lines',
                name='Distance',
                line=dict(color='#3b82f6', width=3),
            ))

        fig.update_layout(
            xaxis_title="Time (hours)",
            yaxis_title="Distance (km)",
            hovermode='x unified',
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
        )

        return fig

    @rx.var
    def speed_elevation_chart_data(self) -> go.Figure:
        """Generate speed and elevation profile chart."""
        fig = go.Figure()

        if self.prediction_results and 'segments' in self.prediction_results:
            segments = self.prediction_results['segments']
            distances = [seg['cumulative_distance_km'] for seg in segments]
            speeds = [seg['predicted_speed_kmh'] for seg in segments]
            elevations = [seg['elevation_m'] for seg in segments]

            # Speed trace
            fig.add_trace(go.Scatter(
                x=distances,
                y=speeds,
                mode='lines',
                name='Speed (km/h)',
                line=dict(color='#10b981', width=2),
                yaxis='y',
            ))

            # Elevation trace
            fig.add_trace(go.Scatter(
                x=distances,
                y=elevations,
                mode='lines',
                name='Elevation (m)',
                line=dict(color='#6366f1', width=2),
                fill='tozeroy',
                fillcolor='rgba(99, 102, 241, 0.2)',
                yaxis='y2',
            ))

        fig.update_layout(
            xaxis_title="Distance (km)",
            yaxis=dict(
                title=dict(text="Speed (km/h)", font=dict(color="#10b981")),
                tickfont=dict(color="#10b981"),
            ),
            yaxis2=dict(
                title=dict(text="Elevation (m)", font=dict(color="#6366f1")),
                tickfont=dict(color="#6366f1"),
                overlaying='y',
                side='right',
            ),
            hovermode='x unified',
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
        )

        return fig

    async def handle_upload(self, files: List[rx.UploadFile]):
        """Handle GPX file upload."""
        self.is_loading = True
        self.error_message = ""
        self.prediction_results = None

        if not files:
            self.error_message = "No file uploaded"
            self.is_loading = False
            return

        # Process the first file
        upload_file = files[0]
        self.uploaded_files = [upload_file.filename]
        self.current_gpx_name = upload_file.filename

        # Read the file content
        try:
            upload_data = await upload_file.read()
            gpx_content = upload_data.decode('utf-8')

            # Parse GPX
            gpx = gpxpy.parse(gpx_content)

            # Make prediction
            model, feature_cols = self.get_model_data()
            if model is None or feature_cols is None:
                self.error_message = "Prediction model not loaded"
                self.is_loading = False
                return

            results = predict_hike_time(gpx, model, feature_cols)

            if results.get('success'):
                self.prediction_results = results
            else:
                self.error_message = results.get('error', 'Prediction failed')

        except Exception as e:
            self.error_message = f"Error processing GPX file: {str(e)}"

        self.is_loading = False

    def clear_and_upload_new(self):
        """Clear results and upload a new file."""
        self.uploaded_files = []
        self.current_gpx_name = ""
        self.prediction_results = None
        self.error_message = ""


def upload_page() -> rx.Component:
    """File upload page component."""
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("Hiking Time Predictor", size="8"),
                rx.text("Upload a GPX file to predict hiking time", color="gray"),
                rx.callout(
                    rx.vstack(
                        rx.text("Supported file format:", weight="bold"),
                        rx.unordered_list(
                            rx.list_item("GPX files (.gpx) with track data"),
                            rx.list_item("Files should contain elevation data for best results"),
                        ),
                        spacing="2",
                    ),
                    icon="info",
                    color_scheme="blue",
                    size="1",
                ),
                rx.upload(
                    rx.vstack(
                        rx.button(
                            "Select GPX File",
                            color_scheme="blue",
                            size="3",
                        ),
                        rx.text(
                            "Drag and drop or click to select",
                            size="2",
                            color="gray",
                        ),
                        spacing="2",
                    ),
                    id="upload1",
                    border="1px dashed #CBD5E0",
                    padding="2em",
                    width="100%",
                    accept={".gpx": ["application/gpx+xml", "text/xml"]},
                ),
                rx.cond(
                    State.error_message != "",
                    rx.callout(
                        State.error_message,
                        icon="triangle_alert",
                        color_scheme="red",
                        role="alert",
                    ),
                ),
                rx.button(
                    "Analyze Route",
                    on_click=State.handle_upload(rx.upload_files(upload_id="upload1")),
                    loading=State.is_loading,
                    width="100%",
                    size="3",
                ),
                spacing="4",
                width="600px",
            ),
        ),
        height="100vh",
    )


def prediction_view() -> rx.Component:
    """Prediction results view."""
    return rx.vstack(
        rx.hstack(
            rx.button(
                "← Upload New Route",
                on_click=State.clear_and_upload_new,
                variant="soft",
            ),
            rx.spacer(),
            width="100%",
            padding="4",
        ),
        rx.heading(State.current_gpx_name, size="8"),
        rx.cond(
            State.is_loading,
            rx.spinner(size="3"),
            rx.cond(
                State.prediction_results != None,
                rx.vstack(
                    # Summary cards
                    rx.hstack(
                        rx.card(
                            rx.vstack(
                                rx.text("Predicted Time", size="2", color="gray"),
                                rx.heading(
                                    State.formatted_time,
                                    size="7",
                                ),
                                align="start",
                            ),
                        ),
                        rx.card(
                            rx.vstack(
                                rx.text("Distance", size="2", color="gray"),
                                rx.heading(
                                    State.formatted_distance,
                                    size="7",
                                ),
                                align="start",
                            ),
                        ),
                        rx.card(
                            rx.vstack(
                                rx.text("Avg Speed", size="2", color="gray"),
                                rx.heading(
                                    State.formatted_speed,
                                    size="7",
                                ),
                                align="start",
                            ),
                        ),
                        rx.card(
                            rx.vstack(
                                rx.text("Elevation Gain", size="2", color="gray"),
                                rx.heading(
                                    State.formatted_elevation_gain,
                                    size="7",
                                ),
                                align="start",
                            ),
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    # Visualizations
                    rx.card(
                        rx.vstack(
                            rx.heading("Distance over Time", size="6"),
                            distance_time_chart(),
                            width="100%",
                        ),
                        width="100%",
                    ),
                    rx.card(
                        rx.vstack(
                            rx.heading("Speed and Elevation Profile", size="6"),
                            speed_elevation_chart(),
                            width="100%",
                        ),
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
            ),
        ),
        spacing="4",
        padding="8",
        width="100%",
        max_width="1400px",
        margin="0 auto",
    )


def distance_time_chart() -> rx.Component:
    """Chart showing cumulative distance over time."""
    return rx.plotly(data=State.distance_chart_data)


def speed_elevation_chart() -> rx.Component:
    """Chart showing speed and elevation profile."""
    return rx.plotly(data=State.speed_elevation_chart_data)


def index() -> rx.Component:
    """Main app component."""
    return rx.fragment(
        rx.cond(
            State.prediction_results != None,
            prediction_view(),
            upload_page(),
        ),
    )


# Create app
app = rx.App()
app.add_page(index, title="Hiking Time Predictor")
