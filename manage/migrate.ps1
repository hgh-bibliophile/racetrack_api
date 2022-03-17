param(
    [Parameter()]
    [String]$commit
)

$env:DATABASE_URL=$(heroku config:get DATABASE_URL -a racetrack-api) -replace "postgres:", "postgresql:"

alembic -n sqlite revision --autogenerate -m $commit
alembic -n sqlite upgrade head
alembic -n postgresql revision --autogenerate -m $commit
alembic -n postgresql upgrade head
