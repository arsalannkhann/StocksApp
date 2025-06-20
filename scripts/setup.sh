

set -e

echo "🚀 Setting up Stock Prediction Platform..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create environment file
if [ ! -f .env ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_warning "Please update .env file with your API keys before running the application"
fi

# Create directories
print_status "Creating necessary directories..."
mkdir -p logs
mkdir -p ml_models/saved_models
mkdir -p airflow/logs
mkdir -p monitoring/grafana/data

# Set permissions for Airflow
print_status "Setting up Airflow permissions..."
mkdir -p airflow/logs airflow/plugins
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > airflow/.env

# Build and start services
print_status "Building and starting all services..."
docker-compose up -d --build

# Wait for services
print_status "Waiting for services to start..."
sleep 30

print_status "🎉 Setup complete! Services are starting up..."
echo ""
echo "Access the application at:"
echo "📊 Frontend Dashboard: http://localhost:3000"
echo "🔧 Airflow UI: http://localhost:8080 (admin/admin123)"
echo "📈 Grafana: http://localhost:3001 (admin/admin123)"
echo "🔍 Prometheus: http://localhost:9090"
echo "🌐 API Health: http://localhost:5000/api/health"
echo ""
echo "To view logs: docker-compose logs -f [service-name]"
echo "To stop services: docker-compose down"
echo ""
print_warning "Remember to update your API keys in the .env file!"
