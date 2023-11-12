# Django-Quotes
An application for managing quotes and authors. Based on Postgres + Alembic.

1) User can singup and login into his own account.
2) Unauthenticated user can view quotes and authors.
3) Only authenticated user can add quotes, tags and authors.
4) Tags are unqiue for each user, quotes and authors are not.

5) It is possible to use /scrap to scrap a website (only for superuser). It runs bs4 scrapper script.

**Example:** 127.0.0.1:8000/scrap/quotes.toscrape.com+quotes.toscrape.com_login+admin+admin

**Template:** ../scrap/<target_link>+<login_link>+<username>+<password>

_It is not quite safe to send credentials in the headers though, so it is made for training purposes only._

6) Each author and tag has its own page.

7) It is possible to reset password for the user.
8) Verification email is sent after the signup.


## Usage:

- docker run --name noteapp-postgres -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres
- cd quotes
- python manage.py runserver
