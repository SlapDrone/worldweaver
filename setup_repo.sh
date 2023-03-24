#!/bin/bash

# Create directories
mkdir -p app/{core,models,api/endpoints,services} tests

# Create core configuration file
touch app/core/config.py

# Create model files
touch app/models/{image.py,music.py}

# Create service files
touch app/services/{ai.py,image.py,music.py}

# Create API endpoint files
touch app/api/endpoints/{images.py,music.py}

# Create main application file
touch app/main.py

# Create test files
touch tests/{test_image_generation.py,test_music_generation.py}
