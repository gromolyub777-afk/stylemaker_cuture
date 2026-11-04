"""UI-модуль приложения (Win98-стиль).

QSS-строка WIN98_QSS намеренно не трогаем — она будет добавлена
в отдельном шаге. Здесь исправлены только синтаксические ошибки:
dunder-имена и отступы по PEP 8 (4 пробела).
"""

from __future__ import annotations

import datetime

from models import AppState, GenerationResult, HistoryEntry, PromptSettings
from prompt_engine import PromptEngine

# TODO: WIN98_QSS будет добавлен в отдельном шаге (не менять логику).


class MainWindow:
    """Главное окно приложения (без зависимости от Qt-библиотек)."""

    def __init__(self, state: AppState | None = None):
        self.state = state or AppState()
        self.engine = PromptEngine(self.state.settings)
        self.title = "Prompt Generator 98"
        self.status = "Готов"

    def on_generate(self) -> GenerationResult:
        """Обрабатывает нажатие кнопки «Генерировать»."""
        result = self.engine.generate()
        entry = HistoryEntry(
            timestamp=datetime.datetime.now().isoformat(timespec="seconds"),
            prompt=self.engine.build_full_prompt(),
            result=result,
        )
        self.state.add_entry(entry)
        self.status = "OK" if result.ok else "Пустой промпт"
        return result

    def update_settings(self, settings: PromptSettings) -> None:
        """Обновляет настройки движка."""
        self.state.settings = settings
        self.engine = self.engine.with_settings(settings)


class DialogWindow(MainWindow):
    """Диалоговое окно настроек."""

    def __init__(self, state: AppState | None = None):
        super().__init__(state)
        self.title = "Настройки"


def run() -> None:
    """Точка входа UI: создаёт окно и выполняет демо-генерацию."""
    window = MainWindow()
    window.state.settings.user_prompt = "Привет, мир!"
    window.on_generate()
    print(f"{window.title}: {window.status}")


if __name__ == "__main__":
    run()
