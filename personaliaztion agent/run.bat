@echo off
title Personalization Agent

:menu
cls
echo ========================================
echo   Personalization Agent
echo ========================================
echo.
echo   1. Setup  (install deps + DB schema)
echo   2. Start Server  (requires DB)
echo   3. Run Mock Tests  (no DB needed)
echo   4. Exit
echo.
set /p choice="Choose an option (1-4): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto server
if "%choice%"=="3" goto mock
if "%choice%"=="4" exit /b
echo Invalid choice. Try again.
pause
goto menu

:: ----------------------------------------
:setup
cls
echo [Setup] Checking .env...
if not exist .env (
    copy .env.example .env >nul
    echo Created .env from template.
    echo.
    echo  IMPORTANT: Edit .env and set DATABASE_URL, then run Setup again.
    pause
    goto menu
)

echo [Setup] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 ( echo ERROR: pip failed. & pause & goto menu )

echo [Setup] Generating Prisma client...
prisma generate --schema=app/prisma/schema.prisma
if errorlevel 1 ( echo ERROR: prisma generate failed. & pause & goto menu )

echo [Setup] Pushing DB schema...
prisma db push --schema=app/prisma/schema.prisma
if errorlevel 1 ( echo ERROR: prisma db push failed. & pause & goto menu )

echo [Setup] Seeding sample data...
python setup_db.py

echo.
echo Setup complete. Run option 2 to start the server.
pause
goto menu

:: ----------------------------------------
:server
cls
echo [Server] Starting on http://localhost:8000
echo Press CTRL+C to stop.
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
goto menu

:: ----------------------------------------
:mock
cls
echo [Mock Tests] Running without database...
echo.
cd mock_testing
python test_standalone.py
cd ..
pause
goto menu
