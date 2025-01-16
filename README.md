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
### Login and Registration:
1. Registration is done by sending a POST request to the following url
```http
    http://localhost:8000/api/register/
```
with the following mandatory data in json
```json
{
    "email": "user1@example.com",
    "password": "user123"
}
```

2. Login is performed by sending a POST request to the following url
```http
    http://localhost:8000/api/login/
```
with the following mandatory data in json
```json
{
    "email": "user1@example.com",
    "password": "user123"
}
```
Afterwards you get access_token and refresh_token (also in json)
### Getting the events with authentification token
Write a GET request to the following url
```http
    http://localhost:8000/api/aut/1/
```
containing the following json data:
```json
{
    "Authorization": "Bearer <access_token>"
}
```
Where instead of <access_token> you use the token which was received upon login 
