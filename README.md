# Python_project - Тренажер решеток Браве
Проект "Разработка Web-приложения на Django" по дисциплине "Python для решения прикладных задач". Веб-приложение для изучения 14 решеток Браве.

## Назначение проекта

Приложение позволяет:
- Изучать 14 решеток Браве в удобной табличной форме
- Проверять знания с помощью квиза
- Тренировать узнавание решеток по изображениям

## Инструкция по запуску (вариант, которым пользуюсь я)

Скопировать проект

git clone https://github.com/ВАШ_АККАУНТ/bravais-lattice-trainer.git

cd bravais-lattice-trainer

Создать виртуальное окружение:

python -m venv venv

venv\Scripts\activate

Установить

pip install django pillow

Создать и заполнить БД (заполнять только для первого запуска)

python manage.py makemigrations

python manage.py migrate

python add_lattices.py

Запустить сервер

python manage.py runserver

Открыть в браузере
http://127.0.0.1:8000/

## Автор

Живетьев Кирилл Витальевич, группа М02-510н_iPhD
