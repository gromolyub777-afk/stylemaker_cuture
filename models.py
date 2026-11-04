"""models.py — Классы одежды (ООП подход).

Каждый предмет одежды знает свои "ретро-атрибуты" для конкретного года.
Приложение строит промты под тренды 20-летней давности: год на экране
(2026) -> целевой ретро-год (2006) и т.д.
"""

from __future__ import annotations


# ----------------------------------------------------------------------
# Базовый класс
# ----------------------------------------------------------------------
class ClothingItem:
    """Базовый класс любого предмета гардероба."""

    def __init__(self, name: str, category: str):
        self.name = name            # отображаемое имя ("Polo Shirt")
        self.category = category    # категория ("Top", "Bottom", ...)

    # -- служебное -----------------------------------------------------
    @staticmethod
    def _decade(year: int) -> int:
        """Возвращает десятилетие, к которому относится год (1990, 2000...)."""
        return (year // 10) * 10

    def get_retro_attributes(self, year: int) -> dict:
        """Возвращает словарь атрибутов ('cut', 'details', 'vibe') для года.

        По умолчанию — общие атрибуты по десятилетиям. Дочерние классы
        могут переопределять или расширять поведение.
        """
        decade = self._decade(year)
        base = {
            1980: {"cut": "boxy retro cut", "vibe": "80s vintage fashion"},
            1990: {"cut": "relaxed 90s fit", "vibe": "grunge era 90s fashion"},
            2000: {"cut": "slim Y2K silhouette", "vibe": "early 2000s Y2K fashion"},
            2010: {"cut": "skinny fast-fashion fit", "vibe": "late 2010s streetwear"},
        }.get(decade, {"cut": "timeless classic cut", "vibe": f"{year} fashion archive"})

        attrs = {
            "cut": base["cut"],
            "vibe": base["vibe"],
            "details": "",
        }
        return attrs

    def __repr__(self) -> str:  # pragma: no cover
        return f"<{type(self).__name__} name={self.name!r} category={self.category!r}>"


# ----------------------------------------------------------------------
# Верх (Tops)
# ----------------------------------------------------------------------
class TShirt(ClothingItem):
    def __init__(self, name: str = "T-Shirt"):
        super().__init__(name, "Top")

    def get_retro_attributes(self, year: int) -> dict:
        attrs = super().get_retro_attributes(year)
        decade = self._decade(year)
        if decade <= 1990:
            attrs["cut"] = "oversized boxy cotton cut"
            attrs["details"] = "wide ribbed collar"
        elif decade == 2000:
            attrs["cut"] = "tight fitted crew-neck cut"
            attrs["details"] = "shrunken tee proportions"
        else:
            attrs["cut"] = "slim modern-fit cut"
            attrs["details"] = "flat-lock seams"
        return attrs


class PoloShirt(ClothingItem):
    def __init__(self, name: str = "Polo Shirt"):
        super().__init__(name, "Top")

    def get_retro_attributes(self, year: int) -> dict:
        attrs = super().get_retro_attributes(year)
        decade = self._decade(year)
        if decade == 2000:
            attrs["cut"] = "pop-collar slim polo cut"
            attrs["details"] = "popped collar, contrasting sleeve stripes"
        elif decade == 1990:
            attrs["cut"] = "loose preppy polo cut"
            attrs["details"] = "big soft collar, two-button placket"
        else:
            attrs["cut"] = "classic pique polo cut"
            attrs["details"] = "three-button placket"
        return attrs


class Hoodie(ClothingItem):
    def __init__(self, name: str = "Hoodie"):
        super().__init__(name, "Top")

    def get_retro_attributes(self, year: int) -> dict:
        attrs = super().get_retro_attributes(year)
        decade = self._decade(year)
        if decade == 2000:
            attrs["cut"] = "baggy zip-up hoodie cut"
            attrs["details"] = "extra-wide kangaroo pocket, drawstring hood"
        elif decade == 1990:
            attrs["cut"] = "oversized pullover hoodie cut"
            attrs["details"] = "double-layer hood"
        else:
            attrs["cut"] = "regular-fit pullover hoodie cut"
            attrs["details"] = "ribbed cuffs and hem"
        return attrs


# ----------------------------------------------------------------------
# Низ (Bottoms)
# ----------------------------------------------------------------------
class Jeans(ClothingItem):
    def __init__(self, name: str = "Jeans"):
        super().__init__(name, "Bottom")

    def get_retro_attributes(self, year: int) -> dict:
        attrs = super().get_retro_attributes(year)
        decade = self._decade(year)
        if decade == 2000:
            attrs["cut"] = "low-rise bootcut jeans"
            attrs["details"] = "flared leg, hip-sitting waistband"
        elif decade == 1990:
            attrs["cut"] = "loose straight-leg baggy jeans"
            attrs["details"] = "hammer loop, cuffed hem"
        else:
            attrs["cut"] = "high-rise slim jeans"
            attrs["details"] = "clean finish"
        return attrs


class CargoPants(ClothingItem):
    def __init__(self, name: str = "Cargo Pants"):
        super().__init__(name, "Bottom")

    def get_retro_attributes(self, year: int) -> dict:
        attrs = super().get_retro_attributes(year)
        decade = self._decade(year)
        if decade == 2000:
            attrs["cut"] = "baggy parachute cargo pants"
            attrs["details"] = "oversized side pockets, ankle straps"
        else:
            attrs["cut"] = "tapered utility cargo cut"
            attrs["details"] = "flat flap pockets"
        return attrs


class Skirt(ClothingItem):
    def __init__(self, name: str = "Mini Skirt"):
        super().__init__(name, "Bottom")

    def get_retro_attributes(self, year: int) -> dict:
        attrs = super().get_retro_attributes(year)
        decade = self._decade(year)
        if decade == 2000:
            attrs["cut"] = "micro pleated mini skirt"
            attrs["details"] = "low-slung hipster waistband"
        else:
            attrs["cut"] = "A-line midi skirt"
            attrs["details"] = "hidden side zipper"
        return attrs


# ----------------------------------------------------------------------
# Обувь (Shoes)
# ----------------------------------------------------------------------
class Sneakers(ClothingItem):
    def __init__(self, name: str = "Sneakers"):
        super().__init__(name, "Shoes")

    def get_retro_attributes(self, year: int) -> dict:
        attrs = super().get_retro_attributes(year)
        decade = self._decade(year)
        if decade == 2000:
            attrs["cut"] = "chunky retro runner sneakers"
            attrs["details"] = "mesh panels, thick foam midsole"
        else:
            attrs["cut"] = "low-profile canvas sneakers"
            attrs["details"] = "rubber cup sole"
        return attrs


# ----------------------------------------------------------------------
# Реестр для UI: категория -> [(класс, отображаемое имя), ...]
# ----------------------------------------------------------------------
CATEGORY_REGISTRY: dict[str, list[tuple[type[ClothingItem], str]]] = {
    "Top": [
        (TShirt, "T-Shirt"),
        (PoloShirt, "Polo Shirt"),
        (Hoodie, "Hoodie"),
    ],
    "Bottom": [
        (Jeans, "Jeans"),
        (CargoPants, "Cargo Pants"),
        (Skirt, "Mini Skirt"),
    ],
    "Shoes": [
        (Sneakers, "Sneakers"),
    ],
}


def make_item(category: str, item_name: str) -> ClothingItem:
    """Фабрика: по названиям из комбобоксов возвращает экземпляр класса."""
    for cls, name in CATEGORY_REGISTRY.get(category, []):
        if name == item_name:
            return cls()
    raise ValueError(f"Unknown item: {category}/{item_name}")
