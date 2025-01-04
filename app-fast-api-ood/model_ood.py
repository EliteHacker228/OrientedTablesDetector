import os

import cv2
import numpy as np
from ultralytics import YOLO

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "models", "pubtab_1548_aug.pt")
file_path = os.path.abspath(file_path)
model = YOLO(file_path)


def get_angle_to_rot_from_result(obb):
    xywhr = obb.xywhr[0]
    x_center, y_center, width, height, rotation = xywhr
    angle_degrees = rotation.item() * (180 / np.pi)
    return round(angle_degrees, 2)


def get_rotated_image(img, angle_to_rot):
    height, width = img.shape[:2]
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle_to_rot, 1.0)

    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])

    new_w = int((height * sin) + (width * cos))
    new_h = int((height * cos) + (width * sin))

    rotation_matrix[0, 2] += new_w / 2 - center[0]
    rotation_matrix[1, 2] += new_h / 2 - center[1]

    return cv2.warpAffine(img, rotation_matrix, (new_w, new_h))


def detect_objects(image):
    image_np = np.array(image)

    # преобразование для черно-белого изображения
    if len(image_np.shape) == 2:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)

    results = model(image_np)
    annotated_img = results[0].plot()

    angle_to_rot = 0
    for result in results:
        if result.obb is not None and len(result.obb) != 0:
            angle_sum = 0
            for obb in result.obb:
                angle_sum += get_angle_to_rot_from_result(obb)
            # angle_to_rot - значение, на которое нужно повернуть изображение, чтобы оно встало под прямым углом
            angle_to_rot = angle_sum / len(result.obb)
            # Agle: - выводится значение, на которое повёрнуто изображение (на сколько оно отлично от прямого угла)
            print(f"Angle: {-angle_to_rot:.2f} degrees")
            print(f"Angle to rot: {angle_to_rot:.2f} degrees")
        else:
            print("No oriented bounding boxes detected.")

    rotated_image = get_rotated_image(image_np, angle_to_rot)
    return angle_to_rot, annotated_img, rotated_image
