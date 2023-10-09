# ДЗ
### Описание
пусто
### Инструкция по развертыванию проекта 
- Склонируйте репозиторий проекта
```bash
git clone git@gitlab.crja72.ru:django_2023/students/214610-the-pimp-47230.git
cd 214610-the-pimp-47230
```

- Создайте файл .env в корневой директории проекта и установите необходимые переменные окружения
```
DJANGO_SECRET_KEY = "secret"
DJANGO_DEBUG = True
DJANGO_ALLOWED_HOSTS = 127.0.0.1
```

### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
```
python3 -m pip install venv  
python3 -m venv venv
source venv/bin/activate
```

- Установите зависимости из файла requirements/dev.txt
```
pip install -r requirements/dev.txt
``` 
- В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```

###Запуск проекта в prod-режиме
- Установите и активируйте виртуальное окружение
```
python3 -m pip install venv
python3 -m venv venv
source venv/bin/activate
```
- Установите зависимости из файла requirements/prod.txt
```
pip install -r requirements/prod.txt
``` 

- При необходимости установите зависимости для тестов из requirements/test.txt
```
pip install -r requirements/test.txt
``` 

- В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```



