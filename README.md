Django-приложение для загрузки JSON-файлов, валидации и сохранения данных в PostgreSQL.  
Отображение данных реализовано с помощью DataTables.

1. Зависимости(на Linux/Debian 11+)

   В bash:
 ``` 
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx postgresql
```
2. Клонируйте репозиторий, создайте виртуальное окружение и установите необходимые проекту пакеты:
```
git clone https://github.com/mrdemonrush/pntj0245.git
cd pntj0245
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Настройте PostgreSQL:
```
 sudo -u postgres psql
 CREATE DATABASE parser_db;
 CREATE USER root WITH PASSWORD 'root';
 GRANT ALL PRIVILEGES ON DATABASE parser_db TO root;
 \q
```
4. Настройте связь Django и PostgreSQL в parser/settings.py:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'parser_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

5. Сделайте миграцию:
```
   python manage.py migrate
```

6. Запустите gunicorn из корня проекта:
```
   gunicorn parser.wsgi:application --bind 127.0.0.1:8001 --workers 3
```

7. Настройте nginx: создайте конфиг в /etc/nginx/sites-available/parser:
```
   server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
 }
```

8. Активируйте сайт(в случае возникновения ошибки File exists - все правильно):
```
 sudo ln -s /etc/nginx/sites-available/parser /etc/nginx/sites-enabled/
 sudo nginx -t
 sudo systemctl restart nginx
```

9. Все готово, переходите по localhost или 127.0.0.1:8001. В случае неправильной страницы по localhost, удалите дефолтный конфиг(nginx/sites-enabled/default) и перезапустите nginx снова.
