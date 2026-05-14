Для миграций, если файла alembic.ini ещё нет, нужно запустить в терминале команду:

`alembic init migrations`

После этого будет создана папка с миграциями и конфигурационный файл для алембика.

* В alembic.ini нужно задать адрес базы данных, в которую будем катать миграции.
* Дальше идём в папку с миграциями и открываем env.py, там вносим изменения в блок, где написано
`from myapp import mymodel`
* Дальше вводим: `alembic revision --autogenerate -m "comment"` - делается при любых изменениях моделей
* Будет создана миграция
* Дальше вводим: `alembic upgrade heads`



docker network create myNetwork

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16

docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4

docker run --name booking_back \
    -p 7777:8000 \
    --network=myNetwork \
    booking_image


docker run --name booking_celery_worker \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO


docker run --name booking_celery_beat \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B


docker build -t booking_image .