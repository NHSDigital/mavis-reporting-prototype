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

## Building & Running a Docker container

The application can be built and run via Docker, to support deployment.

**Build**

`make build-docker`

This will build a container image tagged with `mavis/reporting:latest`, which will listen on port 5000. To use a different tag, supply the `DOCKER_IMAGE` environment variable (e.g. `DOCKER_IMAGE=reporting-component:spike-11 make build-docker`)

Note that it will not push the image to any repository - you must do that manually if you want to.

**Run**

`make run-docker`

This will run the container image tagged with `mavis/reporting:latest` and listen on the host port 5000. 
To use a different tag, supply the `DOCKER_IMAGE` environment variable .
To map a different host port (for instance if you have something else running on port 5000) supply the `HOST_PORT` environment variable 

Example:

`DOCKER_IMAGE=reporting-component:spike-11 HOST_PORT=5001 make run-docker` will run the container image tagged with `reporting-component:spike-11` and map port 5001 on the host to port 5000 on the container.

You could then access the running app with http://localhost:5001 on your browser.

