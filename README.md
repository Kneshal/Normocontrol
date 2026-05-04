# Название проекта

## Продакшен-сервер

- **IP-адрес:** 95.163.242.7
- **Домен:** (если есть — указать)
- **Пользователь для входа:** django / root (SSH по ключу)
- **Путь к проекту:** `/home/django/django_venv/src/`

## Быстрые команды (выполнять от пользователя django)

### Обновить сайт после изменений в репозитории
```
cd /home/django/django_venv/src/
git pull
source /home/django/django_venv/bin/activate
pip install -r requirements.txt   # если изменились зависимости
python manage.py migrate           # если изменились модели
python manage.py collectstatic     # если изменилась статика
sudo systemctl restart gunicorn
```

### Просмотр логов
```
# Логи Gunicorn (ошибки Django)
journalctl -u gunicorn -n 50 --no-pager

# Логи Nginx
tail -30 /var/log/nginx/error.log
```

### Перезапуск сервисов
```
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Технические детали
```
ОС: Ubuntu 20.04 / 22.04

Веб-сервер: Nginx

WSGI-сервер: Gunicorn

База данных: PostgreSQL

Виртуальное окружение: /home/django/django_venv/
```

### Важно
Файл с паролями и секретами (.env) хранится только на сервере, не в репозитории

SSH-ключ для доступа к серверу — у администратора

SSH-ключ для доступа к GitHub — сгенерирован на сервере, добавлен в GitHub как Deploy Key