param(
    [Parameter()]
    [String]$commit
)

$env:DATABASE_URL=$(heroku config:get DATABASE_URL -a racetrack-api) -replace "postgres:", "postgresql:"
$env:DATABASE_URL='postgresql://racetrack_io_user:uGJaU5y7FFdXA0H4nk1sTasCoHA8bnCZ@dpg-cftt399a6gdotc8h893g-a.oregon-postgres.render.com/racetrack_io_7ik0'

alembic -n sqlite revision --autogenerate -m $commit
alembic -n sqlite upgrade head
alembic -n postgresql revision --autogenerate -m $commit
alembic -n postgresql upgrade head
