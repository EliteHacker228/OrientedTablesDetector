import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
from zipfile import ZipFile

from model_ood import detect_objects
from image_processing import prepare_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:4200", "http://localhost:80"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Model server is running"}


@app.post("/upload")
async def upload_image_file(upload_file: UploadFile = File(...)):
    file_content = await upload_file.read()
    file_like = BytesIO(file_content)
    image = Image.open(file_like).convert("RGB")

    angle_to_rot, annotated_img, rotated_image = detect_objects(image)
    # if angle_to_rot == 0:
    #     angle_to_rot = 'No oriented bounding boxes detected.'

    # Подготовка ZIP-архива
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, "w") as zip_file:
        # Добавляем аннотированное изображение
        annotated_image_bytes = prepare_image(annotated_img)
        zip_file.writestr("annotated_image.png", annotated_image_bytes.getvalue())

        # Добавляем повернутое изображение
        rotated_image_bytes = prepare_image(rotated_image)
        zip_file.writestr("rotated_image.png", rotated_image_bytes.getvalue())

    zip_buffer.seek(0)

    # Возвращаем ZIP-архив
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=images.zip",
            # Значение, на которое повёрнуто изображение (на сколько оно отлично от прямого угла)
            "Angle": str(-angle_to_rot),
            # значение, на которое нужно повернуть изображение, чтобы оно встало под прямым углом
            "Angle-To-Rot": str(angle_to_rot),
        },
    )


if __name__ == "__main__":
    uvicorn.run(app="main:app")
