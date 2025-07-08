# 🛠️ Sistema de Notas Técnicas - Reparación de PCs

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3-black?style=for-the-badge&logo=flask)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4-47A248?style=for-the-badge&logo=mongodb)
![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker)

Una aplicación web desarrollada con **Python y Flask** para gestionar y documentar el proceso de reparación de equipos informáticos. La aplicación permite registrar los detalles de cada equipo, adjuntar fotografías y generar automáticamente un **informe técnico en formato PDF** con un diseño institucional.

## ✨ Características Principales

-   **📝 Registro de Informes:** Formulario web intuitivo para capturar todos los datos relevantes del equipo.
-   **🖼️ Carga de Imágenes:** Permite adjuntar múltiples fotografías del equipo para un registro visual completo.
-   **📄 Generación de PDF:** Crea automáticamente un informe técnico en PDF con los datos registrados y el logo institucional.
-   **💾 Persistencia de Datos:** Utiliza **MongoDB** para almacenar todos los informes de manera segura.
-   **🐳 Dockerizado:** Totalmente configurado para ser desplegado fácilmente con **Docker y Docker Compose**.
-   **📜 Historial de Informes:** Visualiza, edita y elimina informes previos desde una tabla de historial.

---

## 🚀 Tecnologías Utilizadas

-   **Backend:** Python 3.11, Flask
-   **Base de Datos:** MongoDB
-   **Generación de PDF:** WeasyPrint (o la librería que estés usando)
-   **Contenerización:** Docker, Docker Compose
-   **Frontend:** HTML, CSS, Bootstrap 5, Jinja2

---

## 📦 Estructura del Proyecto

```
pc-repair-docs/
├── app/
│   ├── __init__.py         # Inicialización de la app Flask
│   ├── routes.py           # Definición de rutas y lógica
│   ├── models.py           # Conexión a la base de datos
│   ├── utils/              # Funciones de utilidad (generador de PDF, helpers)
│   └── templates/          # Plantillas HTML
├── static/
│   ├── images/             # Logo institucional
│   ├── uploads/            # (Ignorado por Git) Fotos subidas
│   └── pdf/                # (Ignorado por Git) PDFs generados
├── .env.example            # Plantilla para variables de entorno
├── .gitignore              # Archivos y carpetas a ignorar por Git
├── Dockerfile              # Instrucciones para construir la imagen de la app
├── docker-compose.yml      # Orquestación de servicios (app y mongo)
├── requirements.txt        # Dependencias de Python
└── run.py                  # Punto de entrada para ejecutar la aplicación
```

---

## ⚙️ Guía de Instalación y Despliegue (con Docker)

Sigue estos pasos para levantar el proyecto en tu entorno local.

### Prerrequisitos

-   Tener [Docker](https://www.docker.com/get-started) y [Docker Compose](https://docs.docker.com/compose/install/) instalados.
-   Tener Git instalado.

### Pasos

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd pc-repair-docs
    ```

2.  **Configurar el logo institucional:**
    Coloca el logo de tu institución en la siguiente ruta. El archivo debe llamarse `logo_unsa.png` o ajustar el nombre en las plantillas HTML.
    ```
    static/images/logo_unsa.png
    ```

3.  **Crear el archivo de entorno:**
    Copia el archivo de ejemplo para crear tu configuración local. Los valores por defecto son correctos para el entorno de Docker Compose.
    ```bash
    cp .env.example .env
    ```

4.  **Construir y levantar los contenedores:**
    Este comando construirá la imagen de Flask y levantará los servicios de la aplicación y la base de datos en segundo plano (`-d`).
    ```bash
    docker-compose up --build -d
    ```

5.  **¡Listo! Acceder a la aplicación:**
    Abre tu navegador web y ve a la siguiente dirección:
    > **http://localhost:5000**

### Comandos útiles de Docker Compose

-   **Para detener los contenedores:**
    ```bash
    docker-compose down
    ```
-   **Para ver los logs de la aplicación en tiempo real:**
    ```bash
    docker-compose logs -f app
    ```