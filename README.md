# Fashion Gen v1.0 — Windows 98 Prompt Constructor

**Концепция:** «Инструмент из прошлого, создающий будущее».
Приложение на Python (PyQt5), имитирующее интерфейс Windows 98 и служащее
конструктором промтов для генерации одежды с упором на тренды **20-летней
давности**, жёстким запретом логотипов и автоматической подстройкой под
белый фон.

## Структура проекта

| Файл | Назначение |
|---|---|
| `main.py` | Точка входа: `python main.py` |
| `models.py` | ООП-классы одежды (`ClothingItem`, `Shirt/PoloShirt/Jeans/...`) и ретро-атрибуты по годам |
| `prompt_engine.py` | Сборка Positive/Negative промтов: тренды −20 лет, No Logo Policy, auto-keywords |
| `ui.py` | Главное окно `QMainWindow` в стиле Win98 (кастомный QSS) |

## Запуск

```bash
pip install -r requirements.txt   # PyQt5>=5.15
python main.py
```

## Интерфейс

* Меню **File / Edit / Help** (декоративное).
* Синяя полоса заголовка `#000080` внутри клиентской области + кнопки `_ □ ✕`.
* **Левая панель:** Combo Box'ы (Category → Item type → Color → Material),
  чекбоксы деталей (карманы, воротник, пуговицы, ретро-полоска),
  кнопка **Generate Prompt** с 3D-эффектом (вдавливается при нажатии).
* **Правая панель:** два Edit Control с вертикальной прокруткой
  (Positive / Negative Prompt) и кнопки **[Copy]** у каждого поля.
* **Статус-бар:** `Ready` → `Generating...` (песочные часы-курсор) →
  `Prompt generated.` / `Copied to clipboard`.
* Палитра Win98: `#C0C0C0` фон, белый ввод с inset-рамкой,
  шрифт MS Sans Serif / Tahoma 8pt.
* Звуковой клик — `QApplication.beep()` при нажатиях (опционально, без файлов).

## Логика генерации

1. **Тренды −20 лет:** `retro_year = current_year - 20`
   (2026 → 2006: low-rise bootcut, pop-collar, Y2K-силуэты).
2. **No Logo Policy:** список `BLOCKED_BRANDS` вырезается из промта
   по границам слов (Nike, Gucci, Levi's…); служебные фразы
   `no logo` / `unbranded` не повреждаются.
3. **Auto-Keywords:** `no logo, no text, unbranded garment, white background,
   studio lighting, product photography, 8k, high detail`.
4. **Negative Prompt:** `logo, text, watermark, brand name, blurry,
   bad quality, complex background, modern <current_year> style, …`.

### Пример результата

```
Positive: Polo Shirt, Navy Blue, Cotton, pop-collar slim polo cut, popped collar,
contrasting sleeve stripes, visible pockets, 2006 retro trend, early 2000s Y2K
fashion, no logo, no text, unbranded garment, white background, studio lighting,
product photography, 8k, high detail

Negative: logo, text, watermark, brand name, branding, blurry, bad quality,
low resolution, complex background, cluttered background, oversaturated colors,
extra limbs, deformed fabric, modern 2026 style, colored background
```

## Пользовательский сценарий (Retro Flow)

1. Запуск → серое окно с синей полосой «Fashion Gen 98».
2. Выбор `Top → Polo Shirt`, цвет `Navy Blue`.
3. Клик **Generate Prompt** (кнопка визуально вдавливается, курсор — песочные
   часы, статус-бар: «Generating...»).
4. Через короткую «пенси на 133 МГц» задержку тексты появляются в полях.
5. Клик **[Copy]** → буфер обмена + «Copied to clipboard» в статус-баре.
