# 🛠️ my-django-starter

**A command-line utility for scaffolding and launching Django projects with a complete, modular, and automated setup pipeline.**

---

## 🚀 Overview

`my-django-starter` is a developer-friendly tool that automates the initial setup of Django projects. It handles everything from virtual environment creation to Django installation, project scaffolding, app setup, settings configuration, and server execution — all in one seamless command-line flow.

---

## 📦 Features

- 📁 Creates a new Django project and apps
- ⚙️  Sets up virtual environments automatically
- 🧪 Detects your OS and adjusts commands accordingly
- 📝 Configures settings, media files, environment variables
- 📄 Generates `requirements.txt`
- 📄 Manages environement variables
- 🧙 Renders a stylish home page template
- 👤 Creates a superuser for the admin dashboard
- 🚀 Launches the development server instantly

---

## 🔧 How It Works

The tool works through a **step-based pipeline** system:

Each setup task is a separate **module**:

- `Banner()` – Displays a welcome banner  
- `OSDetector()` – Detects the operating system  
- `VirtualEnvCreator()` – Creates a Python virtual environment  
- `DjangoInstaller()` – Installs Django via `pip`  
- `ProjectCreator()` – Scaffolds a new Django project  
- `AppCreator()` – Adds one or more Django apps  
- `SettingsModifier()` – Updates project settings  
- `EnvManager()` – Creates and populates a `.env` file  
- `RequirementsGenerator()` – Freezes dependencies  
- `HomePageRenderer()` – Adds a responsive landing page  
- `MediaFileHandler()` – Configures media/static paths  
- `MigrationManager()` – Applies database migrations  
- `AdminSetup()` – Creates an admin superuser  
- `ServerRunner()` – Launches the Django development server  

---

## ⚙️ Usage
```bash
$ pip install my-django-starter

$ mydjango
```

It will:

1. Create a new virtual environment  
2. Install Django  
3. Scaffold your project and apps  
4. Configure everything (settings, env, admin)  
5. Launch your Django server  

---

## 📜 License

MIT License
