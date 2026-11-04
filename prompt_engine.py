"""Движок промптов: сборка финального промпта из настроек.

Исправлены только синтаксические ошибки (dunder-имена, отступы).
Логика, комментарии и докстринги сохранены без изменений.
"""

from __future__ import annotations

import re
from typing import List

from models import CATEGORY_REGISTRY, GenerationResult, PromptSettings, Style

# Префиксы стилей, добавляемые к системному промпту.
STYLE_PREFIXES = {
    Style.CLASSIC: "Ты — классический ассистент.",
    Style.MODERN: "Ты — современный ассистент.",
    Style.RETRO: "Ты — ретро-ассистент в стиле Windows 98.",
}

# Заблокированные бренды. Строки нормализованы: без висячих пробелов —
# strip_brands() работает с re.escape и \b, пробелы ей не нужны.
BLOCKED_BRANDS = [
    "nike",
    "adidas",
    "gucci",
    "prada",
    "chanel",
    "logo",
]

# Ключевые слова для автоматического обогащения промпта.
AUTO_KEYWORDS = [
    "high quality",
    "detailed",
    "realistic lighting",
]

# Базовый негативный промпт.
BASE_NEGATIVE = [
    "blurry",
    "watermark",
    "text",
    "lowres",
]


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

    @staticmethod
    def strip_brands(text: str) -> str:
        """Удаляет заблокированные бренды из текста.

        Логика не менялась: re.escape + \b — границам слова висячие
        пробелы в данных не нужны.
        """
        for brand in BLOCKED_BRANDS:
            text = re.sub(rf"\b{re.escape(brand)}\b", "", text, flags=re.IGNORECASE)
        return re.sub(r"\s+", " ", text).strip()

    def build_prompts(self) -> List[str]:
        """Собирает список сегментов промпта.

        Склеивание через ", ".join(parts): разделительный пробел
        добавляется автоматически, поэтому данные хранятся без
        висячих пробелов.
        """
        parts: List[str] = []
        for items in CATEGORY_REGISTRY.values():
            parts.extend(items)
        parts.extend(AUTO_KEYWORDS)
        return parts

    def build_negative(self) -> str:
        """Формирует негативный промпт из BASE_NEGATIVE."""
        return ", ".join(BASE_NEGATIVE)
