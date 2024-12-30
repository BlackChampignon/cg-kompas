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
<br>

## Usage
### For API testing:
1. http://localhost:8000/api/  → Json array of all Events
2. http://localhost:8000/api/1/   → Any number instead of 1 to get specific event det's
### DB testing (work in progress)
http://localhost:8000/
Working actions:
1. User register
2. User login
3. User delete
4. All categories
5. Add category
6. Modify a category
7. List of all events (work in progress)
8. Add an event
9. Delete an event
