# Full Project Report: MPNMJEC Smart Attendance System

## 1. Project Overview
The **MPNMJEC Smart Attendance System** is a modern, high-performance attendance tracking solution tailored for educational institutions. It combines automated facial recognition with a comprehensive administrative dashboard to manage students, faculty, and attendance records efficiently.

---

## 2. Technical Stack

### **Backend**
- **Framework**: FastAPI (Asynchronous Python)
- **Database**: PostgreSQL (hosted via Supabase)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **AI/ML**: InsightFace, ONNXRuntime, MediaPipe (Face Recognition & Detection)
- **Security**: JWT Authentication, Bcrypt password hashing
- **File Handling**: python-multipart, Zipfile (for exports)

### **Frontend**
- **Framework**: React 19 (Vite)
- **Routing**: React Router DOM 7
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **API Communication**: Axios
- **Vision Tasks**: @mediapipe/tasks-vision

---

## 3. System Architecture

### **3.1 Backend Architecture (`/backend`)**
The backend follows a modular monolith structure:
- **`main.py`**: The central engine containing API endpoints, business logic for attendance windows, and RBAC enforcement.
- **`models.py`**: Defines the relational schema including Users, Attendances, Face Embeddings, and Class Assignments.
- **`ai_service.py`**: Manages the loading of facial recognition models and provides embedding generation services.
- **`auth.py`**: Handles user login, token generation, and secure dependency injection for routes.
- **`database.py`**: Manages the connection pool to the Supabase PostgreSQL instance.

### **3.2 Frontend Architecture (`/frontend`)**
The frontend is designed as a responsive Single Page Application (SPA):
- **Pages**:
    - `KioskPage.jsx`: The automated attendance interface using the device camera.
    - `AttendancePage.jsx`: Manual attendance entry for staff.
    - `DashboardPage.jsx`: Analytics overview for admins and HODs.
    - `UsersPage.jsx`: Detailed management of student and staff profiles.
    - `SettingsPage.jsx`: Global configuration for holidays and session timings.
- **`api.js`**: A centralized Axios instance for interacting with the backend.

---

## 4. Database Schema Highlights

### **Core Tables**
1.  **Users**: Stores profiles for all roles (Admin, Student, Staff, etc.). Includes a `face_samples` JSON field for identity verification.
2.  **Embeddings**: Stores high-dimensional vector representations of users' faces for fast matching.
3.  **Attendance**: Records individual check-ins with date, time, session (Morning/Afternoon), and status (Present/Absent/Late).
4.  **StaffClassAssignments**: Maps faculty members to specific departments, years, and semesters.
5.  **Settings & CalendarRules**: Configures institutional schedules, holidays, and special events.

---

## 5. Key Features

### **5.1 Smart Attendance (Kiosk Mode)**
Using the `InsightFace` model, the system can detect faces in real-time, generate embeddings, and compare them against the database to mark attendance in seconds without user intervention.

### **5.2 Flexible Session Management**
- **Morning/Afternoon Sessions**: Supports configurable start and end times.
- **Staff vs. Student Windows**: Allows different attendance windows for employees and students.
- **Grace Periods**: Automatically marks late arrivals based on institutional settings.

### **5.3 Comprehensive Reporting**
- **Exporting**: Admins can export data as CSV or ZIP files.
- **Statistics**: Calculates attendance percentages by department, class, or individual.
- **Filtering**: Extensive filtering by date range, role, and department.

---

## 6. Deployment & Setup

### **Environment Configuration**
- **`.env`**: Stores sensitive data like `SUPABASE_DATABASE_URL` and `SECRET_KEY`.
- **`Dockerfile`**: Defines the containerized environment for the backend and frontend.

### **Running the System**
The project includes PowerShell scripts for easy local execution:
- `.\start-backend.ps1`: Initializes the Python venv and starts the FastAPI server.
- `.\start-frontend.ps1`: Installs NPM dependencies and launches the Vite dev server.

---

## 7. Security Features
- **CORS Protection**: Only authorized frontend origins (e.g., local dev or production domain) can access the API.
- **Role-Based Access (RBAC)**: Strict permission checks for every sensitive endpoint (e.g., only Admins can access `SettingsPage`).
- **Encrypted Storage**: No plain-text passwords; all sensitive staff data is hashed.

---
*Report generated on: 2026-05-07*
