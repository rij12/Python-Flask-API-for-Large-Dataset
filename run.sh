# Get Server data ready
unzip data/fake_profiles.zip -d data/

# Build Containers
docker-compose build

# Start server
docker-compose up
