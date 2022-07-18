
# Tilkku
#### Situational Awareness tool for Scouting events
Built for the 2022 FinnJamboree

---
## Installation

### Prerequisites
- Docker
- Docker Compose

### Setup
- Clone the repository
- Copy the file example.env to .env
- Edit the .env file to match your environment
- Run `docker-compose up -d --build`
- Open the browser and navigate to http://hostname:8001/
- You should see the application running

### Environment
The environment is defined in the .env file. All values in this table are mandatory.

|Key | Value|
|--- | ---|
HOST_NAME | The actual hostname of the server.
TIME_ZONE | The timezone of the server.
POSTGRES_USER | The username for the Postgres database.
POSTGRES_PASSWORD | The password for the Postgres database.
POSTGRES_DB | The name of the Postgres database.
POSTGRES_HOST | The hostname of the Postgres database. (default: tilkku_postgres)
ADMIN_USER | The username for the admin account.
ADMIN_PASS | The password for the admin account.
ADMIN_EMAIL | The email address for the admin account.
DJANGO_KEY | The secret key for the Django application. Generate new one!
HOME_LAT | The latitude of the home location.
HOME_LON | The longitude of the home location.
HOME_ZOOM | The zoom level of the home location.
GRID_LAT | The latitude of the grid top left corner location.
GRID_LON | The longitude of the grid top left corner location.
GRID_SIZE | The size of one grid square in meters.
GRID_COLS | The number of columns in the grid.
GRID_ROWS | The number of rows in the grid.
|--- | ---|

The DJANGO_KEY is used to encrypt the session cookies. You can generate a new one by running `openssl rand --base64 128`. DO NOT USE the one on the example!

---
&copy; 2022 Risto Lievonen