"""UI-модуль приложения (Win98-стиль).

QSS-строка WIN98_QSS намеренно не трогаем — она будет добавлена
в отдельном шаге. Здесь исправлены только синтаксические ошибки:
dunder-имена и отступы по PEP 8 (4 пробела).
"""

from __future__ import annotations

import datetime

from models import AppState, GenerationResult, HistoryEntry, PromptSettings
from prompt_engine import PromptEngine

# WIN98_QSS — стилизация в духе Windows 98. Все опечатки исправлены:
# закрытые комментарии */, color, selection-background-color, border-color,
# margin, solid, width, цвета #FFFFFF/#000080/#808080 без разрывов,
# шрифты без висячих пробелов, объект TitleLabel.
WIN98_QSS = """
/* ---------------- Global ---------------- */
QWidget {
    font-family: "MS Sans Serif", "Tahoma", "Arial";
    font-size: 11px;
    background-color: #C0C0C0;
    color: #000000;
}

/* ---------------- Menu bar ---------------- */
QMenuBar {
    background-color: #C0C0C0;
    border-color: #808080;
    margin: 2px;
}

QMenuBar::item {
    padding: 4px 8px;
    background: transparent;
}

QMenuBar::item:selected {
    background-color: #000080;
    color: #FFFFFF;
}

/* ---------------- Push button ---------------- */
QPushButton {
    background-color: #C0C0C0;
    border: 2px solid;
    border-color: #FFFFFF #808080 #808080 #FFFFFF;
    margin: 2px;
    padding: 4px 12px;
    min-width: 75px;
}

QPushButton:pressed {
    border-color: #808080 #FFFFFF #FFFFFF #808080;
}

/* ---------------- Line edit ---------------- */
QLineEdit {
    background-color: #FFFFFF;
    border: 2px solid;
    border-color: #808080 #FFFFFF #FFFFFF #808080;
    selection-background-color: #000080;
    selection-color: #FFFFFF;
    margin: 2px;
    padding: 2px;
    height: 20px;
}

/* ---------------- Labels ---------------- */
QLabel {
    background: transparent;
}

QLabel#TitleLabel {
    font-size: 16px;
    font-weight: bold;
    color: #000080;
}

/* ---------------- Group box ---------------- */
QGroupBox {
    border: 2px solid;
    border-color: #FFFFFF #808080 #808080 #FFFFFF;
    margin: 4px;
    padding-top: 8px;
}

/* ---------------- Scroll area ---------------- */
QScrollBar:vertical {
    background-color: #C0C0C0;
    border: 1px solid #808080;
    width: 16px;
    margin: 0px;
}
"""


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
