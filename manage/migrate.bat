set DATABASE_URL=$(heroku config:get DATABASE_URL -a racetrack-api | %{$_ -replace "postgres:","postgresql:"})

alembic -n sqlite revision --autogenerate -m %1
alembic -n sqlite upgrade head
alembic -n postgresql revision --autogenerate -m %1
alembic -n postgresql upgrade head
