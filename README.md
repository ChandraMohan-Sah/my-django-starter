```console
   ____ ___  __  __      ____/ / (_)___ _____  ____ _____        _____/ /_____ ______/ /____  _____
  / __ `__ \/ / / /_____/ __  / / / __ `/ __ \/ __ `/ __ \______/ ___/ __/ __ `/ ___/ __/ _ \/ ___/
 / / / / / / /_/ /_____/ /_/ / / / /_/ / / / / /_/ / /_/ /_____(__  ) /_/ /_/ / /  / /_/  __/ /    
/_/ /_/ /_/\__,_/      \__,_/_/ /\__,_/_/ /_/\__, /\____/     /____/\__/\__,_/_/   \__/\___/_/     
         /____/           /___/            /____/
```

# 🛠️ my-django-starter

**A command-line utility for scaffolding and launching Django projects with a complete, modular, and automated setup pipeline.**



## 💻 [System Architecture : OOP Design](https://lucid.app/lucidchart/05ef5f18-8771-4bf5-98f9-a02179d64d49/edit?invitationId=inv_f47c4113-0103-46fb-a9a3-599e8f7245c8&page=0_0#)


## 🎥 [Live Demo](https://youtu.be/qYoUna9-jEw)

## 🚀 Overview

my-django-starter is a developer-friendly tool that automates the initial setup of Django projects. It handles everything from virtual environment creation to Django installation, project scaffolding, app setup, settings configuration, and server execution — all in one seamless command-line flow.



## 📦 Features

- 📁 Creates a new Django project and apps
- ⚙️ Sets up virtual environments automatically
- 🧪 Detects your OS and adjusts commands accordingly
- 📝 Configures settings, media files, environment variables
- 📄 Generates requirements.txt
- 📄 Manages environement variables
- 🧙 Renders a stylish home page template
- 👤 Creates a superuser for the admin dashboard
- 🚀 Launches the development server instantly

---

## 🔧 How It Works

The tool works through a **step-based pipeline** system:

Each setup task is a separate **module**:
- Banner() – Displays a welcome banner  
- OSDetector() – Detects the operating system  
- VirtualEnvCreator() – Creates a Python virtual environment  
- DjangoInstaller() – Installs Django via pip  
- ProjectCreator() – Scaffolds a new Django project  
- AppCreator() – Adds one or more Django apps  
- SettingsModifier() – Updates project settings  
- EnvManager() – Creates and populates a .env file  
- RequirementsGenerator() – Freezes dependencies  
- HomePageRenderer() – Adds a responsive landing page  
- MediaFileHandler() – Configures media/static paths  
- MigrationManager() – Applies database migrations  
- AdminSetup() – Creates an admin superuser  
- ServerRunner() – Launches the Django development server  

---

## ⚙️ Installation & Usage

### For Linux/macOS:
```bash
$ pip install my-django-starter==0.1.7  # replace with actual version
$ mydjango
```


### For Windows:
```bash
$ pip install my-django-starter==0.1.7  # replace with actual version
# Add mydjango.exe to PATH environment variable
$ mydjango
```

It will:

1. Creates a new virtual environment  
2. Install Django  
3. Scaffold your project and apps  
4. Configure everything (settings, env, admin)  
5. Creates a requirements.txt file 
6. Create a home page and render using home app 
7. Launch your Django server  



## Adding New App to Existing Django Project 

### For Linux/macOS:
```bash 
$ source myenv/bin/activate  # Activate your virtual environment
$ cd /path/to/your-django-project
$ mydjango-add-generalapp
```

### For Windows:
```bash 
$ myenv\Scripts\activate  # Activate your virtual environment
$ cd C:\path\to\your-django-project
$ mydjango-add-generalapp
```

It will:

1. Add new app to existing project
4. Configure everything (settings,urls)  
3. Adds templates and static folder inside each newly created app 




## 📜 License

MIT License
