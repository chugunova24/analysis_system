Система учета и анализа данных
==============
***Содержание:***
- [Введение](#Introduction)
- [Стек технологий](#Technology-stack)
- [Запуск контейнеров](#Run-container)
- [Схема системы](#SchemaSystem)
- [Дополнительно: учетные данные PgAdmin4](#Addition-PgAdmin)
- [Спасибо за внимание!](#Thanks)


# Введение <a name="Introduction"></a>
analysis_system -  это система учета и анализа данных, поступающих с условного устройства. Полученные данные привязываются к временной метке и устройству, с которого пришли данные, и сохраняются в БД. Набор данных используется для дальнейшего анализа.

# Стек технологий <a name="Technology-stack"></a>

- Веб-фреймворк - [FastAPI](https://fastapi.tiangolo.com/)
- Очередь задач - [Celery](https://docs.celeryq.dev/en/stable/)
- Мониторинг Celery - [Flower](https://flower.readthedocs.io/en/latest/)
- Инструмент для управления зависимостями в Python - [Poetry](https://python-poetry.org/)
- Объектно-реляционная СУБД - [PostreSQL](https://www.postgresql.org/)
- NoSQL база данных в качестве брокера сообщений - [Redis](https://redis.io/)
- Графический интерфейс к PostgreSQL - [Pgadmin4](https://www.pgadmin.org/download/)
- Платформа для контейнеризации - [Docker](https://www.docker.com/)

# Запуск контейнеров <a name="Run-container"></a>
Предполагается, что у Вас уже установлен Docker, docker-compose. 

1. Склонируйте репозиторий на свой компьютер с помощью команды:
```
git https://github.com/chugunova24/analysis_system
```
2. Зайдите в папку проекта:
```
cd analysis_system
```
3. Выполните команду для сборки всех сервисов посредством Docker:

```
docker compose up -d
```

4. После завершения установки Вы сможете пройти по следующим адресам:
   

	|***Сервис*** | ***URL***| ***Метод*** |
	| --- | --- | --- |
	| Flower |  http://0.0.0.0:5555| - |
	| Pgadmin4 |  http://0.0.0.0:5050| - |
	| Статистика по конкретному (http)  |  http://0.0.0.0:8000/data/statistic?from_datetime=2024-03-12 13:00:00&to_datetime=2024-03-13 09:00:09&device_id=c72e53b4-84a7-4709-b78d-8bbfc467e2a0| GET |
	| Статистика за все время по всем устройствам (websocket) |  http://127.0.0.1:8000/data/realtime| GET |
	| Генерация устройства |  http://0.0.0.0:8000/data/device | POST |
	| Добавление тестовых данных |  http://0.0.0.0:8000/data/test_data | POST |
	| Проверка готовности сервера |  http://0.0.0.0:8000/ping | GET |
	| Документация API Swagger |  http://0.0.0.0:8888/docs | GET |


# Схема системы <a name="SchemaSystem"></a>

<p align="center">
<img src="https://github.com/chugunova24/analysis_system/blob/master/readme_img/schema_analysis_device.drawio.png" style="width:50%;height:50%"/>
</p>

# Дополнительно: учетные данные PgAdmin4 <a name="Addition-PgAdmin"></a>

1. | ***Параметр***| ***Значение*** |
	| --- | --- |
	| Логин |  admin@gmail.com |
	| Пароль |  123456 |
	| База данных |  gazprom_db |

# Спасибо за внимание! <a name="Thanks"></a>
<p align="center">
<img src="https://github.com/chugunova24/chugunova24/blob/main/giphy.gif" style="width:50%;height:50%"/>
</p>
