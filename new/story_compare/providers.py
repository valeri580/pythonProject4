from __future__ import annotations

import base64
import os
import uuid
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class GenResult:
    provider: str
    ok: bool
    text: str
    error: Optional[str] = None


def _norm_bool_env(name: str, default: bool = True) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return str(raw).strip().lower() not in {"0", "false", "no", "off"}


def generate_openai_story(prompt: str) -> GenResult:
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    if not api_key:
        return GenResult("openai", False, "", "OPENAI_API_KEY не задан")

    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "Ты создаёшь вдохновляющие сторис короткой формы."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.9,
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"].strip()
        return GenResult("openai", True, text)
    except Exception as e:  # noqa: BLE001
        return GenResult("openai", False, "", str(e))


def _giga_basic_from_env() -> Optional[str]:
    auth_b64 = os.getenv("AUTHORIZATION_KEY")
    if auth_b64:
        auth_b64 = auth_b64.strip().strip('"')
        if auth_b64:
            return f"Basic {auth_b64}"
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    if client_id and client_secret:
        raw = f"{client_id}:{client_secret}".encode("utf-8")
        return "Basic " + base64.b64encode(raw).decode("utf-8")
    return None


def _giga_get_token(scope: str) -> str:
    oauth_url = os.getenv("GIGACHAT_OAUTH_URL", "https://ngw.devices.sberbank.ru:9443/api/v2/oauth")
    auth_header = _giga_basic_from_env()
    if not auth_header:
        raise RuntimeError("Не заданы AUTHORIZATION_KEY или CLIENT_ID/CLIENT_SECRET для GigaChat")
    resp = requests.post(
        oauth_url,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": auth_header,
        },
        data={"scope": scope},
        timeout=30,
    )
    resp.raise_for_status()
    token = resp.json().get("access_token")
    if not token:
        raise RuntimeError("GigaChat: access_token не получен")
    return token


def generate_gigachat_story(prompt: str) -> GenResult:
    scope = os.getenv("SCOPE", "GIGACHAT_API_PERS")
    model = os.getenv("GIGACHAT_MODEL", "GigaChat")

    try:
        force_refresh = os.getenv("GIGACHAT_ALWAYS_REFRESH_TOKEN", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        token = _giga_get_token(scope) if force_refresh else (os.getenv("ACCESS_TOKEN") or _giga_get_token(scope))
    except Exception as e:  # noqa: BLE001
        return GenResult("gigachat", False, "", f"Ошибка токена: {e}")

    try:
        resp = requests.post(
            "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "Ты создаёшь вдохновляющие сторис короткой формы."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.9,
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"].strip()
        return GenResult("gigachat", True, text)
    except Exception as e:  # noqa: BLE001
        return GenResult("gigachat", False, "", str(e))


def generate_yandex_story(prompt: str) -> GenResult:
    api_key = os.getenv("YANDEX_API_KEY")
    iam_token = os.getenv("YC_IAM_TOKEN")
    folder_id = os.getenv("YANDEX_FOLDER_ID")
    model = os.getenv("YANDEX_MODEL", "gpt://{folder_id}/yandexgpt-lite")
    if (not api_key and not iam_token) or not folder_id:
        return GenResult("yandex", False, "", "YANDEX_API_KEY или YC_IAM_TOKEN и YANDEX_FOLDER_ID не заданы")

    # Приводим модель
    if "{folder_id}" in model:
        model = model.replace("{folder_id}", folder_id)

    try:
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {"Content-Type": "application/json", "x-folder-id": folder_id}
        if iam_token:
            headers["Authorization"] = f"Bearer {iam_token}"
        else:
            headers["Authorization"] = f"Api-Key {api_key}"
        resp = requests.post(
            url,
            headers=headers,
            json={
                "modelUri": model,
                "completionOptions": {"temperature": 0.9, "maxTokens": 500},
                "messages": [
                    {"role": "system", "text": "Ты создаёшь вдохновляющие сторис короткой формы."},
                    {"role": "user", "text": prompt},
                ],
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        alt = data.get("result", {}).get("alternatives", [])
        text = (alt[0].get("message", {}).get("text") if alt else "").strip()
        if not text:
            raise RuntimeError("Yandex: пустой ответ")
        return GenResult("yandex", True, text)
    except Exception as e:  # noqa: BLE001
        return GenResult("yandex", False, "", str(e))


