from unittest.mock import MagicMock

import numpy as np
import pytest
from locust import HttpUser, between, task
from model_ood import detect_objects, get_angle_to_rot_from_result, get_rotated_image


# --- Модульные тесты (Unit Tests) ---
def test_get_angle_to_rot_from_result():
    """Проверяет вычисление угла поворота из результата OBB."""
    mock_obb = MagicMock()
    mock_obb.xywhr = np.array([[0, 0, 10, 20, np.pi / 4]])

    angle = get_angle_to_rot_from_result(mock_obb)
    expected_angle = 45.0
    assert angle == expected_angle, f"Ожидалось {expected_angle}, но получено {angle}"


def test_get_rotated_image():
    """Проверяет вращение изображения на заданный угол."""
    img = np.zeros((100, 200, 3), dtype=np.uint8)
    angle = 45.0
    rotated_img = get_rotated_image(img, angle)

    assert (
        rotated_img.shape[:2] != img.shape[:2]
    ), "Размеры изображения должны измениться после поворота."


# --- Интеграционные тесты (Integration Tests) ---
def test_detect_objects_with_mock_model():
    """Проверяет взаимодействие между функциями обнаружения объектов."""
    mock_model = MagicMock()
    mock_model.return_value = [
        MagicMock(obb=[MagicMock(xywhr=np.array([[0, 0, 10, 20, np.pi / 6]]))])
    ]

    original_model = detect_objects.__globals__["model"]
    detect_objects.__globals__["model"] = mock_model

    try:
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        angle_to_rot, annotated_img, rotated_image = detect_objects(img)

        assert angle_to_rot == 30.0, "Ожидалось значение угла 30.0 градусов."
        assert (
            annotated_img is not None
        ), "Аннотированное изображение должно быть создано."
        assert rotated_image is not None, "Повернутое изображение должно быть создано."
    finally:
        detect_objects.__globals__["model"] = original_model


# --- Регрессионные тесты (Regression Tests) ---
@pytest.mark.parametrize(
    "obb_data,expected_angle",
    [
        (np.array([[0, 0, 10, 20, np.pi / 6]]), 30.0),
        (np.array([[0, 0, 15, 25, np.pi / 4]]), 45.0),
    ],
)
def test_regression_get_angle_to_rot(obb_data, expected_angle):
    """Проверяет стабильность результатов вычисления угла поворота."""
    mock_obb = MagicMock()
    mock_obb.xywhr = obb_data

    angle = get_angle_to_rot_from_result(mock_obb)
    assert angle == expected_angle, f"Ожидалось {expected_angle}, но получено {angle}"


# --- Приемочные тесты (Acceptance Tests) ---
def test_acceptance_detect_objects():
    """Проверяет, что функция корректно обрабатывает изображение и ошибки."""
    img = np.zeros((100, 100, 3), dtype=np.uint8)

    try:
        angle_to_rot, annotated_img, rotated_image = detect_objects(img)
        assert isinstance(
            angle_to_rot, float
        ), "Угол должен быть числом с плавающей точкой."
        assert isinstance(
            annotated_img, np.ndarray
        ), "Аннотированное изображение должно быть массивом."
        assert isinstance(
            rotated_image, np.ndarray
        ), "Повернутое изображение должно быть массивом."
    except Exception as e:
        pytest.fail(f"Произошла ошибка: {e}")


# --- Нагрузочные тесты (Load Tests) ---


class LoadTestUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def predict_task(self):
        img_data = np.zeros((100, 100, 3), dtype=np.uint8).tolist()
        self.client.post("/detect", json={"image": img_data})


# --- Параметризованные тесты ---
@pytest.mark.parametrize(
    "image_shape",
    [
        (100, 100, 3),
        (200, 200, 3),
        (50, 150, 3),
    ],
)
def test_prediction_with_various_images(image_shape):
    """Проверяет функцию detect_objects на изображениях различных размеров."""
    img = np.zeros(image_shape, dtype=np.uint8)
    angle_to_rot, annotated_img, rotated_image = detect_objects(img)

    assert isinstance(
        angle_to_rot, float
    ), "Угол должен быть числом с плавающей точкой."
    assert isinstance(
        annotated_img, np.ndarray
    ), "Аннотированное изображение должно быть массивом."
    assert isinstance(
        rotated_image, np.ndarray
    ), "Повернутое изображение должно быть массивом."
