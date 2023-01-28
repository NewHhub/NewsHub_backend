# Установка 
## Загрузка проекта и виртуального окружения
Для загрузки проекта необходимо скачать его с github 
```commandline
git clone https://github.com/Qetu987/NewsHub_backend.git
```
после создать виртуальное окружение
- для unix систем
```commandline
python3 -m venv venv 
source venv/bin/activate
```
- для win
```commandline
python -m venv venv 
venv\Scripts\activate
```

## Установка необходимых билиотек
для корректной работы необходимо установить в виртуальное окружение все необходимые библиотеки 
- для unix систем
```commandline
pip3 install -r requarements.txt
```
- для win
```commandline
pip install -r requarements.txt
```

## создание супер-юзера 
после скачивания репозитория, база уже будет установленна, нужно добавть суперпользователя для админки
```commandline
python manage.py createsuperuser
```
После чего вводим данные для пользователя (пароль при вводе отображаться не будет)

## Создание стилей 
так как в проекте используется scss, для создания стиле необходимо их скомпилить (исходная [папка](./static/scss) конечная [папка](./static/css))

## Запуск проекта 
Для запуска необходимо запустить локальный сервер
```commandline
python manage.py runserver
```