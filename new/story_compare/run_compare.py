import os
from pathlib import Path

from dotenv import load_dotenv

from .providers import (
    GenResult,
    generate_gigachat_story,
    generate_openai_story,
    generate_yandex_story,
)


def save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def summarize(results: list[GenResult]) -> str:
    lines: list[str] = []
    for r in results:
        status = "OK" if r.ok else "FAIL"
        lines.append(f"{r.provider}: {status}")
    oks = [r for r in results if r.ok]
    if oks:
        # Простая эвристика: длина ответа как прокси качества
        best = max(oks, key=lambda x: len(x.text))
        lines.append(f"Лучший по длине ответа: {best.provider}")
    return "\n".join(lines)


def main() -> int:
    # Грузим .env из корня проекта, затем локальный рядом (если есть)
    load_dotenv()
    # Также пробуем подхватить переменные из new/.env (для GigaChat и прочих)
    from pathlib import Path as _P
    new_env = _P(__file__).resolve().parent.parent / ".env"
    if new_env.exists():
        # Не перезаписываем уже заданные переменные окружения
        load_dotenv(new_env, override=False)
    local_env = Path(__file__).resolve().parent / ".env"
    if local_env.exists():
        load_dotenv(local_env, override=False)

    prompt = os.getenv(
        "STORY_PROMPT",
        "Сделай вдохновляющую сторис о том, как начать утро продуктивно.",
    )

    out_dir = Path(os.getenv("STORY_OUT", "new/story_compare/output"))

    results: list[GenResult] = []

    for fn in (generate_openai_story, generate_yandex_story, generate_gigachat_story):
        res = fn(prompt)
        results.append(res)
        file_name = f"{res.provider}.txt"
        if res.ok:
            save_text(out_dir / file_name, res.text)
        else:
            save_text(out_dir / f"{res.provider}.error.txt", res.error or "unknown error")

    report = summarize(results)
    save_text(out_dir / "report.txt", report)
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


