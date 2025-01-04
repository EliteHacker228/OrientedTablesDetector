import os

import cv2
import numpy as np
from ultralytics import YOLO


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


def detect_objects(model, image_path, output_path, output_path_rot):
    img = cv2.imread(image_path)
    results = model(img)
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

    rotated_image = get_rotated_image(img, angle_to_rot)
    cv2.imwrite(output_path, annotated_img)
    cv2.imwrite(output_path_rot, rotated_image)


model = YOLO("models/pubtab_1548_aug.pt")
allowed_extensions = ["jpg", "jpeg", "png"]
for image_name in os.listdir("images"):
    image_name_parts = image_name.split(".")
    if image_name_parts[-1] not in allowed_extensions:
        continue
    input_path = f"images/{image_name}"
    output_path = f"results/{image_name}"
    output_path_rot = f"results/{image_name_parts[0] + '_rot.' + image_name_parts[1]}"
    print("#########################")
    print(f"results/{image_name}")
    detect_objects(model, input_path, output_path, output_path_rot)
