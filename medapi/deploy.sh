#!/bin/bash

# Simple deployment script for the Medical Personal Account API

# Colors for better readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Medical Personal Account API Deployment Script${NC}"
echo "----------------------------------------------"

case "$1" in
  start)
    echo -e "${GREEN}Starting the application with SQLite database...${NC}"
    docker-compose up -d
    echo -e "${GREEN}Application started! Access it at http://localhost:8000${NC}"
    echo -e "${GREEN}API documentation available at http://localhost:8000/docs${NC}"
    ;;
  
  start-postgres)
    echo -e "${GREEN}Starting the application with PostgreSQL database...${NC}"
    docker-compose -f docker-compose.postgres.yml up -d
    echo -e "${GREEN}Application started! Access it at http://localhost:8000${NC}"
    echo -e "${GREEN}API documentation available at http://localhost:8000/docs${NC}"
    ;;

  stop)
    echo -e "${YELLOW}Stopping the application...${NC}"
    docker-compose down
    echo -e "${GREEN}Application stopped.${NC}"
    ;;
  
  logs)
    echo -e "${YELLOW}Showing logs...${NC}"
    docker-compose logs -f
    ;;
  
  rebuild)
    echo -e "${YELLOW}Rebuilding the application...${NC}"
    docker-compose build --no-cache
    echo -e "${GREEN}Rebuild complete. Use './deploy.sh start' to start the application.${NC}"
    ;;

  *)
    echo -e "${RED}Usage: $0 {start|start-postgres|stop|logs|rebuild}${NC}"
    echo ""
    echo "Commands:"
    echo "  start          - Start the application with SQLite database"
    echo "  start-postgres - Start the application with PostgreSQL database"
    echo "  stop           - Stop the application"
    echo "  logs           - Show application logs"
    echo "  rebuild        - Rebuild the Docker image"
    exit 1
esac

exit 0
