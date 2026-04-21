import asyncio
import os

from PIL import Image

from src.db import async_session_maker_null_pool
from src.tasks.celery_app import celery_inst
from src.utils.db_manager import DBManager


@celery_inst.task
def test_task():
    print("Hello from the test task!")


# @celery_inst.task
def resize_image(image_path: str):
    """A task that compresses a photo to a size of px.
    Processed photos are saved to the output_folder."""

    sizes = [1000, 500, 200]
    output_folder = "src/static/images"

    # Открываем изображение
    img = Image.open(image_path)

    # Получаем имя файла и его расширение
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    # Проходим по каждому размеру
    for size in sizes:
        # Сжимаем изображение
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS
        )

        # Формируем имя нового файла
        new_file_name = f"{name}_{size}px{ext}"

        # Полный путь для сохранения
        output_path = os.path.join(output_folder, new_file_name)

        # Сохраняем изображение
        img_resized.save(output_path)

    print(f"Photo compressed to sizes: {sizes} in folder {output_folder}")


async def get_bookings_with_today_checkin_helper():
    print("Starting task: get_bookings_with_today_checkin_helper")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_inst.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
