import sys
import os
import json
import time
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import (QApplication, QMainWindow, QComboBox, QPushButton, 
                            QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                            QGridLayout, QGroupBox, QStatusBar, QFrame, QSplitter,
                            QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget, QLineEdit,
                            QSpinBox, QSlider)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QSize
from PyQt6.QtGui import QColor, QPalette, QFont, QIcon, QPixmap

# Import des utilitaires série
from serial_utils import SerialReaderThread, get_available_ports, open_serial_port, parse_can_frame


class SerialMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Moniteur CAN")
        self.resize(1200, 800)
        self.serial_port = None
        self.reader_thread = SerialReaderThread()
        self.reader_thread.data_received.connect(self.update_received_data)
        self.received_frames = []
        self.is_dark_mode = True
        self.init_theme()
        self.init_ui()
        self.create_menu_bar()
        self.apply_theme()
        
        # Appliquer la configuration de l'interface
        self.apply_ui_config()

    def create_menu_bar(self):
        """Crée la barre de menu en haut de l'application."""
        menu_bar = self.menuBar()

        # Menu Fichier
        file_menu = menu_bar.addMenu("&Fichier")
        
        save_action = QAction("Enregistrer les données", self)
        save_action.triggered.connect(self.save_data)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Quitter", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Menu Affichage
        view_menu = menu_bar.addMenu("&Affichage")
        self.toggle_table_action = QAction("Afficher/Masquer la table", self, checkable=True)
        self.toggle_table_action.setChecked(True)
        self.toggle_table_action.triggered.connect(self.toggle_table_visibility)
        view_menu.addAction(self.toggle_table_action)
        self.toggle_text_action = QAction("Afficher/Masquer la zone texte", self, checkable=True)
        self.toggle_text_action.setChecked(True)
        self.toggle_text_action.triggered.connect(self.toggle_text_visibility)
        view_menu.addAction(self.toggle_text_action)

        # Menu Thème
        theme_menu = menu_bar.addMenu("&Thème")
        self.theme_action = QAction("Mode Jour", self, checkable=True)
        self.theme_action.setChecked(not self.is_dark_mode)
        self.theme_action.triggered.connect(self.toggle_theme)
        theme_menu.addAction(self.theme_action)

        # Menu Favoris
        self.favorites_menu = menu_bar.addMenu("&Favoris")
        add_favorite_action = QAction("Ajouter commande actuelle", self)
        add_favorite_action.triggered.connect(self.add_to_favorites)
        self.favorites_menu.addAction(add_favorite_action)
        
        manage_favorites_action = QAction("Gérer les favoris", self)
        manage_favorites_action.triggered.connect(self.manage_favorites)
        self.favorites_menu.addAction(manage_favorites_action)
        
        self.favorites_menu.addSeparator()
        
        # Charger les favoris enregistrés
        self.load_favorites()
        
        # Menu Configuration
        config_menu = menu_bar.addMenu("&Configuration")
        
        # Options d'interface utilisateur
        ui_config_action = QAction("Options d'interface", self)
        ui_config_action.triggered.connect(self.show_ui_config_dialog)
        config_menu.addAction(ui_config_action)
        
        # Sauvegarder/restaurer la configuration
        save_config_action = QAction("Sauvegarder la configuration", self)
        save_config_action.triggered.connect(self.save_config)
        config_menu.addAction(save_config_action)
        
        reset_config_action = QAction("Réinitialiser la configuration", self)
        reset_config_action.triggered.connect(self.reset_config)
        config_menu.addAction(reset_config_action)
        
        # Menu Aide
        help_menu = menu_bar.addMenu("&Aide")
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def toggle_table_visibility(self):
        if hasattr(self, 'data_table'):
            visible = self.toggle_table_action.isChecked()
            self.data_table.setVisible(visible)
    def toggle_text_visibility(self):
        if hasattr(self, 'data_display'):
            visible = self.toggle_text_action.isChecked()
            self.data_display.setVisible(visible)
    def show_about_dialog(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "À propos", "CAN Sniffer\nInterface graphique pour le monitoring et l'envoi de trames CAN.\nDéveloppé avec PyQt6.")

    def toggle_theme(self):
        """Bascule entre le thème clair et sombre."""
        self.is_dark_mode = not self.is_dark_mode
        self.theme_action.setText("Mode Jour" if self.is_dark_mode else "Mode Nuit")
        self.init_theme()

    def init_theme(self):
        """Initialise les couleurs du thème."""
        if self.is_dark_mode:
            # Thème sombre inspiré de SunHub
            self.bg_primary = "#1e2132"       # Bleu très foncé (fond principal)
            self.bg_secondary = "#171923"     # Bleu encore plus foncé (fond secondaire)
            self.bg_tertiary = "#252a41"      # Bleu foncé pour les cartes
            self.text_primary = "#ffffff"     # Blanc pour le texte
            self.accent_primary = "#7aa2f7"   # Bleu clair pour les accents
            self.accent_secondary = "#252a41" # Bleu clair pour les boutons
            self.disabled = "#9ba3af"        # Gris pour les éléments désactivés
            self.border = "#171923"          # Bordures très foncées
        else:
            # Thème clair avec des tons de gris
            self.bg_primary = "#f5f6fa"       # Gris très clair (fond principal)
            self.bg_secondary = "#e8e9ef"     # Gris clair (fond secondaire)
            self.bg_tertiary = "#ffffff"      # Blanc pour les cartes
            self.text_primary = "#2c3e50"     # Gris foncé pour le texte
            self.accent_primary = "#3498db"   # Bleu pour les accents
            self.accent_secondary = "#2980b9" # Bleu foncé pour les boutons
            self.disabled = "#bdc3c7"        # Gris pour les éléments désactivés
            self.border = "#dcdde1"          # Gris clair pour les bordures

        # Couleurs communes aux deux thèmes
        self.warning = "#f39c12"         # Orange (avertissement)
        self.error = "#e74c3c"           # Rouge (erreur)
        self.success = "#27ae60"         # Vert (succès)
        
        self.apply_theme()
        
    def apply_theme(self):
        """Applique le thème à l'application entière."""
        app = QApplication.instance()
        palette = QPalette()
        
        # Couleurs générales
        palette.setColor(QPalette.ColorRole.Window, QColor(self.bg_primary))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(self.text_primary))
        palette.setColor(QPalette.ColorRole.Base, QColor(self.bg_secondary))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(self.bg_tertiary))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(self.bg_secondary))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(self.text_primary))
        palette.setColor(QPalette.ColorRole.Text, QColor(self.text_primary))
        palette.setColor(QPalette.ColorRole.Button, QColor(self.bg_tertiary))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(self.text_primary))
        palette.setColor(QPalette.ColorRole.Link, QColor(self.accent_primary))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(self.accent_secondary))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(self.text_primary))
        
        # Couleurs pour les widgets désactivés
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(self.disabled))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(self.disabled))
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(self.disabled))
        
        app.setPalette(palette)
        
        # Style sheets pour les widgets spécifiques
        app.setStyleSheet(f"""
            QMainWindow, QDialog {{ background-color: {self.bg_primary}; }}
            QMenuBar {{ background-color: {self.bg_secondary}; color: {self.text_primary}; border-bottom: 1px solid {self.border}; }}
            QMenuBar::item {{ background-color: transparent; }}
            QMenuBar::item:selected {{ background-color: {self.accent_primary}; color: white; }}
            QMenu {{ background-color: {self.bg_secondary}; color: {self.text_primary}; border: 1px solid {self.border}; }}
            QMenu::item:selected {{ background-color: {self.accent_primary}; color: white; }}
            QTabWidget::pane {{ border: 1px solid {self.border}; }}
            QTabBar::tab {{ 
                background-color: {self.bg_secondary}; 
                color: {self.text_primary}; 
                padding: 8px 12px; 
                border-top-left-radius: 8px; 
                border-top-right-radius: 8px;
                margin-right: 2px;
                border: 1px solid {self.border};
                border-bottom: none;
            }}
            QTabBar::tab:selected {{ 
                background-color: {self.bg_tertiary}; 
                color: {self.accent_primary};
                border-bottom: none;
            }}
            QGroupBox {{ 
                border: 1px solid {self.border}; 
                border-radius: 8px; 
                margin-top: 1em; 
                background-color: {self.bg_tertiary};
                color: {self.text_primary};
                padding: 10px;
            }}
            QGroupBox::title {{ 
                subcontrol-origin: margin; 
                left: 10px; 
                padding: 0 5px; 
                color: {self.text_primary};
                font-weight: bold;
            }}
            QPushButton {{ 
                background-color: {self.bg_tertiary}; 
                color: {self.text_primary}; 
                border: 1px solid {self.accent_primary}; 
                padding: 8px 15px; 
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{ 
                background-color: {self.accent_secondary}; 
            }}
            QPushButton:pressed {{ 
                background-color: {self.accent_primary}; 
            }}
            QPushButton:disabled {{ 
                background-color: {self.bg_secondary}; 
                color: {self.disabled}; 
            }}
            QComboBox {{ 
                background-color: {self.bg_secondary}; 
                color: {self.text_primary}; 
                border: 1px solid {self.border}; 
                padding: 5px; 
                border-radius: 3px; 
            }}
            QComboBox:drop-down {{ 
                border: none; 
                width: 20px; 
            }}
            QComboBox::down-arrow {{ 
                image: none; 
                background: none; 
                border: none; 
            }}
            QComboBox QAbstractItemView {{ 
                background-color: {self.bg_secondary}; 
                color: {self.text_primary}; 
                selection-background-color: {self.accent_primary}; 
            }}
            QTextEdit, QTableWidget {{ 
                background-color: {self.bg_secondary}; 
                color: {self.text_primary}; 
                border: 1px solid {self.border}; 
                border-radius: 8px;
                selection-background-color: {self.accent_primary}; 
                selection-color: {self.text_primary}; 
            }}
            QTableWidget::item:selected {{ 
                background-color: {self.accent_primary}; 
                color: white; 
            }}
            QTableWidget {{ 
                background-color: {self.bg_secondary}; 
                color: {self.text_primary}; 
                gridline-color: {self.border}; 
                border: none; 
            }}
            QHeaderView::section {{ 
                background-color: {self.bg_tertiary}; 
                color: {self.text_primary}; 
                padding: 5px; 
                border: none; 
            }}
            QTableWidget::item {{ 
                padding: 5px; 
            }}
            QLineEdit, QSpinBox {{ 
                background-color: {self.bg_secondary}; 
                color: {self.text_primary}; 
                border: 1px solid {self.border}; 
                padding: 5px; 
                border-radius: 3px; 
            }}
            QCheckBox {{ 
                color: {self.text_primary};
            }}
            QCheckBox::indicator {{ 
                width: 15px;
                height: 15px;
                border: 1px solid {self.accent_primary};
                border-radius: 3px;
            }}
            QCheckBox::indicator:checked {{ 
                background-color: {self.accent_primary}; 
                border: 1px solid {self.accent_primary}; 
            }}
        """)
        
        # Mettre à jour le texte de l'action de thème si elle existe déjà
        # Mise à jour du style des champs de saisie CAN
        if hasattr(self, 'send_id_input') and hasattr(self, 'send_data_input') and hasattr(self, 'send_btn'):
            champ_style = f"background-color: {self.bg_secondary}; color: {self.text_primary}; border: 1px solid {self.border}; border-radius: 4px;"
            self.send_id_input.setStyleSheet(champ_style)
            self.send_data_input.setStyleSheet(champ_style)
            self.send_btn.setStyleSheet(f"background-color: {self.bg_secondary}; color: {self.text_primary}; border: 1px solid {self.border}; border-radius: 4px; padding: 5px 15px;")
        
        if hasattr(self, 'theme_action'):
            self.theme_action.setText("Mode Nuit" if not self.is_dark_mode else "Mode Jour")
    
    def init_ui(self):
        # Configuration de la fenêtre principale
        self.setWindowTitle("CAN Sniffer")
        self.setGeometry(100, 100, 1200, 800)  # Fenêtre plus grande
        
        # Variables pour les nouvelles fonctionnalités
        self.autoscroll_enabled = True
        self.frame_counter = 0
        self.favorites = []  # Liste des commandes favorites
        self.favorites_actions = []  # Actions du menu favoris
        self.filter_id = ""  # Filtre par ID
        self.throttle_delay = 0  # Délai en ms entre les trames (0 = pas de délai)
        self.last_update_time = 0  # Timestamp de la dernière mise à jour
        
        # Fichiers de configuration
        self.favorites_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "can_favorites.json")
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "can_config.json")
        
        # Configuration par défaut
        self.config = {
            "show_filter_id": True,
            "show_throttle_control": True,
            "show_autoscroll_button": True,
            "show_send_panel": True,
            "show_frame_counter": True
        }
        
        # Charger la configuration
        self.load_config()
        
        # Widget central et layout principal
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Groupe pour les contrôles du port série
        port_group = QGroupBox("Configuration du Port CAN")
        port_layout = QGridLayout()
        port_layout.setSpacing(10)
        port_layout.setContentsMargins(10, 20, 10, 10)
        
        # Sélection du port
        port_layout.addWidget(QLabel("Port:"), 0, 0)
        self.port_combo = QComboBox()
        port_layout.addWidget(self.port_combo, 0, 1)
        self.refresh_btn = QPushButton("Rafraîchir")
        self.refresh_btn.clicked.connect(self.refresh_ports)
        port_layout.addWidget(self.refresh_btn, 0, 2)
        
        # Sélection de la vitesse (baud rate)
        port_layout.addWidget(QLabel("Vitesse:"), 1, 0)
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"])
        self.baud_combo.setCurrentText("9600")  # Valeur par défaut
        port_layout.addWidget(self.baud_combo, 1, 1)
        
        # Boutons de connexion
        self.connect_btn = QPushButton("Connecter")
        self.connect_btn.clicked.connect(self.connect_to_port)
        port_layout.addWidget(self.connect_btn, 2, 0)
        
        self.disconnect_btn = QPushButton("Déconnecter")
        self.disconnect_btn.clicked.connect(self.disconnect_from_port)
        self.disconnect_btn.setEnabled(False)
        port_layout.addWidget(self.disconnect_btn, 2, 1)
        
        port_group.setLayout(port_layout)
        main_layout.addWidget(port_group)

        # Groupe pour l'envoi de trames CAN
        send_group = QGroupBox("Envoyer une trame CAN")
        send_layout = QHBoxLayout()
        send_layout.setSpacing(10)
        send_layout.setContentsMargins(10, 10, 10, 10)
        send_group.setLayout(send_layout)
        
        send_layout.addWidget(QLabel("ID (hex):"))
        self.send_id_input = QLineEdit()
        self.send_id_input.setPlaceholderText("ex: 123")
        self.send_id_input.setMaxLength(8)
        send_layout.addWidget(self.send_id_input)
        
        send_layout.addWidget(QLabel("Données (hex):"))
        self.send_data_input = QLineEdit()
        self.send_data_input.setPlaceholderText("ex: 11223344AABBCCDD")
        self.send_data_input.setMaxLength(16)
        send_layout.addWidget(self.send_data_input)
        
        self.send_btn = QPushButton("Envoyer")
        self.send_btn.clicked.connect(self.send_can_frame)
        send_layout.addWidget(self.send_btn)
        
        # Le style des champs est défini dans apply_theme

        main_layout.addWidget(send_group)
        
        # Aucun préréglage module - cet espace a été supprimé
        
        # Zone d'affichage des données reçues (beaucoup plus grande)
        data_group = QGroupBox("Trames CAN Reçues")
        data_group.setStyleSheet(f"QGroupBox {{ font-size: 14px; font-weight: bold; color: {self.accent_primary}; }}")
        data_layout = QVBoxLayout()
        data_layout.setSpacing(10)
        data_layout.setContentsMargins(10, 20, 10, 10)
        
        # Création d'un widget à onglets pour différentes vues
        self.data_tabs = QTabWidget()
        
        # Onglet 1: Vue brute (texte)
        self.raw_tab = QWidget()
        raw_layout = QVBoxLayout(self.raw_tab)
        self.data_display = QTextEdit()
        self.data_display.setReadOnly(True)
        self.data_display.setFont(QFont("Consolas", 11))  # Police plus grande
        self.data_display.setMinimumHeight(500)  # Hauteur minimale encore plus grande
        raw_layout.addWidget(self.data_display)
        
        # Onglet 2: Vue tableau
        self.table_tab = QWidget()
        table_layout = QVBoxLayout(self.table_tab)
        self.data_table = QTableWidget(0, 5)
        self.data_table.setHorizontalHeaderLabels(["Timestamp", "ID", "DLC", "Données", "ASCII"])
        self.data_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.data_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.data_table.verticalHeader().setVisible(False)
        self.data_table.setMinimumHeight(500)  # Hauteur minimale encore plus grande
        self.data_table.setFont(QFont("Consolas", 11))  # Police plus grande
        self.data_table.horizontalHeader().setFont(QFont("Consolas", 11, QFont.Weight.Bold))
        # Ajuster les largeurs des colonnes
        self.data_table.setColumnWidth(0, 120)  # Timestamp
        self.data_table.setColumnWidth(1, 80)   # ID
        self.data_table.setColumnWidth(2, 60)   # DLC
        table_layout.addWidget(self.data_table)
        
        # Ajout des onglets
        self.data_tabs.addTab(self.raw_tab, "Données Brutes")
        self.data_tabs.addTab(self.table_tab, "Vue Tableau")
        
        data_layout.addWidget(self.data_tabs)
        
        # Boutons pour la gestion des données
        btn_layout = QHBoxLayout()
        
        # Bouton effacer
        self.clear_btn = QPushButton("Effacer")
        self.clear_btn.clicked.connect(self.clear_data)
        btn_layout.addWidget(self.clear_btn)
        
        # Bouton enregistrer
        self.save_btn = QPushButton("Enregistrer")
        self.save_btn.clicked.connect(self.save_data)
        btn_layout.addWidget(self.save_btn)
        
        # Ajout des nouveaux contrôles
        # Autoscroll toggle
        self.autoscroll_btn = QPushButton("Autoscroll: ON")
        self.autoscroll_btn.setCheckable(True)
        self.autoscroll_btn.setChecked(True)
        self.autoscroll_btn.clicked.connect(self.toggle_autoscroll)
        btn_layout.addWidget(self.autoscroll_btn)
        
        # Compteur de trames
        counter_layout = QHBoxLayout()
        counter_layout.addWidget(QLabel("Trames reçues:"))
        self.frame_count_label = QLabel("0")
        self.frame_count_label.setStyleSheet("font-weight: bold;")
        counter_layout.addWidget(self.frame_count_label)
        
        # Contrôle de vitesse d'affichage
        throttle_layout = QHBoxLayout()
        throttle_layout.addWidget(QLabel("Vitesse d'affichage:"))
        self.throttle_slider = QSlider(Qt.Orientation.Horizontal)
        self.throttle_slider.setMinimum(0)
        self.throttle_slider.setMaximum(1000)  # Jusqu'à 1 seconde de délai
        self.throttle_slider.setValue(0)
        self.throttle_slider.setTickInterval(100)
        self.throttle_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.throttle_slider.valueChanged.connect(self.set_throttle_delay)
        throttle_layout.addWidget(self.throttle_slider)
        
        self.throttle_value_label = QLabel("0 ms")
        throttle_layout.addWidget(self.throttle_value_label)
        
        # Filtrage par ID
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrer par ID:"))
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("ex: 123 (laisser vide = tous)")
        self.filter_input.textChanged.connect(self.set_id_filter)
        filter_layout.addWidget(self.filter_input)
        
        # Ajout des nouveaux layouts
        data_layout.addLayout(btn_layout)
        data_layout.addLayout(counter_layout)
        data_layout.addLayout(throttle_layout)
        data_layout.addLayout(filter_layout)
        data_group.setLayout(data_layout)
        main_layout.addWidget(data_group)
        
        # Barre de statut
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")
        
        # Définir les proportions du layout principal
        # Donner plus d'espace à la zone d'affichage des trames
        main_layout.setStretch(0, 1)  # Configuration du port
        main_layout.setStretch(1, 1)  # Envoi de trame
        main_layout.setStretch(2, 8)  # Trames CAN reçues (8x plus d'espace)
        
        # Finalisation de l'interface
        self.setCentralWidget(central_widget)
        
        # Initialisation des ports disponibles
        self.refresh_ports()
    
    def refresh_ports(self):
        """Rafraîchit la liste des ports série disponibles."""
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(f"{port.device} - {port.description}")
        
        if self.port_combo.count() == 0:
            self.status_bar.showMessage("Aucun port série détecté")
            self.connect_btn.setEnabled(False)
        else:
            self.status_bar.showMessage("Ports série détectés")
            self.connect_btn.setEnabled(True)
    
    def connect_to_port(self):
        """Se connecte au port série sélectionné."""
        if self.port_combo.currentText():
            try:
                port_name = self.port_combo.currentText().split(" - ")[0]
                baud_rate = int(self.baud_combo.currentText())
                
                self.serial_port = serial.Serial(port_name, baud_rate, timeout=0.1)
                
                self.reader_thread.set_serial_port(self.serial_port)
                self.reader_thread.start()
                
                self.connect_btn.setEnabled(False)
                self.disconnect_btn.setEnabled(True)
                self.port_combo.setEnabled(False)
                self.baud_combo.setEnabled(False)
                
                self.status_bar.showMessage(f"Connecté à {port_name} à {baud_rate} bauds")
                self.data_display.append(f"--- Connecté à {port_name} à {baud_rate} bauds ---\n")
            except Exception as e:
                self.status_bar.showMessage(f"Erreur de connexion: {str(e)}")
                self.data_display.append(f"Erreur de connexion: {str(e)}\n")
    
    def disconnect_from_port(self):
        """Se déconnecte du port série."""
        if self.reader_thread.isRunning():
            self.reader_thread.stop()
        
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.serial_port = None
        
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.port_combo.setEnabled(True)
        self.baud_combo.setEnabled(True)
        
        self.status_bar.showMessage("Déconnecté")
        self.data_display.append("--- Déconnecté ---\n")
    
    def update_received_data(self, data):
        """Met à jour l'affichage avec les données reçues."""
        # Vérifier le throttling
        current_time = int(time.time() * 1000)  # Temps en millisecondes
        if current_time - self.last_update_time < self.throttle_delay:
            # Si le délai n'est pas passé, ne pas afficher cette trame
            return
        self.last_update_time = current_time
        
        # Mise à jour de l'affichage texte
        self.data_display.append(data)
        
        # Auto-scroll vers le bas si activé
        if self.autoscroll_enabled:
            scrollbar = self.data_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        
        # Tentative de parser les données comme une trame CAN
        try:
            # Exemple de format simple: "ID:123 DLC:8 DATA:0102030405060708"
            # Cette partie doit être adaptée au format réel de vos trames
            parts = data.strip().split()
            if len(parts) >= 3 and parts[0].startswith("ID:") and parts[1].startswith("DLC:"):
                can_id = parts[0].split(":")[1]
                dlc = parts[1].split(":")[1]
                hex_data = parts[2].split(":")[1]
                
                # Conversion des données hex en ASCII pour affichage
                ascii_repr = ""
                try:
                    for i in range(0, len(hex_data), 2):
                        byte = int(hex_data[i:i+2], 16)
                        if 32 <= byte <= 126:  # Caractères ASCII imprimables
                            ascii_repr += chr(byte)
                        else:
                            ascii_repr += "."
                except:
                    ascii_repr = "<non-ASCII>"
                
                # Ajout à la table
                row_position = self.data_table.rowCount()
                self.data_table.insertRow(row_position)
                
                import datetime
                timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
                
                self.data_table.setItem(row_position, 0, QTableWidgetItem(timestamp))
                self.data_table.setItem(row_position, 1, QTableWidgetItem(can_id))
                self.data_table.setItem(row_position, 2, QTableWidgetItem(dlc))
                self.data_table.setItem(row_position, 3, QTableWidgetItem(hex_data))
                self.data_table.setItem(row_position, 4, QTableWidgetItem(ascii_repr))
                
                # Incrémenter le compteur de trames
                self.frame_counter += 1
                self.frame_count_label.setText(str(self.frame_counter))
                
                # Auto-scroll de la table si activé
                if self.autoscroll_enabled:
                    self.data_table.scrollToBottom()
                
                # Appliquer le filtre si nécessaire
                if self.filter_id and can_id.lower() != self.filter_id.lower():
                    # Cacher la ligne si elle ne correspond pas au filtre
                    self.data_table.setRowHidden(row_position, True)
        except Exception as e:
            # Si le parsing échoue, on ne fait rien de plus
            pass
    def clear_data(self):
        """Efface les données affichées."""
        self.data_display.clear()
        self.data_table.setRowCount(0)
        # Ne pas réinitialiser le compteur
    
    def save_data(self):
        """Enregistre les données dans un fichier."""
        from PyQt6.QtWidgets import QFileDialog
        from datetime import datetime
        
        # Déterminer quel onglet est actif pour savoir quel format d'export utiliser
        current_tab = self.data_tabs.currentIndex()
        
        if current_tab == 0:  # Onglet texte brut
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                "Enregistrer les données", 
                f"can_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "Fichiers texte (*.txt)"
            )
            
            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(self.data_display.toPlainText())
                    self.status_bar.showMessage(f"Données enregistrées dans {filename}")
                except Exception as e:
                    self.status_bar.showMessage(f"Erreur lors de l'enregistrement: {str(e)}")
        
        elif current_tab == 1:  # Onglet tableau
            filename, filter_type = QFileDialog.getSaveFileName(
                self, 
                "Enregistrer les données", 
                f"can_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "Fichiers CSV (*.csv);;Fichiers texte (*.txt)"
            )
            
            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        # Écrire l'en-tête
                        headers = []
                        for col in range(self.data_table.columnCount()):
                            headers.append(self.data_table.horizontalHeaderItem(col).text())
                        f.write(','.join(headers) + '\n')
                        
                        # Écrire les données
                        for row in range(self.data_table.rowCount()):
                            row_data = []
                            for col in range(self.data_table.columnCount()):
                                item = self.data_table.item(row, col)
                                if item is not None:
                                    # Échapper les virgules dans les cellules
                                    cell_text = item.text().replace(',', ',')
                                    row_data.append(cell_text)
                                else:
                                    row_data.append('')
                            f.write(','.join(row_data) + '\n')
                    
                    self.status_bar.showMessage(f"Données enregistrées dans {filename}")
                except Exception as e:
                    self.status_bar.showMessage(f"Erreur lors de l'enregistrement: {str(e)}")
    
    def closeEvent(self, event):
        """Gère la fermeture de l'application."""
        self.disconnect_from_port()
        event.accept()

    def send_can_frame(self):
        """Envoie une trame CAN sur le bus via le port série."""
        can_id = self.send_id_input.text().strip()
        data = self.send_data_input.text().strip()
        if not can_id or not all(c in '0123456789ABCDEFabcdef' for c in can_id):
            self.status_bar.showMessage("ID CAN invalide (hex)")
            return
        if not data or not all(c in '0123456789ABCDEFabcdef' for c in data):
            self.status_bar.showMessage("Données CAN invalides (hex)")
            return
        if len(data) % 2 != 0 or len(data) > 16:
            self.status_bar.showMessage("Données: longueur paire, max 8 octets")
            return
        if not self.serial_port or not self.serial_port.is_open:
            self.status_bar.showMessage("Port non connecté")
            return
            
        # Convertir les données hex en bytes
        data_bytes = bytearray.fromhex(data)
        
        try:
            # Envoyer les données brutes
            self.serial_port.write(data_bytes)
            self.status_bar.showMessage(f"Trame envoyée: {data.upper()}")
            self.data_display.append(f"[ENVOYÉ] ID:{can_id} DATA:{data.upper()}")
            
            # Ajout dans la vue tableau
            from datetime import datetime
            row = self.data_table.rowCount()
            self.data_table.insertRow(row)
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            self.data_table.setItem(row, 0, QTableWidgetItem(timestamp))
            self.data_table.setItem(row, 1, QTableWidgetItem(can_id.upper()))
            self.data_table.setItem(row, 2, QTableWidgetItem(str(len(data_bytes))))
            self.data_table.setItem(row, 3, QTableWidgetItem(data.upper()))
            
            # ASCII
            ascii_data = ''.join([chr(b) if 32 <= b <= 126 else '.' for b in data_bytes])
            self.data_table.setItem(row, 4, QTableWidgetItem("[ENVOYÉ] " + ascii_data))
            self.data_table.scrollToBottom()
        except Exception as e:
            self.status_bar.showMessage(f"Erreur d'envoi: {str(e)}")

    def _send_formatted_can_frame(self, can_id, data_bytes):
        """Méthode interne pour envoyer une trame CAN formatée."""
        # Convertir les données en chaîne hexadécimale
        data_hex = ''.join([f"{b:02X}" for b in data_bytes])
        # Pré-remplir les champs d'envoi pour référence
        self.send_id_input.setText(can_id)
        self.send_data_input.setText(data_hex)
        
        # Format de trame simple - juste envoyer les données brutes
        # D'après l'image, le format semble être simplement les octets sans format SLCAN
        raw_bytes = bytes(data_bytes)
        
        if not self.serial_port or not self.serial_port.is_open:
            self.status_bar.showMessage("Port non connecté")
            return False
        
        try:
            # Envoyer les données brutes
            self.serial_port.write(raw_bytes)
            self.status_bar.showMessage(f"Trame envoyée: {data_hex}")
            self.data_display.append(f"[ENVOYÉ] ID:{can_id} DATA:{data_hex}")
            
            # Ajout dans la vue tableau
            from datetime import datetime
            row = self.data_table.rowCount()
            self.data_table.insertRow(row)
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            self.data_table.setItem(row, 0, QTableWidgetItem(timestamp))
            self.data_table.setItem(row, 1, QTableWidgetItem(can_id.upper()))
            self.data_table.setItem(row, 2, QTableWidgetItem(str(len(data_bytes))))
            self.data_table.setItem(row, 3, QTableWidgetItem(data_hex.upper()))
            
            # ASCII
            ascii_data = ''.join([chr(b) if 32 <= b <= 126 else '.' for b in data_bytes])
            self.data_table.setItem(row, 4, QTableWidgetItem("[ENVOYÉ] " + ascii_data))
            self.data_table.scrollToBottom()
            return True
        except Exception as e:
            self.status_bar.showMessage(f"Erreur d'envoi: {str(e)}")
            return False

    def send_eclairage_cmd(self):
        """Envoie une commande au module Éclairage (ID: 0x45)."""
        # Récupérer les valeurs des contrôles
        cmd_idx = self.ec_cmd_combo.currentIndex()
        niveau = self.ec_niv_spin.value()
        
        # D'après l'image:
        # 1) 0x45 - ID du module éclairage
        # 2) ec_cmd: (0-5) 1 pour matrice, 2 pour LED 1, 3 pour LED 2
        # 3) ec_niv: (0-15) moduler le niveau d'éclairage de la matrice
        # 4) 0x0D - terminaison
        
        # Construire les données - format selon l'image
        # On ajoute 0x0D à la fin comme indiqué
        data_bytes = [cmd_idx, niveau, 0x0D]
        
        # Envoyer la trame
        if self._send_formatted_can_frame("45", data_bytes):
            cmd_str = "Off" if cmd_idx == 0 else "LED 1" if cmd_idx == 1 else "LED 2" if cmd_idx == 2 else "LED 1+2"
            self.status_bar.showMessage(f"Commande Éclairage envoyée: {cmd_str}, Niveau={niveau}")

    def send_correction_cmd(self):
        """Envoie une commande au module Correction (ID: 0x4C)."""
        # Récupérer les valeurs des contrôles
        mode_text = self.cor_mode_combo.currentText()
        mode = int(mode_text.split(":")[0])  # Extraire le nombre avant ":" 
        seuil = self.cor_seuil_spin.value()
        periode = self.cor_per_spin.value()
        
        # D'après l'image:
        # 1) 0x4C - ID du module correction
        # 2) (0-2): 0 manuel, 2 automatique
        # 3) cor_seuil: (0-15) écart de la luminosité qui justifie une correction
        # 4) cor_per: (0-15) périodicité en mn des corrections
        # 5) 0x0D - terminaison
        
        # Construire les données - format selon l'image
        # On ajoute 0x0D à la fin comme indiqué
        data_bytes = [mode, seuil, periode, 0x0D]
        
        # Envoyer la trame
        if self._send_formatted_can_frame("4C", data_bytes):
            mode_str = "Manuel" if mode == 0 else "Automatique"
            self.status_bar.showMessage(f"Commande Correction envoyée: Mode={mode_str}, Seuil={seuil}, Période={periode}mn")

    def send_moteur_cmd(self):
        """Envoie une commande au module Moteur (ID: 0x4B)."""
        # Récupérer les valeurs des contrôles
        sens_text = self.mot_sens_combo.currentText()
        sens = int(sens_text.split(":")[0])  # Extraire le nombre avant ":"
        duree = self.mot_duree_spin.value()
        park_text = self.mot_park_combo.currentText()
        park = int(park_text.split(":")[0])  # Extraire le nombre avant ":"
        
        # D'après l'image:
        # 1) élévation / azimut: 0x4B - ID du module moteur
        # 2) mot_e_sens: (0-2) sens de déplacement
        # 3) mot_e_duree: (0-10) durée de déplacement en secondes
        # 4) park: (0-1) indicateur pour demande parking
        # 5) 0x0D - terminaison
        
        # Construire les données - format selon l'image
        # On ajoute 0x0D à la fin comme indiqué
        data_bytes = [sens, duree, park, 0x0D]
        
        # Envoyer la trame
        if self._send_formatted_can_frame("4B", data_bytes):
            sens_str = "Horaire" if sens == 0 else "Anti-horaire" if sens == 1 else "Alterné"
            park_str = "Oui" if park == 1 else "Non"
            self.status_bar.showMessage(f"Commande Moteur envoyée: Sens={sens_str}, Durée={duree}s, Parking={park_str}")


    def toggle_autoscroll(self):
        """Active ou désactive le défilement automatique."""
        self.autoscroll_enabled = not self.autoscroll_enabled
        self.autoscroll_btn.setText(f"Autoscroll: {'ON' if self.autoscroll_enabled else 'OFF'}")

    def set_throttle_delay(self, value):
        """Définit le délai entre les affichages de trames."""
        self.throttle_delay = value
        self.throttle_value_label.setText(f"{value} ms")

    def set_id_filter(self, filter_text):
        """Définit le filtre d'ID CAN."""
        self.filter_id = filter_text.strip()
        # Réappliquer le filtre sur toutes les lignes existantes
        for row in range(self.data_table.rowCount()):
            id_item = self.data_table.item(row, 1)
            if id_item:
                can_id = id_item.text()
                if self.filter_id and can_id.lower() != self.filter_id.lower():
                    self.data_table.setRowHidden(row, True)
                else:
                    self.data_table.setRowHidden(row, False)

    def add_to_favorites(self):
        """Ajoute la commande actuelle aux favoris."""
        can_id = self.send_id_input.text().strip()
        data = self.send_data_input.text().strip()

        if not can_id or not data:
            self.status_bar.showMessage("Remplissez d'abord les champs ID et Données")
            return

        # Créer un nom pour cette commande
        from PyQt6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "Ajouter aux favoris", "Nom de cette commande:")

        if ok and name:
            # Créer l'action pour le menu
            favorite_action = QAction(f"{name} (ID:{can_id}, Data:{data})", self)
            
            # Créer une closure pour cette commande spécifique
            def send_favorite_command():
                self.send_id_input.setText(can_id)
                self.send_data_input.setText(data)
                self.send_can_frame()
            
            favorite_action.triggered.connect(send_favorite_command)
            self.favorites_menu.addAction(favorite_action)
            self.favorites_actions.append(favorite_action)
            
            # Stocker dans la liste des favoris
            new_favorite = {"name": name, "can_id": can_id, "data": data}
            self.favorites.append(new_favorite)
            self.status_bar.showMessage(f"Commande '{name}' ajoutée aux favoris")
            
            # Sauvegarder les favoris
            self.save_favorites()
    
    def manage_favorites(self):
        """Gérer les favoris (supprimer, réorganiser, etc.)"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QListWidgetItem
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Gérer les favoris")
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Liste des favoris
        list_widget = QListWidget()
        for favorite in self.favorites:
            item = QListWidgetItem(f"{favorite['name']} (ID:{favorite['can_id']}, Data:{favorite['data']}")
            item.setData(Qt.ItemDataRole.UserRole, favorite)
            list_widget.addItem(item)
        
        layout.addWidget(QLabel("Sélectionnez un favori à supprimer:"))
        layout.addWidget(list_widget)
        
        # Boutons
        button_layout = QHBoxLayout()
        
        delete_btn = QPushButton("Supprimer")
        button_layout.addWidget(delete_btn)
        
        close_btn = QPushButton("Fermer")
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        # Connecter les actions
        close_btn.clicked.connect(dialog.accept)
        
        def delete_favorite():
            selected_items = list_widget.selectedItems()
            if not selected_items:
                return
                
            for item in selected_items:
                selected_index = list_widget.row(item)
                favorite_data = self.favorites[selected_index]
                
                # Supprimer de la liste des favoris
                del self.favorites[selected_index]
                
                # Supprimer l'action du menu
                action_to_remove = self.favorites_actions[selected_index]
                self.favorites_menu.removeAction(action_to_remove)
                del self.favorites_actions[selected_index]
                
                list_widget.takeItem(selected_index)
                
                self.status_bar.showMessage(f"Favori '{favorite_data['name']}' supprimé")
            
            # Sauvegarder les changements
            self.save_favorites()
        
        delete_btn.clicked.connect(delete_favorite)
        
        dialog.exec()
    
    def save_favorites(self):
        """Sauvegarde les favoris dans un fichier JSON."""
        try:
            with open(self.favorites_file, 'w') as f:
                json.dump(self.favorites, f, indent=2)
        except Exception as e:
            self.status_bar.showMessage(f"Erreur lors de la sauvegarde des favoris: {str(e)}")
    
    def load_favorites(self):
        """Charge les favoris depuis un fichier JSON."""
        if not os.path.exists(self.favorites_file):
            return
            
        try:
            with open(self.favorites_file, 'r') as f:
                self.favorites = json.load(f)
                
            # Ajouter les favoris au menu
            for favorite in self.favorites:
                name = favorite['name']
                can_id = favorite['can_id']
                data = favorite['data']
                
                # Créer l'action
                favorite_action = QAction(f"{name} (ID:{can_id}, Data:{data})", self)
                
                # Créer une closure pour cette commande
                def create_send_command(id_val, data_val):
                    def send_cmd():
                        self.send_id_input.setText(id_val)
                        self.send_data_input.setText(data_val)
                        self.send_can_frame()
                    return send_cmd
                
                favorite_action.triggered.connect(create_send_command(can_id, data))
                self.favorites_menu.addAction(favorite_action)
                self.favorites_actions.append(favorite_action)
        except Exception as e:
            self.status_bar.showMessage(f"Erreur lors du chargement des favoris: {str(e)}")


    def show_ui_config_dialog(self):
        """Affiche la boîte de dialogue de configuration de l'interface."""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton, QHBoxLayout
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Configuration de l'interface")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # Créer les options de configuration
        checkboxes = {}
        
        # Option: Afficher le filtre par ID
        filter_id_cb = QCheckBox("Afficher le filtre par ID")
        filter_id_cb.setChecked(self.config["show_filter_id"])
        layout.addWidget(filter_id_cb)
        checkboxes["show_filter_id"] = filter_id_cb
        
        # Option: Afficher le contrôle de vitesse
        throttle_cb = QCheckBox("Afficher le contrôle de vitesse d'affichage")
        throttle_cb.setChecked(self.config["show_throttle_control"])
        layout.addWidget(throttle_cb)
        checkboxes["show_throttle_control"] = throttle_cb
        
        # Option: Afficher le bouton autoscroll
        autoscroll_cb = QCheckBox("Afficher le bouton autoscroll")
        autoscroll_cb.setChecked(self.config["show_autoscroll_button"])
        layout.addWidget(autoscroll_cb)
        checkboxes["show_autoscroll_button"] = autoscroll_cb
        
        # Option: Afficher le panneau d'envoi
        send_panel_cb = QCheckBox("Afficher le panneau d'envoi de trames")
        send_panel_cb.setChecked(self.config["show_send_panel"])
        layout.addWidget(send_panel_cb)
        checkboxes["show_send_panel"] = send_panel_cb
        
        # Option: Afficher le compteur de trames
        frame_counter_cb = QCheckBox("Afficher le compteur de trames")
        frame_counter_cb.setChecked(self.config["show_frame_counter"])
        layout.addWidget(frame_counter_cb)
        checkboxes["show_frame_counter"] = frame_counter_cb
        
        # Boutons OK/Annuler
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("Appliquer")
        cancel_btn = QPushButton("Annuler")
        
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        # Connecter les actions
        cancel_btn.clicked.connect(dialog.reject)
        
        def apply_config():
            # Mettre à jour la configuration
            for key, checkbox in checkboxes.items():
                self.config[key] = checkbox.isChecked()
            
            # Appliquer les changements
            self.apply_ui_config()
            
            # Sauvegarder
            self.save_config()
            dialog.accept()
        
        ok_btn.clicked.connect(apply_config)
        
        dialog.exec()
    
    def apply_ui_config(self):
        """Applique la configuration de l'interface utilisateur."""
        # Panneau d'envoi
        send_group_index = 1
        if send_group_index < len(self.findChildren(QGroupBox)):
            send_group = self.findChildren(QGroupBox)[send_group_index]
            send_group.setVisible(self.config["show_send_panel"])
        
        # Filtre par ID
        if hasattr(self, 'filter_input'):
            self.filter_input.parentWidget().setVisible(self.config["show_filter_id"])
        
        # Contrôle de vitesse
        if hasattr(self, 'throttle_slider'):
            throttle_layout = self.throttle_slider.parentWidget()
            if throttle_layout:
                throttle_layout.setVisible(self.config["show_throttle_control"])
        
        # Bouton autoscroll
        if hasattr(self, 'autoscroll_btn'):
            self.autoscroll_btn.setVisible(self.config["show_autoscroll_button"])
        
        # Compteur de trames
        if hasattr(self, 'frame_count_label'):
            counter_layout = self.frame_count_label.parentWidget()
            if counter_layout:
                counter_layout.setVisible(self.config["show_frame_counter"])
    
    def load_config(self):
        """Charge la configuration depuis un fichier JSON."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Mettre à jour uniquement les clés existantes
                    for key, value in loaded_config.items():
                        if key in self.config:
                            self.config[key] = value
            except Exception as e:
                self.status_bar.showMessage(f"Erreur lors du chargement de la configuration: {str(e)}")
    
    def save_config(self):
        """Sauvegarde la configuration dans un fichier JSON."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            self.status_bar.showMessage("Configuration sauvegardée")
        except Exception as e:
            self.status_bar.showMessage(f"Erreur lors de la sauvegarde de la configuration: {str(e)}")
    
    def reset_config(self):
        """Réinitialise la configuration aux valeurs par défaut."""
        self.config = {
            "show_filter_id": True,
            "show_throttle_control": True,
            "show_autoscroll_button": True,
            "show_send_panel": True,
            "show_frame_counter": True
        }
        self.apply_ui_config()
        self.save_config()
        self.status_bar.showMessage("Configuration réinitialisée")


def main():
    app = QApplication(sys.argv)
    serial_monitor = SerialMonitorApp()
    serial_monitor.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
