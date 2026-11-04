"""Точка входа приложения Prompt Generator 98.

Исправлены синтаксические ошибки: `from __future__ import annotations`
и `if __name__ == "__main__":`. Отступы выровнены по PEP 8 (4 пробела).
Логика, комментарии и докстринги сохранены без изменений.
"""

from __future__ import annotations

import sys

from models import AppState, PromptSettings, Style
from prompt_engine import PromptEngine
from ui import MainWindow


def bootstrap() -> MainWindow:
    """Создаёт состояние приложения и главное окно."""
    state = AppState()
    state.settings = PromptSettings(
        system_prompt="Отвечай кратко.",
        user_prompt="",
        style=Style.RETRO,
    )
    window = MainWindow(state)
    return window


def main(argv: list[str] | None = None) -> int:
    """Основная функция: запускает демо-генерацию из CLI."""
    argv = sys.argv[1:] if argv is None else argv
    window = bootstrap()
    if argv:
        window.state.settings.user_prompt = " ".join(argv)
    else:
        window.state.settings.user_prompt = "Привет!"
    window.engine = PromptEngine(window.state.settings)
    result = window.on_generate()
    print(result.text)
    print(f"Статус: {window.status}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
