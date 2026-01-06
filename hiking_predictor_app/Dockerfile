FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Node.js and git
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    nodejs \
    npm \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user to run the application
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g ${GROUP_ID} nico && \
    useradd -m -u ${USER_ID} -g nico nico

# Copy requirements first for better caching
COPY hiking_predictor_app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY hiking_predictor_app/rxconfig.py .
COPY hiking_predictor_app/hiking_predictor_app/ ./hiking_predictor_app/

# Copy the trained model from the data directory
RUN mkdir -p ./data/
COPY hiking_predictor_app/data/hiking_speed_model.pkl ./data/hiking_speed_model.pkl

# Initialize Reflex
RUN reflex init

# Change ownership of the app directory to nico user
RUN chown -R nico:nico /app

# Switch to non-root user
USER nico

# Expose ports
# 3000 for frontend
# 8000 for backend API
EXPOSE 3000 8000

# Set environment variables
ENV REFLEX_DEPLOY_URL=http://0.0.0.0:3000
ENV PYTHONUNBUFFERED=1

# Run the application
# Note: Using --loglevel debug to see what's happening
CMD ["reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0", "--backend-port", "8000", "--loglevel", "debug"]
