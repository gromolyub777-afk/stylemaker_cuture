"""Модели данных приложения (эмуляция Win98-интерфейса).

Модуль содержит dataclass-модели и простые классы, описывающие
настройки генерации промптов. Логика не менялась — исправлены
только синтаксические ошибки (dunder-имена).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Style(Enum):
    """Перечисление поддерживаемых стилей генерации."""

    CLASSIC = "classic"
    MODERN = "modern"
    RETRO = "retro"


@dataclass
class PromptSettings:
    """Настройки одного промпта."""

    system_prompt: str = ""
    user_prompt: str = ""
    style: Style = Style.CLASSIC
    temperature: float = 0.7
    max_tokens: int = 512
    tags: List[str] = field(default_factory=list)

    def copy(self) -> "PromptSettings":
        """Возвращает поверхностную копию настроек."""
        return PromptSettings(
            system_prompt=self.system_prompt,
            user_prompt=self.user_prompt,
            style=self.style,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            tags=list(self.tags),
        )


class GenerationResult:
    """Результат генерации, возвращаемый движком промптов."""

    def __init__(self, text: str, settings: PromptSettings, ok: bool = True):
        self.text = text
        self.settings = settings
        self.ok = ok

    def __repr__(self) -> str:
        return (
            f"GenerationResult(ok={self.ok}, "
            f"text={self.text[:40]!r}...)"
        )


class HistoryEntry:
    """Одна запись истории генераций."""

    def __init__(self, timestamp: str, prompt: str, result: GenerationResult):
        self.timestamp = timestamp
        self.prompt = prompt
        self.result = result


class AppState:
    """Глобальное состояние приложения."""

    def __init__(self):
        self.settings = PromptSettings()
        self.history: List[HistoryEntry] = []

    def add_entry(self, entry: HistoryEntry) -> None:
        """Добавляет запись в историю."""
        self.history.append(entry)

    def last_result(self) -> GenerationResult | None:
        """Возвращает последний результат генерации или None."""
        if not self.history:
            return None
        return self.history[-1].result
