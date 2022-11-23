# Payment_forms - Сервер, который создает платёжные формы для товаров

## Оглавление
- [Описание проекта](#description)
- [Используемые технологии](#technologies)
- [Установка и запуск проекта](#launch)

<a id=description></a>
## Описание проекта
Сервер создает платёжные формы для товаров для имитации и тестирования платежей, с помощью платёжной системы Stripe. 
Реализованы Django + Stripe API бэкенд со следующим функционалом:
- Django Модель Item с полями (name, description, price) 
- API с двумя методами:
    - GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe выполняется запрос stripe.checkout.Session.create(...) и полученный session.id выдавается в результате запроса
    - GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy происходит запрос на /buy/{id}, получение session_id и далее  с помощью JS библиотеки Stripe происходит редирект на Checkout форму stripe.redirectToCheckout(sessionId=session_id)
- Запуск используя Docker
- Использование environment variables(специально выгружены на github для тестирования)
- Просмотр Django Моделей в Django Admin панели
- Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items

---
<a id=technologies></a>
## Используемые технологии:
- Python 3.10
- Django 3.2
- Stripe
- Docker

<a id=launch></a>
## Установка и запуск проекта
### Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:V-pix/payment_forms.git
```
### Перейти в репозиторий в командной строке:
```bash
cd payment_forms
```
### Установить `docker` и `docker-compose`:
```bash
https://docs.docker.com/get-docker/
```
```bash
https://docs.docker.com/compose/
```
### Cоберите контейнер и запустите:
```bash
docker build -t payment_forms .
```
```bash
docker-compose up
```
### Выполните миграции:
```bash
docker-compose exec web python manage.py migrate
```
### Заполните тестовые данные:
```bash
docker-compose exec web python manage.py loaddata data.json
```

### Теперь проект доступен по адресам:
http://localhost:8000/ 

http://localhost:8000/admin/

### Учетная запись администратора
```sh
login: admin
password: 123
```