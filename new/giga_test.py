import base64
import os
import sys
import uuid
from pathlib import Path

import requests
from dotenv import load_dotenv


def build_basic_auth_from_env() -> str:
    auth_b64 = os.getenv("AUTHORIZATION_KEY")
    if auth_b64:
        return f"Basic {auth_b64.strip()}"

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError(
            "Отсутствуют CLIENT_ID и/или CLIENT_SECRET, и не задан AUTHORIZATION_KEY"
        )
    raw = f"{client_id}:{client_secret}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("utf-8")


def main() -> int:
    # Загружаем .env, лежащий рядом с этим файлом (new/.env)
    dotenv_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(dotenv_path=dotenv_path, override=True)

    url = os.getenv(
        "GIGACHAT_OAUTH_URL",
        "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
    )
    scope = os.getenv("SCOPE", "GIGACHAT_API_PERS")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
        "Authorization": build_basic_auth_from_env(),
    }
    payload = {"scope": scope}

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=30)
        response.raise_for_status()
    except requests.exceptions.SSLError as ssl_err:
        print(
            "SSL ошибка. Убедитесь, что установлен корневой сертификат Минцифры (мы уже ставили через gigachain)."
        )
        print(f"Детали: {ssl_err}")
        return 1
    except requests.RequestException as req_err:
        print(f"HTTP ошибка: {req_err}")
        if req_err.response is not None:
            print(req_err.response.text)
        return 1

    data = response.json()
    access_token = data.get("access_token")
    token_type = data.get("token_type")
    expires_at = data.get("expires_at") or data.get("expires_in")

    if not access_token:
        print("Не удалось получить access_token. Ответ:")
        print(data)
        return 2

    # Печатаем токен и служебную информацию
    print(access_token)
    if token_type:
        print(f"token_type={token_type}")
    if expires_at:
        print(f"expires={expires_at}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
