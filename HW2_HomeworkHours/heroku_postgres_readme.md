+ Working with Postgres and Heroku
    + Install a [hobby-dev add-on](https://elements.heroku.com/addons/heroku-postgresql).
        + `heroku addons:create heroku-postgresql:hobby-dev -a your-app-name`
    + Dump your local database, copy to Heroku, and confirm ([ref](https://docs.forestadmin.com/documentation/how-tos/databases/populate-a-postgresql-database-on-heroku):
        + `PGPASSWORD=your-password pg_dump -h localhost -U your-username homework_users_db --no-owner --no-acl -f homework_users_db.dump`
        + `heroku pg:psql DATABASE_URL -a your-app-name < homework_users_db.dump`
        + `heroku logs -t -a your-app-name`
    + Troubleshoot in the [dev-center](https://devcenter.heroku.com/articles/heroku-postgresql).
    + Set environment variables as [configurations](https://devcenter.heroku.com/articles/config-vars) (keep in mind you can do this in your Heroku dashboard).
