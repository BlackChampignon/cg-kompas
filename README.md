# CG Kompas
An app for API calls and DB maintenance
<br>
## Installation:
### 0. Choose your project folder in cmd
   ```sh
   cd your_project_folder
   ```
### 1. Clone the repo
   ```sh
   git clone https://github.com/BlackChampignon/cg-kompas.git
   ```
### 2. Download Docker Desktop
  <a href="https://www.docker.com/">Download</a>
### 3. Complete the Docker installation and register\login

<br>
## Running the server
### 0. Go into your folder in cmd
   ```sh
   cd your_project_folder/cg-kompas
   ```
### 1. Verify that your files are up-to-date
   ```sh
   git pull
   ```
### 2. Build the image and run the container:
  ```sh
   docker-compose up
   ```

<br>
## Quitting
### 1. Stop the Django server
   Use <b>Ctrl + C</b> in cmd where the containers are run
### 2. Remove the containers
  ```sh
   docker-compose down
   ```
