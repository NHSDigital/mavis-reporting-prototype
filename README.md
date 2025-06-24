# Mavis Reporting Prototype

A Flask-based web application prototype for the commissioner reporting component of Mavis.

## Prerequisites

- Mise
- Make

## Installation

1. **Install Mise**

   Please see the main Mavis repository for [how to install mise](https://github.com/nhsuk/manage-vaccinations-in-schools?tab=readme-ov-file#mise).

   Once mise is installed, run the following command to install the project dependencies:

   ```bash
   mise install
   ```

2. **Install project dependencies**

   This will install the project dependencies using Poetry and NPM.

   Note that the Poetry virtual environment will be created in the `.venv` directory to allow IDEs to use the correct Python interpreter.

   ```bash
   make install
   ```

3. **Create an environment file**

   Create a `.env` file in the root of the project following the example provided in `.env.example`.

4. **Run the application in development mode**

   ```bash
   make dev
   ```

   The application will be available at `http://localhost:5000`.
