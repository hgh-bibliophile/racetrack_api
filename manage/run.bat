set DATABASE_URL=$(heroku config:get DATABASE_URL -a racetrack-api | %{$_ -replace "postgres:","postgresql:"})
uvicorn main:app --reload