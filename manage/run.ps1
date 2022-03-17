$env:DATABASE_URL=$(heroku config:get DATABASE_URL -a racetrack-api) -replace "postgres:", "postgresql:"
uvicorn main:app --reload