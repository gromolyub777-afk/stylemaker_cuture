"""Движок промптов: сборка финального промпта из настроек.

Исправлены только синтаксические ошибки (dunder-имена, отступы).
Логика, комментарии и докстринги сохранены без изменений.
"""

from __future__ import annotations

from typing import List

from models import GenerationResult, PromptSettings, Style

# Префиксы стилей, добавляемые к системному промпту.
STYLE_PREFIXES = {
    Style.CLASSIC: "Ты — классический ассистент.",
    Style.MODERN: "Ты — современный ассистент.",
    Style.RETRO: "Ты — ретро-ассистент в стиле Windows 98.",
}


class PromptEngine:
    """Собирает промпты и возвращает результаты генерации."""

    def __init__(self, settings: PromptSettings | None = None):
        self.settings = settings or PromptSettings()

    def build_system_prompt(self) -> str:
        """Формирует системный промпт с учётом стиля."""
        prefix = STYLE_PREFIXES.get(self.settings.style, "")
        parts: List[str] = [prefix, self.settings.system_prompt]
        return "\n".join(p for p in parts if p)

    def build_full_prompt(self) -> str:
        """Возвращает полный промпт (системный + пользовательский)."""
        system = self.build_system_prompt()
        user = self.settings.user_prompt
        if not system:
            return user
        return f"{system}\n\n{user}"

    def generate(self) -> GenerationResult:
        """Эмуляция генерации: возвращает заглушку результата."""
        prompt = self.build_full_prompt()
        text = f"[echo] {prompt[:100]}"
        ok = bool(prompt.strip())
        return GenerationResult(text=text, settings=self.settings, ok=ok)

    def with_settings(self, settings: PromptSettings) -> "PromptEngine":
        """Возвращает новый движок с переданными настройками."""
        return PromptEngine(settings=settings)
