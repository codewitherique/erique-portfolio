# Erique Developer Portfolio (Django + PostgreSQL + Jazzmin)


```

## 2. Project setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # then edit SECRET_KEY and DB_PASSWORD
python manage.py makemigrations core
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```
Site: http://127.0.0.1:8000/  Admin: http://127.0.0.1:8000/admin/
Secret key: `python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"`

## 3. Managing content
Profile, photo, education, skills, projects, referees, messages, SEO and the hide-referees switch are all edited in the admin.

## 4. Production (Ubuntu VPS) outline
1. `sudo apt install python3-venv postgresql nginx certbot python3-certbot-nginx`
2. Create the DB as above, clone repo, set `.env` with `DEBUG=False` and your domain in `ALLOWED_HOSTS`.
3. `python manage.py collectstatic --noinput && python manage.py migrate`
4. Run Gunicorn as a systemd service: `gunicorn config.wsgi:application --bind unix:/run/erique.sock`
5. Nginx: proxy to the socket, serve `/media/` from the `media/` folder, pass `X-Forwarded-Proto`.
6. HTTPS: `sudo certbot --nginx -d yourdomain.com`
7. Backups: `pg_dump -U erique_user erique_db > backup.sql` and `tar czf media.tgz media/`

## Not yet included
Automated tests, sitemap, project filtering, Docker files.
