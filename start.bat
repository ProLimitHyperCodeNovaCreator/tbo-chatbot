@echo off
REM TBO ChatBot Platform - Quick Start Script for Windows

SetLocal EnableDelayedExpansion

echo.
echo ================================================================================
echo     TBO CHATBOT PLATFORM - INTEGRATED TRAVEL BOOKING SYSTEM
echo ================================================================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo [INIT] Docker is running...
echo.

REM Check if docker-compose file exists
if not exist "docker-compose.yml" (
    echo [ERROR] docker-compose.yml not found in current directory.
    echo Current directory: %cd%
    pause
    exit /b 1
)

echo [INIT] Found docker-compose.yml
echo.

REM Offer menu
:menu
echo ================================================================================
echo                           MENU OPTIONS
echo ================================================================================
echo 1. Start all services (docker-compose up --build)
echo 2. Stop all services (docker-compose down)
echo 3. View logs (docker-compose logs -f)
echo 4. Run integration tests
echo 5. Clean up volumes (WARNING: deletes data)
echo 6. Restart services
echo 7. Exit
echo ================================================================================
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto start
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto logs
if "%choice%"=="4" goto test
if "%choice%"=="5" goto cleanup
if "%choice%"=="6" goto restart
if "%choice%"=="7" goto exit

echo [ERROR] Invalid choice. Please try again.
echo.
goto menu

:start
echo.
echo [START] Building and starting all services...
echo [INFO] This may take 5-10 minutes on first run...
echo.
docker-compose up --build
goto menu

:stop
echo.
echo [STOP] Stopping all services...
echo.
docker-compose down
echo [STOP] All services stopped.
echo.
goto menu

:logs
echo.
echo [LOGS] Streaming logs from all services (Ctrl+C to stop)...
echo.
docker-compose logs -f
goto menu

:test
echo.
echo [TEST] Running integration test suite...
echo [INFO] Waiting for services to be ready...
echo.
timeout /t 5 /nobreak
python test_integration.py
echo.
pause
goto menu

:cleanup
echo.
echo [WARNING] This will delete all Docker volumes and data!
set /p confirm="Are you sure? (yes/no): "
if "%confirm%"=="yes" (
    echo [CLEANUP] Removing containers and volumes...
    docker-compose down -v
    echo [CLEANUP] Complete.
) else (
    echo [CLEANUP] Cancelled.
)
echo.
goto menu

:restart
echo.
echo [RESTART] Restarting all services...
echo.
docker-compose restart
echo [RESTART] Services restarted.
echo.
goto menu

:exit
echo.
echo [EXIT] Goodbye!
echo.
exit /b 0
