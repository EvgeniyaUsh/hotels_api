import os
from PIL import Image
from src.tasks.celery_app import celery_inst


@celery_inst.task
def main_task():
    print("Hello from the main task!")

@celery_inst.task
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
