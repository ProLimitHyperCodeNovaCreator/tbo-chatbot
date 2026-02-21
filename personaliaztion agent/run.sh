#!/bin/bash

show_menu() {
    clear
    echo "========================================"
    echo "  Personalization Agent"
    echo "========================================"
    echo ""
    echo "  1. Setup  (install deps + DB schema)"
    echo "  2. Start Server  (requires DB)"
    echo "  3. Run Mock Tests  (no DB needed)"
    echo "  4. Exit"
    echo ""
    read -rp "Choose an option (1-4): " choice
}

do_setup() {
    clear
    echo "[Setup] Checking .env..."
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "Created .env from template."
        echo ""
        echo " IMPORTANT: Edit .env and set DATABASE_URL, then run Setup again."
        read -rp "Press Enter to return to menu..."
        return
    fi

    echo "[Setup] Installing dependencies..."
    pip install -r requirements.txt || { echo "ERROR: pip failed."; read -rp "Press Enter..."; return; }

    echo "[Setup] Generating Prisma client..."
    prisma generate --schema=app/prisma/schema.prisma || { echo "ERROR: prisma generate failed."; read -rp "Press Enter..."; return; }

    echo "[Setup] Pushing DB schema..."
    prisma db push --schema=app/prisma/schema.prisma || { echo "ERROR: prisma db push failed."; read -rp "Press Enter..."; return; }

    echo "[Setup] Seeding sample data..."
    python setup_db.py

    echo ""
    echo "Setup complete. Run option 2 to start the server."
    read -rp "Press Enter to return to menu..."
}

do_server() {
    clear
    echo "[Server] Starting on http://localhost:8000"
    echo "Press CTRL+C to stop."
    echo ""
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    read -rp "Press Enter to return to menu..."
}

do_mock() {
    clear
    echo "[Mock Tests] Running without database..."
    echo ""
    cd mock_testing && python test_standalone.py
    cd ..
    read -rp "Press Enter to return to menu..."
}

while true; do
    show_menu
    case "$choice" in
        1) do_setup ;;
        2) do_server ;;
        3) do_mock ;;
        4) exit 0 ;;
        *) echo "Invalid choice."; sleep 1 ;;
    esac
done
