"""ui.py — Главное окно "Fashion Gen v1.0" в стиле Windows 98.

PyQt5, кастомный QSS (имитация Win98): серые панели #C0C0C0,
синие заголовки #000080, 3D-кнопки, вдавленные поля ввода,
меню File/Edit/Help (декоративное), статус-бар.
"""

from __future__ import annotations

import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QGuiApplication, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenuBar,
    QPushButton,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from models import CATEGORY_REGISTRY, make_item
from prompt_engine import build_prompts, default_current_year

# ----------------------------------------------------------------------
# QSS — имитация Windows 98
# ----------------------------------------------------------------------
WIN98_QSS = """
QWidget {
    background-color: #C0C0C0;
    color: #000000;
    font-family: "MS Sans Serif", "Tahoma", "Arial", sans-serif;
    font-size: 12px;
}
QMainWindow::separator {
    background: #C0C0C0;
    width: 2px;
    height: 2px;
}
/* ---------------- Menu bar ---------------- */
QMenuBar {
    background-color: #C0C0C0;
    border-bottom: 1px solid #808080;
}
QMenuBar::item {
    background: transparent;
    padding: 3px 8px;
}
QMenuBar::item:selected {
    background: #000080;
    color: #FFFFFF;
}
QMenu {
    background-color: #C0C0C0;
    border: 2px solid;
    border-color: #FFFFFF #808080 #808080 #FFFFFF;
}
QMenu::item:selected {
    background-color: #000080;
    color: #FFFFFF;
}
/* ---------------- Buttons: 3D raised ---------------- */
QPushButton {
    background-color: #C0C0C0;
    border-width: 2px;
    border-style: solid;
    border-color: #FFFFFF #808080 #808080 #FFFFFF;
    padding: 4px 10px;
    min-height: 16px;
}
QPushButton:hover {
    background-color: #D4D0C8;
}
QPushButton:pressed,
QPushButton:checked {
    border-color: #808080 #FFFFFF #FFFFFF #808080;
    padding: 5px 9px 3px 11px; /* текст "сдвигается" при нажатии */
}
QPushButton:default {
    border-color: #000000 #808080 #808080 #000000;
}
QPushButton:disabled {
    color: #808080;
    background-color: #C0C0C0;
}
/* ---------------- Inputs: inset ---------------- */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #FFFFFF;
    color: #000000;
    border-width: 2px;
    border-style: solid;
    border-color: #808080 #FFFFFF #FFFFFF #808080;
    selection-background-color: #000080;
    selection-color: #FFFFFF;
    padding: 2px;
}
QComboBox {
    background-color: #FFFFFF;
    border-width: 2px;
    border-style: solid;
    border-color: #808080 #FFFFFF #FFFFFF #808080;
    padding: 1px 4px;
    min-height: 18px;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 18px;
    border-left: 1px solid #808080;
    background-color: #C0C0C0;
    border-top: 1px solid #FFFFFF;
    border-right: 1px solid #808080;
    border-bottom: 1px solid #808080;
}
QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 2px solid #808080;
    selection-background-color: #000080;
    selection-color: #FFFFFF;
}
/* ---------------- Checkboxes ---------------- */
QCheckBox {
    spacing: 6px;
    background: transparent;
}
QCheckBox::indicator {
    width: 13px;
    height: 13px;
    background-color: #FFFFFF;
    border-width: 2px;
    border-style: solid;
    border-color: #808080 #FFFFFF #FFFFFF #808080;
}
QCheckBox::indicator:checked {
    background-color: #FFFFFF;
    image: none;
    border-color: #808080 #FFFFFF #FFFFFF #808080;
    color: #000000;
}
/* ---------------- Group boxes (Win98 fieldset) ---------------- */
QGroupBox {
    border: 1px solid #808080;
    border-top: 1px solid #FFFFFF;
    margin-top: 10px;
    padding-top: 6px;
    background-color: #C0C0C0;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 8px;
    padding: 0 3px;
    color: #000000;
}
/* ---------------- Scrollbars ---------------- */
QScrollBar {
    background: #DFDFDF;
    border: 1px solid #808080;
    width: 16px;
    height: 16px;
}
QScrollBar::handle {
    background: #C0C0C0;
    border-width: 1px;
    border-style: solid;
    border-color: #FFFFFF #808080 #808080 #FFFFFF;
    min-height: 14px;
    min-width: 14px;
}
QScrollBar::add-line, QScrollBar::sub-line {
    background: #C0C0C0;
    border-width: 1px;
    border-style: solid;
    border-color: #FFFFFF #808080 #808080 #FFFFFF;
    height: 15px;
    width: 15px;
}
QScrollBar::up-arrow, QScrollBar::down-arrow,
QScrollBar::left-arrow, QScrollBar::right-arrow {
    width: 0; height: 0;
}
/* ---------------- Status bar ---------------- */
QStatusBar {
    background-color: #C0C0C0;
}
QStatusBar::item {
    border: none;
}
QStatusBar QLabel {
    background-color: #C0C0C0;
    border-width: 1px;
    border-style: solid;
    border-color: #808080 #FFFFFF #FFFFFF #808080;
    padding: 2px 6px;
}
/* Sunken panel for output area */
QFrame#OutFrame {
    border-width: 2px;
    border-style: solid;
    border-color: #808080 #FFFFFF #FFFFFF #808080;
    background-color: #C0C0C0;
}
QLabel#TitleLabel {
    color: #000080;
    font-weight: bold;
    font-size: 14px;
}
"""


class Win98TitleBar(QFrame):
    """Фирменная синяя полоса внутри клиентской области окна."""

    def __init__(self, title: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setFixedHeight(22)
        self.setStyleSheet(
            "QFrame { background-color: #000080; }"
            "QLabel { color: #FFFFFF; font-weight: bold; font-size: 12px;"
            " background: transparent; }"
            "QPushButton { background-color: #C0C0C0; color: #000000;"
            " border-width: 2px; border-style: solid;"
            " border-color: #FFFFFF #808080 #808080 #FFFFFF;"
            " font-weight: bold; min-width: 16px; max-width: 16px;"
            " min-height: 14px; max-height: 14px; padding: 0px; }"
            "QPushButton:pressed { border-color: #808080 #FFFFFF #FFFFFF #808080; }"
        )
        lay = QHBoxLayout(self)
        lay.setContentsMargins(4, 2, 2, 2)
        lay.setSpacing(2)
        label = QLabel("\U0001F457  " + title)
        lay.addWidget(label)
        lay.addStretch(1)
        for ch in ("_", "\u25A1", "\u2715"):
            btn = QPushButton(ch)
            btn.setFixedSize(18, 16)
            if ch == "\u2715":
                btn.clicked.connect(lambda: self.window().close())
            elif ch == "_":
                btn.clicked.connect(lambda: self.window().showMinimized())
            else:
                btn.setDisabled(True)
            lay.addWidget(btn)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fashion Gen v1.0")
        self.resize(760, 520)
        self._current_year = default_current_year()

        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(6)

        root.addWidget(Win98TitleBar(f"Fashion Gen 98  -  [{self._current_year - 20}] Trend Engine"))

        body = QHBoxLayout()
        body.setSpacing(8)
        body.addLayout(self._build_left_panel(), 2)
        body.addLayout(self._build_right_panel(), 3)
        root.addLayout(body, 1)

        self.setCentralWidget(central)
        self._build_menu()

        # ---- Status bar ----
        sb = QStatusBar()
        sb.setSizeGripEnabled(True)
        self.setStatusBar(sb)
        self.status_label = QLabel("Ready")
        self.year_label = QLabel(f"Trend year: {self._current_year - 20}")
        sb.addWidget(self.status_label, 1)
        sb.addPermanentWidget(self.year_label)

        self.setStyleSheet(WIN98_QSS)
        app_font = QFont("MS Sans Serif", 8)
        app_font.setStyleHint(QFont.SansSerif)
        self.setFont(app_font)

    # ------------------------------------------------------------------
    # Меню (декоративное)
    # ------------------------------------------------------------------
    def _build_menu(self):
        mb = QMenuBar(self)
        for name in ("File", "Edit", "Help"):
            m = mb.addMenu(name)
            if name == "File":
                m.addAction("New...")
                m.addAction("Open...")
                m.addSeparator()
                m.addAction("Exit", self.close)
            elif name == "Edit":
                m.addAction("Copy")
                m.addAction("Paste")
            else:
                m.addAction("About Fashion Gen 98...", self._about)
        self.setMenuBar(mb)

    def _about(self):
        self.status("Fashion Gen v1.0 (c) 1998-ish  |  Tool from the past, creating the future")

    def status(self, text: str):
        self.status_label.setText(text)

    # ------------------------------------------------------------------
    # Левая панель — настройки
    # ------------------------------------------------------------------
    def _build_left_panel(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(8)

        grp = QGroupBox("Settings")
        grid = QGridLayout(grp)
        grid.setContentsMargins(8, 12, 8, 8)
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(6)

        grid.addWidget(QLabel("Category:"), 0, 0)
        self.cb_category = QComboBox()
        self.cb_category.addItems(list(CATEGORY_REGISTRY.keys()))
        grid.addWidget(self.cb_category, 0, 1)

        grid.addWidget(QLabel("Item type:"), 1, 0)
        self.cb_item = QComboBox()
        grid.addWidget(self.cb_item, 1, 1)

        grid.addWidget(QLabel("Color:"), 2, 0)
        self.cb_color = QComboBox()
        self.cb_color.addItems([
            "Any", "Black", "White", "Navy Blue", "Red", "Forest Green",
            "Beige", "Grey", "Pastel Pink", "Brown", "Mustard Yellow",
        ])
        grid.addWidget(self.cb_color, 2, 1)

        grid.addWidget(QLabel("Material:"), 3, 0)
        self.cb_material = QComboBox()
        self.cb_material.addItems([
            "Any", "Cotton", "Denim", "Wool", "Leather", "Polyester",
            "Silk", "Linen", "Fleece",
        ])
        grid.addWidget(self.cb_material, 3, 1)

        layout.addWidget(grp)

        # Чекбоксы деталей
        det = QGroupBox("Details")
        dv = QVBoxLayout(det)
        dv.setContentsMargins(8, 12, 8, 6)
        self.chk_pockets = QCheckBox("Pockets")
        self.chk_collar = QCheckBox("Collar")
        self.chk_buttons = QCheckBox("Buttons")
        self.chk_pattern = QCheckBox("Retro pattern / stripes")
        for c in (self.chk_pockets, self.chk_collar, self.chk_buttons, self.chk_pattern):
            dv.addWidget(c)
        layout.addWidget(det)

        # Кнопка генерации
        self.btn_generate = QPushButton("Generate Prompt")
        self.btn_generate.setDefault(True)
        self.btn_generate.setMinimumHeight(30)
        self.btn_generate.clicked.connect(self.on_generate)
        layout.addWidget(self.btn_generate)

        layout.addStretch(1)

        # Заполнение списка предметов
        self.cb_category.currentTextChanged.connect(self._refresh_items)
        self._refresh_items(self.cb_category.currentText())
        return layout

    def _refresh_items(self, category: str):
        self.cb_item.clear()
        for _, name in CATEGORY_REGISTRY.get(category, []):
            self.cb_item.addItem(name)

    # ------------------------------------------------------------------
    # Правая панель — результат
    # ------------------------------------------------------------------
    def _build_right_panel(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(6)

        pos_box = QGroupBox("Positive Prompt")
        pv = QVBoxLayout(pos_box)
        pv.setContentsMargins(8, 12, 8, 8)
        self.txt_positive = QTextEdit()
        self.txt_positive.setReadOnly(True)
        self.txt_positive.setLineWrapMode(QTextEdit.WidgetWidth)
        pv.addWidget(self.txt_positive)
        row_pos = QHBoxLayout()
        row_pos.addStretch(1)
        btn_copy_pos = QPushButton("[Copy]")
        btn_copy_pos.clicked.connect(lambda: self.copy_to_clipboard(self.txt_positive))
        row_pos.addWidget(btn_copy_pos)
        pv.addLayout(row_pos)
        layout.addWidget(pos_box, 1)

        neg_box = QGroupBox("Negative Prompt")
        nv = QVBoxLayout(neg_box)
        nv.setContentsMargins(8, 12, 8, 8)
        self.txt_negative = QTextEdit()
        self.txt_negative.setReadOnly(True)
        self.txt_negative.setLineWrapMode(QTextEdit.WidgetWidth)
        nv.addWidget(self.txt_negative)
        row_neg = QHBoxLayout()
        row_neg.addStretch(1)
        btn_copy_neg = QPushButton("[Copy]")
        btn_copy_neg.clicked.connect(lambda: self.copy_to_clipboard(self.txt_negative))
        row_neg.addWidget(btn_copy_neg)
        nv.addLayout(row_neg)
        layout.addWidget(neg_box, 1)

        return layout

    # ------------------------------------------------------------------
    # Действия
    # ------------------------------------------------------------------
    def on_generate(self):
        self._play_click()
        self.status("Generating...")
        QApplication.changeOverrideCursor(Qt.WaitCursor)
        self.btn_generate.setEnabled(False)
        # Небольшая ретро-задержка "как на пеньке 133 МГц"
        QTimer.singleShot(350, self._do_generate)

    def _do_generate(self):
        try:
            item = make_item(self.cb_category.currentText(),
                             self.cb_item.currentText())
        except ValueError:
            self.status("No item selected!")
            self._finish_generation()
            return

        details = []
        if self.chk_pockets.isChecked():
            details.append("visible pockets")
        if self.chk_collar.isChecked():
            details.append("structured collar")
        if self.chk_buttons.isChecked():
            details.append("button closure")
        if self.chk_pattern.isChecked():
            details.append("retro striped pattern")

        attributes = {
            "color": self.cb_color.currentText(),
            "material": self.cb_material.currentText(),
        }

        positive, negative = build_prompts(item, attributes,
                                           current_year=self._current_year,
                                           details=details)
        self.txt_positive.setPlainText(positive)
        self.txt_negative.setPlainText(negative)
        self.status("Prompt generated.")
        self._finish_generation()
        QTimer.singleShot(2500, lambda: self.status("Ready"))

    def _finish_generation(self):
        QApplication.restoreOverrideCursor()
        self.btn_generate.setEnabled(True)

    def copy_to_clipboard(self, widget: QTextEdit):
        self._play_click()
        text = widget.toPlainText()
        if not text:
            self.status("Nothing to copy.")
            return
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text)
        self.status("Copied to clipboard")
        QTimer.singleShot(2000, lambda: self.status("Ready"))

    @staticmethod
    def _play_click():
        """Опциональный звуковой эффект клика (без внешних файлов)."""
        try:
            QApplication.beep()
        except Exception:
            pass


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Fashion Gen v1.0")
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
