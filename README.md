
# DeepFace NiceGUI Access Control

A local Desktop Face Recognition application built with **Python**, **NiceGUI** (Web-based UI), and **DeepFace**.
The application mimics a Windows 11 style interface and provides secure access control via Face Recognition or PIN.

## Features

- **Face Recognition**: Real-time detection and identification using DeepFace (Facenet model).
- **Windows 11 UI**: Clean, modern interface with "Mica" style background and responsive cards.
- **Dual Authentication**: 
  - **Biometric**: Automatic face login.
  - **PIN Fallback**: Manual entry for failed conditions.
- **Role-Based Access**:
  - **Admin**: Full access to User Dashboard (Add/Delete users).
  - **User/Visitante**: Access only to authorized areas (Login confirmation).
- **Modular Architecture**: Built with maintainability in mind (Service-Controller-View pattern).

## Installation

1.  **Clone/Download** the repository.
2.  **Create a Virtual Environment** (Optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    pip install nicegui deepface opencv-python
    ```
    *(Note: `requirements.txt` might need updating depending on your env)*

## Usage

Simply run the startup script:

```bash
./run_app.sh
```

Or manually:

```bash
source venv/bin/activate
python3 main.py
```

### First Run
If the database (`users.db`) is empty, the app will redirect you to the **Setup Page**.
1. Enter the Admin Name and PIN.
2. Position yourself in front of the camera.
3. Click **"Criar Sistema"**.

## Project Structure

```
src/
  common/       # Shared resources
    config.py   # App constants
    database.py # SQLite CRUD
    state.py    # Global AppState
    theme.py    # UI Styles
  features/     # Core Logic
    inferencia/ # DeepFace Engine
  pages/        # UI Pages
    login.py    # Landing Page
    dashboard.py# Admin Panel
    setup.py    # First-run Setup
services.py     # Dependency Injection (Singletons)
main.py         # Application Entry Point
```
