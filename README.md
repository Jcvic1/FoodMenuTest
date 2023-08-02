# FoodMenuTest

1. clone repository or download zip.

2. create an environment and install requirements.txt (optional).

3. create .env file in parent folder and add

  DATABASE_PORT=5432
  POSTGRES_USER={POSTGRES_USER}
  POSTGRES_PASSWORD={POSTGRES_PASSWORD}
  POSTGRES_HOST={POSTGRES_HOST}
  POSTGRES_DB={POSTGRES_DB}
  POSTGRES_HOSTNAME=db

4. Run docker-compose up --build to build image, start db, run test and show test results in terminal.
