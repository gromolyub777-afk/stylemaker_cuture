"""prompt_engine.py — Движок сборки промтов.

Правила:
 * Тренды "-20 лет": retro_year = current_year - 20, атрибуты берутся у модели.
 * No Logo Policy: жёсткое исключение брендов (список BLOCKED_BRANDS).
 * Auto-Keywords: белый фон, студийный свет и т.д. добавляются автоматически.
 * Negative Prompt: автосборка списка запретов.
"""

from __future__ import annotations

from datetime import date

# ----------------------------------------------------------------------
# No Logo Policy — любые упоминания этих слов вырезаются из промта
# ----------------------------------------------------------------------
BLOCKED_BRANDS = [
    "nike", "adidas", "puma", "reebok", "gucci", "prada", "louis vuitton",
    "chanel", "dior", "versace", "armani", "balenciaga", "fendi", "hermes",
    "levi", "levis", "calvin klein", "tommy hilfiger", "ralph lauren",
    "lacoste", "fila", "new balance", "vans", "converse", "supreme",
    "off-white", "burberry", "moncler", "north face", "champion",
    "logo", "brand", "trademark",
]

# Auto-keywords, подмешиваемые в каждый positive prompt
AUTO_KEYWORDS = [
    "no logo",
    "no text",
    "unbranded garment",
    "white background",
    "studio lighting",
    "product photography",
    "8k",
    "high detail",
]

# Базовый negative prompt
BASE_NEGATIVE = [
    "logo",
    "text",
    "watermark",
    "brand name",
    "branding",
    "blurry",
    "bad quality",
    "low resolution",
    "complex background",
    "cluttered background",
    "oversaturated colors",
    "extra limbs",
    "deformed fabric",
]


def strip_brands(text: str) -> str:
    """Жёстко вырезает названия брендов из произвольного текста.

    Вырезание выполняется по словам (word boundary), чтобы не портить
    служебные фразы вроде "no logo" или "unbranded". Слово "logo"/"brand"
    удаляется только если оно НЕ предваряется частицей "no"/"un".
    """
    import re

    def _pattern(word: str) -> str:
        # Разрешаем дефис/пробел внутри многословных брендов
        return r"\b" + r"[\s\-]?".join(re.escape(p) for p in word.split()) + r"\b"

    for brand in BLOCKED_BRANDS:
        if brand in ("logo", "brand", "trademark"):
            # Оставляем "no logo" / "no text" / "unbranded" нетронутыми
            pat = r"(?<!\bno\s)(?<!\bun)" + _pattern(brand)
        else:
            pat = _pattern(brand)
        text = re.sub(pat, "", text, flags=re.IGNORECASE)

    # Схлопываем мусор, оставшийся после вырезания
    text = re.sub(r"\s+,", ",", text)
    text = re.sub(r",{2,}", ",", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip().strip(",").strip()


def default_current_year() -> int:
    return date.today().year


# ----------------------------------------------------------------------
# Основная сборка
# ----------------------------------------------------------------------
def build_prompts(item, attributes: dict, current_year: int | None = None,
                  details: list[str] | None = None) -> tuple[str, str]:
    """Собирает (positive, negative) промты для выбранной одежды.

    :param item: экземпляр ClothingItem (см. models.py)
    :param attributes: {"color": "...", "material": "..."} — выбор пользователя
    :param current_year: текущий год (по умолчанию — системный)
    :param details: список включённых чекбоксов ("pockets", "collar", ...)
    :return: кортеж (positive_prompt, negative_prompt)
    """
    if current_year is None:
        current_year = default_current_year()

    retro_year = current_year - 20
    attrs = item.get_retro_attributes(retro_year)

    parts: list[str] = [item.name]

    color = (attributes.get("color") or "").strip()
    if color and color != "Any":
        parts.append(color)

    material = (attributes.get("material") or "").strip()
    if material and material != "Any":
        parts.append(material)

    parts.append(attrs["cut"])

    detail_bits = []
    if attrs.get("details"):
        detail_bits.append(attrs["details"])
    for d in details or []:
        if d:
            detail_bits.append(d)
    if detail_bits:
        parts.append(", ".join(detail_bits))

    parts.append(f"{retro_year} retro trend, {attrs['vibe']}")
    parts.extend(AUTO_KEYWORDS)

    positive = strip_brands(", ".join(parts))

    # Negative: база + всё, что связано с брендами/логотипами
    negative_terms = list(BASE_NEGATIVE)
    negative_terms.append(f"modern {current_year} style")
    negative_terms.append("colored background")
    negative = ", ".join(negative_terms)

    return positive, negative
