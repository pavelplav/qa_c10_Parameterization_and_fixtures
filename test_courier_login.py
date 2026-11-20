import os

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


class TestCourierLogin:

    @pytest.mark.parametrize(
        "login_type, password_type, expected_status",
        [
            # TODO: добавьте минимум 3 набора данных.
            # Должны быть позитивные и негативные сценарии.
            #
            # Например:
             ("valid", "valid", 200),
             ("missing", "valid", 400),
             ("valid", "missing", 400),
             ("invalid", "invalid", 404),
        ],
    )
    def test_courier_login(
        self,
        courier,
        login_type,
        password_type,
        expected_status,
    ):
        
        payload = {}

        if login_type == "valid":
            payload["login"] = courier["login"]
        elif login_type == "missing":
            payload["login"] = ""
        elif login_type == "invalid":
            payload["login"] = "non_existent_user_999"
  

        if password_type == "valid":
            payload["password"] = courier["password"]
        elif password_type == "missing":
            payload["password"] = ""
        elif password_type == "invalid":
            payload["password"] = "wrong_password_999"

        response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            json=payload,
        )


        # TODO: проверьте ожидаемый статус ответа.
        assert response.status_code == expected_status


        response_data = response.json()

        if expected_status == 200:
            assert "id" in response_data and response_data["id"] is not None
        elif expected_status == 400:
            assert response_data.get("message") == "Недостаточно данных для входа"
        elif expected_status == 404:
            assert response_data.get("message") == "Учетная запись не найдена"

        