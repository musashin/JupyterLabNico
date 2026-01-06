#!/bin/bash

# Build and run the Hiking Predictor app using Docker

set -e

echo "🏔️  Building Hiking Predictor Docker container..."

# Build the Docker image
sudo docker-compose build

echo "✅ Build complete!"
echo ""
echo "🚀 Starting the application..."

# Start the container
sudo docker-compose up -d

echo ""
echo "✅ Application started!"
echo ""
echo "📊 Access the app at: http://localhost:3000"
echo ""
echo "Useful commands:"
echo "  View logs:        sudo docker-compose logs -f"
echo "  Stop app:         sudo docker-compose down"
echo "  Rebuild & start:  sudo docker-compose up -d --build"
echo "  Check status:     sudo docker-compose ps"
echo ""
