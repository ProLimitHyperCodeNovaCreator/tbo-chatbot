#!/bin/bash

# TBO ChatBot Platform - Quick Start Script for Linux/Mac

set -e

echo ""
echo "================================================================================"
echo "    TBO CHATBOT PLATFORM - INTEGRATED TRAVEL BOOKING SYSTEM"
echo "================================================================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "[ERROR] Docker is not running. Please start Docker."
    exit 1
fi

echo "[INIT] Docker is running..."
echo ""

# Check if docker-compose file exists
if [ ! -f "docker-compose.yml" ]; then
    echo "[ERROR] docker-compose.yml not found in current directory."
    echo "Current directory: $(pwd)"
    exit 1
fi

echo "[INIT] Found docker-compose.yml"
echo ""

# Menu function
show_menu() {
    echo "================================================================================"
    echo "                           MENU OPTIONS"
    echo "================================================================================"
    echo "1. Start all services (docker-compose up --build)"
    echo "2. Stop all services (docker-compose down)"
    echo "3. View logs (docker-compose logs -f)"
    echo "4. Run integration tests"
    echo "5. Clean up volumes (WARNING: deletes data)"
    echo "6. Restart services"
    echo "7. Exit"
    echo "================================================================================"
    echo ""
}

while true; do
    show_menu
    read -p "Enter your choice (1-7): " choice
    
    case $choice in
        1)
            echo ""
            echo "[START] Building and starting all services..."
            echo "[INFO] This may take 5-10 minutes on first run..."
            echo ""
            docker-compose up --build
            ;;
        2)
            echo ""
            echo "[STOP] Stopping all services..."
            echo ""
            docker-compose down
            echo "[STOP] All services stopped."
            echo ""
            ;;
        3)
            echo ""
            echo "[LOGS] Streaming logs from all services (Ctrl+C to stop)..."
            echo ""
            docker-compose logs -f
            ;;
        4)
            echo ""
            echo "[TEST] Running integration test suite..."
            echo "[INFO] Waiting for services to be ready..."
            echo ""
            sleep 5
            python3 test_integration.py
            echo ""
            read -p "Press Enter to continue..."
            ;;
        5)
            echo ""
            echo "[WARNING] This will delete all Docker volumes and data!"
            read -p "Are you sure? (yes/no): " confirm
            if [ "$confirm" = "yes" ]; then
                echo "[CLEANUP] Removing containers and volumes..."
                docker-compose down -v
                echo "[CLEANUP] Complete."
            else
                echo "[CLEANUP] Cancelled."
            fi
            echo ""
            ;;
        6)
            echo ""
            echo "[RESTART] Restarting all services..."
            echo ""
            docker-compose restart
            echo "[RESTART] Services restarted."
            echo ""
            ;;
        7)
            echo ""
            echo "[EXIT] Goodbye!"
            echo ""
            exit 0
            ;;
        *)
            echo "[ERROR] Invalid choice. Please try again."
            echo ""
            ;;
    esac
done
