from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from services.api_service import APIService
from base import set_module_style, create_label
from constants import BG_OPACITY, RADIUS_100, TEXT_100, PADD_200, FONT_BODY, BG_100, BG_200, SECONDARY, ACCENT, PRIMARY, TABLE_FIELDS

class SearchPage(QWidget):
    def __init__(self):
        """Initialize the Search page"""
        super().__init__()
        self.api = APIService()
        set_module_style(self)
        self.setup_ui()

    def setup_ui(self):
        """Initialize the Search page"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        container = QWidget()
        container_layout = QVBoxLayout(container)

        # Search bar
        search_bar = self.crate_search_bar()
        container_layout.addWidget(search_bar)

        # Scroll area for results
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setStyleSheet(self.scrollbar_style())
        container_layout.addWidget(self.scroll_area)

        main_layout.addWidget(container)

        # Show initial table
        latest = self.show_latest_records()
        if latest: self.create_table(latest)
        else: self.show_message("No data available.", SECONDARY)

    def crate_search_bar(self):
        """Creates a search bar to show a data related to the searched id"""
        container = QWidget()
        search_layout = QHBoxLayout()
        search_layout.setSpacing(0)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID...")
        self.search_input.returnPressed.connect(self.search)
        self.search_input.setStyleSheet(f"""
            background-color: {BG_OPACITY};
            padding: {PADD_200}px;
            height: 40px;
            width: 40px;
            border-top-left-radius: {RADIUS_100}px;
            border-bottom-left-radius: {RADIUS_100}px;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
            color: {TEXT_100};
            font: 11pt;
        """)

        # Search button
        search_button = QPushButton()
        search_button.setIcon(QIcon("assets/icons/search.svg"))
        search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        search_button.clicked.connect(self.search)
        search_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_OPACITY};
                padding: {PADD_200}px;
                height: 40px;
                min-width: 40px;
                max-width: 40px;
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                border-top-right-radius: {RADIUS_100}px;
                border-bottom-right-radius: {RADIUS_100}px;
            }}
            QPushButton:hover {{
                background-color: {BG_100};
            }}
            QPushButton:pressed {{
                background-color: {PRIMARY};
            }}
        """)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        container.setLayout(search_layout)
        return container
    
    def clear_area(self):
        """Cleans the scrolling area"""
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item: widget = item.widget()
            if widget: widget.deleteLater()

    def show_message(self, message, color="white"):
        """
        Displays a message in the scrolling areap
        :param message: The message to be displayed
        :param color: The color of the message
        """
        self.clear_area()
        label = create_label(message, FONT_BODY, f"color: {color}; padding: 12px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addWidget(label) 

    def show_latest_records(self):
        """Displays the last 5 data from the database"""
        try:
            result = self.api.get_all()
            if not result.get("success") or "data" not in result:
                return None
            data = result["data"]
            if not isinstance(data, list) or not data:
                return None
            return list(data[:5])
        except Exception as e:
            self.show_message(f"Error: {str(e)}", ACCENT)
            return None

    def search(self):
        """Allows searching by id of some data"""
        id_text = self.search_input.text().strip()
        if id_text == "":
            latest = self.show_latest_records()
            if latest: self.create_table(latest)
            else: self.show_message("No data available.", SECONDARY)
            return
        
        if not id_text.isdigit():
            self.show_message("Please enter a valid numeric ID.", SECONDARY)
            return
        
        try:
            result = self.api.get_by_id(int(id_text))
            if result.get("success") and result.get("data"):
                self.create_table([result["data"]])
            else: self.show_message("No data found for that ID.", SECONDARY)
        except Exception as e:
            self.show_message(f"Error: {str(e)}", ACCENT)

    def create_table(self, data):
        """
        Creates a table with the data
        :param data: The data to be displayed in the table
        """
        self.clear_area()
        if not data:
            self.show_message("No data to display.", SECONDARY)
            return
        
        table = QTableWidget()
        table.setRowCount(len(data[0]))
        table.setColumnCount(1 + len(data))

        # Table settings
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        header_h = table.horizontalHeader()
        header_v = table.verticalHeader()
        viewport = table.viewport()

        if header_h:
            header_h.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            header_h.setVisible(False)

        if header_v:
            header_v.setVisible(False)

        if viewport:
            viewport.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)

        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {BG_OPACITY};
                alternate-background-color: {BG_200};
                padding: 15px {PADD_200}px;
                border: none;
            }}
            QTableWidget::item {{
                color: {TEXT_100};
                border-right: 1px solid {BG_OPACITY};
                padding: 12px;
            }}
        """)

        # First column (titles)
        font_bold = FONT_BODY
        font_bold.setBold(True)
        for row, key in enumerate(list(data[0].keys())):
            item = QTableWidgetItem(str(TABLE_FIELDS.get(key, key)).upper())
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            item.setFont(font_bold)
            table.setItem(row, 0, item)
            table.setRowHeight(row, 39)
        
        # Columns with data
        for col_idx, record in enumerate(data, start=1):
            for row_idx, key in enumerate(list(data[0].keys())):
                value = str(record.get(key, ""))
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFont(FONT_BODY)
                table.setItem(row_idx, col_idx, item)

        self.scroll_layout.addWidget(table)

    def scrollbar_style(self):
        """Returns the scrollbar stylesheet"""
        return f"""
            QScrollBar:vertical {{
                background-color: {BG_200};
                width: 20px;
                padding: 0;
            }}
            QScrollBar::handle:vertical {{
                background-color: {BG_100};
                min-height: 20px;
                margin: 21px 0;
            }}
            QScrollBar::handle:vertical:pressed,
            QScrollBar::sub-line:vertical:pressed,
            QScrollBar::add-line:vertical:pressed {{
                background-color: {PRIMARY};
            }}
            QScrollBar::sub-line:vertical,
            QScrollBar::add-line:vertical {{
                border: none;
                background-color: {BG_100};
                height: 20px;
            }}
            QScrollBar::up-arrow:vertical, 
            QScrollBar::down-arrow:vertical {{
                width: 15px;
                height: 15px;
                background: none;
            }}
            QScrollBar::up-arrow:vertical {{
                image: url("assets/icons/up.svg");
            }}
            QScrollBar::down-arrow:vertical {{
                image: url("assets/icons/down.svg")
            }}
            QScrollBar::add-page:vertical, 
            QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """
