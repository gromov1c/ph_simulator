"""
Main Application for the pH Calculator.
"""
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QRadioButton,
                               QButtonGroup, QFrame, QSlider, QTextEdit)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QPoint, QEasingCurve
from PySide6.QtGui import QFont, QPixmap, QMouseEvent, QGuiApplication, QTextBlockFormat
from calculations import *
from models import (ASH_GREY, ASHIER_GREY, CAMBRIDGE_BLUE, BLACK, CONCENTRATION_VALUES,
                   BUFFER_CONCENTRATION_VALUES, PH_COLORS, BUFFER_NAME_MAPPING,
                   BUFFER_PKA_VALUES)
from models import BURNT_ORANGE
from resource_manager import ResourceManager


class pHCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize resource manager
        self.resource_manager = ResourceManager()

        # Initialize state variables
        self.drop_counter = 0
        self.solution_volume = 10
        self.probe_inserted = False
        self.solution_selected = False
        self.current_ph_value = 7
        self.startup_screen_active = True

        # Get the screen geometry for responsive positioning
        self.screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        self.screen_width = self.screen_geometry.width()
        self.screen_height = self.screen_geometry.height()

        # Set scaling factors based on screen resolution
        self.width_factor = min(1.0, (self.screen_width / 1200) / 1.05)
        self.height_factor = min(1.0, (self.screen_height / 800) / 1.05)
        self.scale_factor = min(self.width_factor, self.height_factor)

        # Set window properties
        self.setWindowTitle("pH Calculator")

        # Calculate scaled window size
        scaled_width = int(1200 * self.scale_factor)
        scaled_height = int(800 * self.scale_factor)
        self.setFixedSize(scaled_width, scaled_height)

        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set background color
        self.central_widget.setStyleSheet(f"background-color: {ASH_GREY};")

        # Show startup screen first
        self.setup_startup_screen()

    def setup_startup_screen(self):
        """Set up the startup screen with title, description and start button."""
        # Create startup layout
        self.startup_layout = QVBoxLayout(self.central_widget)
        self.startup_layout.setContentsMargins(50, 50, 50, 50)
        self.startup_layout.setSpacing(0)
        
        # Title label
        title_label = QLabel("pH Simulation")
        title_font = QFont("Calibri", int(40 * self.scale_factor), QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {BLACK}; margin-bottom: 20px;")
        
        # Description text
        description_text = QLabel()
        description_text.setStyleSheet(f"background-color: {ASHIER_GREY}; border: 2px solid black; border-radius: 10px; padding: 15px; color: {BLACK};")
        description_text.setFont(QFont("Calibri", int(18 * self.scale_factor), ))
        description_text.setWordWrap(True)
        description_text.setAlignment(Qt.AlignCenter)
        description_text.setText(f"""
            <div>
                This application simulates using a pH probe and a meter to measure the pH of various
                Acids, Bases, Salts, Buffers, Household items, and Water. It is used to illustrate how the pH
                is affected by having strong or weak acids and bases, the effects of concentration, the pH
                of salts of weak acids or bases, and how buffers maintain pH when strong acid or base is
                added. The pH given is idealized based on the concentration and dissociation constants
                for any weak acids or bases. For household items the pH is for a typical product. The
                concentration for any solution ranges up to 0.1 Molar, which may exceed the solubility of
                the compound, such as for calcium hydroxide. Drops of strong acid or base can be added
                to the buffers and water to see any effect on the pH. For the buffers, the Henderson-
                Hasselbalch equation is used for the pH, and may not be valid near the buffer capacity.
            </div>
        """)
        
        # Start button container for centering
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        
        # Start button
        start_button = QPushButton("Start")
        start_button.setFixedSize(int(150 * self.scale_factor), int(40 * self.scale_factor))
        start_button.setFont(QFont("Calibri", int(14 * self.scale_factor), QFont.Bold))
        start_button.setStyleSheet(f"background-color: {BURNT_ORANGE}; color: {BLACK}; border: 2px solid black; border-radius: 10px;")
        start_button.clicked.connect(self.start_main_application)
        
        # Add the start button to its container layout (centered)
        button_layout.addStretch()
        button_layout.addWidget(start_button)
        button_layout.addStretch()
        
        # Add widgets to the startup layout
        self.startup_layout.addStretch()
        self.startup_layout.addWidget(title_label)
        self.startup_layout.addWidget(description_text)
        self.startup_layout.addWidget(button_container)
        self.startup_layout.addStretch()
        
        # Create copyright label
        copyright_label = QLabel("Made by: Ronald Ruszczyk, Ryder Selikow, Nicholas Dill, Igor Gromovic, Andrew Fletcher @ Lewis & Clark College", self.central_widget)
        copyright_label.setGeometry(
            int(650 * self.scale_factor),
            int(780 * self.scale_factor),
            int(550 * self.scale_factor),
            int(20 * self.scale_factor)
        )
        copyright_label.setFont(QFont("Calibri", int(8 * self.scale_factor)))
        copyright_label.setStyleSheet("color: black; background-color: transparent;")

    def start_main_application(self):
        """Transition from startup screen to the main application."""
        # Clear the startup screen
        self.startup_screen_active = False
        
        # Remove all widgets from the central widget layout
        while self.startup_layout.count():
            item = self.startup_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Delete the startup layout
        self.startup_layout.deleteLater()
        
        # Create a clean slate - remove existing central widget and create a new one
        self.central_widget.deleteLater()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Set background color again for the new central widget
        self.central_widget.setStyleSheet(f"background-color: {ASH_GREY};")
        
        # Initialize the main application UI
        self.initialize_gui()

    def initialize_gui(self):
        """Initialize all GUI components and set up the UI."""
        # Load images
        self.load_images()

        # Create UI components
        self.setup_primary_ui_components()

        # Set up frames and layouts
        self.setup_frames()

        # Initialize data and values
        self.initialize_data()

        # Set up controls and radio buttons
        self.setup_radio_buttons()

        # Connect signals
        self.connect_signals()

        # Style
        self.setStyleSheet(
            f"""
            .bordered_frames {{
                background-color: {ASHIER_GREY}; 
                border: 2px solid black; 
                border-radius: 20px;
            }}
            """
        )
        
        # Create copyright label in the top corner
        self.copyright_label = QLabel("Made by: Ronald Ruszczyk, Ryder Selikow, Nicholas Dill, Igor Gromovic, Andrew Fletcher @ Lewis & Clark College", self.central_widget)
        self.copyright_label.setGeometry(
            int(650 * self.scale_factor),
            int(780 * self.scale_factor),
            int(550 * self.scale_factor),
            int(20 * self.scale_factor)
        )
        self.copyright_label.setFont(QFont("Calibri", int(8 * self.scale_factor)))
        self.copyright_label.setStyleSheet("color: black; background-color: transparent;")

    def setup_frames(self):
        """Set up the frames and layouts for different categories."""
        # Create category buttons frame - apply scaling
        self.category_frame = QFrame(self.central_widget)
        self.category_frame.setGeometry(
            int(30 * self.scale_factor),
            int(500 * self.scale_factor),
            int(170 * self.scale_factor),
            int(180 * self.scale_factor)
        )
        self.category_frame.setStyleSheet(f"background-color: {ASHIER_GREY};")
        self.category_frame.setProperty("class", "bordered_frames")


        # Create acids/bases button frame - apply scaling
        self.acids_bases_frame = QFrame(self.central_widget)
        self.acids_bases_frame.setGeometry(
            int(210 * self.scale_factor),
            int(500 * self.scale_factor),
            int(400 * self.scale_factor),
            int(280 * self.scale_factor)
        )
        self.acids_bases_frame.setStyleSheet(f"background-color: {ASHIER_GREY}; border-radius: 20px;")
        self.acids_bases_frame.setProperty("class", "bordered_frames")

        # Create slider frame - apply scaling
        self.slider_frame = QFrame(self.central_widget)

        self.slider_frame.setGeometry(
            int(810 * self.scale_factor),
            int(500 * self.scale_factor),
            int(300 * self.scale_factor),
            int(100 * self.scale_factor)
        )
        self.slider_frame.setStyleSheet(f"background-color: {ASHIER_GREY};")
        self.slider_frame.setProperty("class", "bordered_frames")

        # Create salts button frame - apply scaling
        self.salts_frame = QFrame(self.central_widget)
        self.salts_frame.setGeometry(
            int(210 * self.scale_factor),
            int(500 * self.scale_factor),
            int(400 * self.scale_factor),
            int(280 * self.scale_factor)
        )
        self.salts_frame.setStyleSheet(f"background-color: {ASHIER_GREY};")
        self.salts_frame.setProperty("class", "bordered_frames")
        self.salts_frame.hide()  # Initially hidden

        # Create buffers button frame - apply scaling
        self.buffers_frame = QFrame(self.central_widget)
        self.buffers_frame.setGeometry(
            int(205 * self.scale_factor),
            int(500 * self.scale_factor),
            int(600 * self.scale_factor),
            int(280 * self.scale_factor)
        )
        self.buffers_frame.setStyleSheet(f"background-color: {ASHIER_GREY};")
        self.buffers_frame.setProperty("class", "bordered_frames")
        self.buffers_frame.hide()  # Initially hidden

        # Create household button frame - apply scaling
        self.household_items_frame = QFrame(self.central_widget)
        self.household_items_frame.setGeometry(
            int(210 * self.scale_factor),
            int(500 * self.scale_factor),
            int(700 * self.scale_factor),
            int(280 * self.scale_factor)
        )
        self.household_items_frame.setStyleSheet(f"background-color: {ASHIER_GREY}; border-radius: 20px;")
        self.household_items_frame.setProperty("class", "bordered_frames")
        self.household_items_frame.hide()  # Initially hidden

        # Create water button frame - apply scaling
        self.water_frame = QFrame(self.central_widget)
        self.water_frame.setGeometry(
            int(210 * self.scale_factor),
            int(500 * self.scale_factor),
            int(400 * self.scale_factor),
            int(280 * self.scale_factor)
        )
        self.water_frame.setStyleSheet(f"background-color: {ASHIER_GREY};")
        self.water_frame.setProperty("class", "bordered_frames")
        self.water_frame.hide()  # Initially hidden

        # Create drops button frame - apply scaling
        self.drops_frame = QFrame(self.central_widget)
        self.drops_frame.setGeometry(
            int(925 * self.scale_factor),
            int(225 * self.scale_factor),
            int(200 * self.scale_factor),
            int(200 * self.scale_factor)
        )
        self.drops_frame.setStyleSheet(f"background-color: {ASHIER_GREY};")
        self.drops_frame.setProperty("class", "bordered_frames")
        self.drops_frame.hide()
        self.drops_added_label.hide()

        # Create layouts for the frames
        self.setup_layouts()

    def setup_primary_ui_components(self):
        """Set up the primary UI components like labels and buttons."""
        # Create image label with scaling
        self.image_label = QLabel(self.central_widget)
        self.image_label.setGeometry(
            int(-20 * self.scale_factor),
            int(-30 * self.scale_factor),
            int(950 * self.scale_factor),
            int(600 * self.scale_factor)
        )
        # Scale the pixmap with smooth transformation
        scaled_pixmap = self.ph_meter_empty_outside.scaled(
            int(self.ph_meter_empty_outside.width() * self.scale_factor),
            int(self.ph_meter_empty_outside.height() * self.scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Create dropper label with scaling
        self.dropper_label = QLabel(self.central_widget)
        self.dropper_label.setGeometry(
            int(755 * self.scale_factor),
            int(0 * self.scale_factor),
            int(120 * self.scale_factor),
            int(120 * self.scale_factor)
        )
        self.dropper_label.setPixmap(self.dropperPix.scaled(
            int(120 * self.scale_factor),
            int(120 * self.scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        self.dropper_label.setAlignment(Qt.AlignCenter)
        self.dropper_label.hide()

        # Create solution volume label with absolute positioning and scaling
        self.solution_volume_label = QLabel(f"Solution volume: {self.solution_volume} ml", self.central_widget)
        self.solution_volume_label.setGeometry(
            int(630 * self.scale_factor),
            int(420 * self.scale_factor),
            int(200 * self.scale_factor),
            int(60 * self.scale_factor)
        )
        scaled_font = QFont("Calibri", int(12 * self.scale_factor))
        self.solution_volume_label.setFont(scaled_font)
        self.solution_volume_label.setStyleSheet("color: black; background-color: transparent;")
        self.solution_volume_label.hide()

        # Create drops added label with absolute positioning and scaling
        self.drops_added_label = QLabel(f"Number of Drops Added: {self.drop_counter}", self.central_widget)
        self.drops_added_label.setGeometry(
            int(950 * self.scale_factor),
            int(120 * self.scale_factor),
            int(300 * self.scale_factor),
            int(20 * self.scale_factor)
        )
        self.drops_added_label.setFont(QFont("Calibri", int(10 * self.scale_factor)))
        self.drops_added_label.setStyleSheet("color: black;")

        # Create alert label with absolute positioning and scaling
        self.alert_label = QLabel("BUFFER EXCEEDED", self.central_widget)
        self.alert_label.setGeometry(
            int(147 * self.scale_factor),
            int(273 * self.scale_factor),
            int(200 * self.scale_factor),
            int(30 * self.scale_factor)
        )
        self.alert_label.setAlignment(Qt.AlignCenter)
        self.alert_label.setFont(QFont("Calibri", int(12 * self.scale_factor), QFont.Bold))
        self.alert_label.setStyleSheet("color: white; background-color: transparent;")
        self.alert_label.hide()  # Initially hidden

        # Create copyright label in the top corner
        self.copyright_label = QLabel("Made by: Ronald Ruszczyk, Ryder Selikow, Nicholas Dill, Igor Gromovic, Andrew Fletcher @ Lewis & Clark College", self.central_widget)
        self.copyright_label.setGeometry(
            int(650 * self.scale_factor),
            int(780 * self.scale_factor),
            int(550 * self.scale_factor),
            int(20 * self.scale_factor)
        )
        self.copyright_label.setFont(QFont("Calibri", int(8 * self.scale_factor)))
        self.copyright_label.setStyleSheet("color: black; background-color: transparent;")

        # Create buttons with absolute positioning and scaling
        self.insert_probe_button = QPushButton("Insert Probe", self.central_widget)
        self.insert_probe_button.setGeometry(
            int(172 * self.scale_factor),
            int(365 * self.scale_factor),
            int(150 * self.scale_factor),
            int(30 * self.scale_factor)
        )
        self.insert_probe_button.setStyleSheet(f"background-color: {BURNT_ORANGE}; padding: 5px; border:1px solid black; border-radius: 5px;")
        self.insert_probe_button.setFont(QFont("Calibri", int(12 * self.scale_factor)))
        self.insert_probe_button.clicked.connect(self.insert_probe)

        self.remove_probe_button = QPushButton("Remove Probe", self.central_widget)
        self.remove_probe_button.setGeometry(
            int(172 * self.scale_factor),
            int(400 * self.scale_factor),
            int(150 * self.scale_factor),
            int(30 * self.scale_factor)
        )
        self.remove_probe_button.setStyleSheet(f"background-color: {BURNT_ORANGE}; padding: 5px; border:1px solid black; border-radius: 5px;")
        self.remove_probe_button.setFont(QFont("Calibri", int(12 * self.scale_factor)))
        self.remove_probe_button.clicked.connect(self.remove_probe)

        #Create toggle indicator button
        self.toggle_indicator_button = QPushButton("pH Indicator: ON", self.central_widget)
        self.toggle_indicator_button.setGeometry(
            int(172 * self.scale_factor),
            int(435 * self.scale_factor),
            int(150 * self.scale_factor),
            int(30 * self.scale_factor)
        )
        self.toggle_indicator_button.setStyleSheet(f"background-color: {BURNT_ORANGE}; padding: 5px; border:1px solid black; border-radius: 5px;")
        self.toggle_indicator_button.setFont(QFont("Calibri", int(12 * self.scale_factor)))
        self.toggle_indicator_button.setCheckable(True)
        self.toggle_indicator_button.setChecked(False)
        self.toggle_indicator_button.clicked.connect(self.toggle_ph_strip_reset)

        # Create add drop button with absolute positioning and scaling
        self.add_drop_button = QPushButton("Add drop", self.central_widget)
        self.add_drop_button.setGeometry(
            int(950 * self.scale_factor),
            int(170 * self.scale_factor),
            int(150 * self.scale_factor),
            int(30 * self.scale_factor)
        )
        self.add_drop_button.setStyleSheet(f"background-color: {BURNT_ORANGE}; padding: 5px; border:1px solid black; border-radius: 5px;")
        self.add_drop_button.setFont(QFont("Calibri", int(10 * self.scale_factor)))
        self.add_drop_button.clicked.connect(self.send_drop)
        self.add_drop_button.hide()  # Initially hidden


        # Create pH value label with absolute positioning and scaling
        self.ph_value_label = QLabel("---", self.central_widget)
        self.ph_value_label.setGeometry(
            int(225 * self.scale_factor),
            int(180 * self.scale_factor),
            int(90 * self.scale_factor),
            int(60 * self.scale_factor)
        )
        self.ph_value_label.setFont(QFont("Calibri", int(20 * self.scale_factor)))
        self.ph_value_label.setStyleSheet("color: black;")

        # Create pH Strip with scaling
        self.ph_strip_label = QLabel(self.central_widget)
        self.ph_strip_label.setGeometry(
            int(170 * self.scale_factor),
            int(316 * self.scale_factor),
            int(150 * self.scale_factor),
            int(30 * self.scale_factor)
        )
        self.ph_strip_label.setText("pH indicator")
        self.ph_strip_label.setAlignment(Qt.AlignCenter)
        self.ph_strip_label.setFont(QFont("Calibri", int(12 * self.scale_factor)))
        self.ph_strip_label.setStyleSheet("color: black; border: 2px solid black; background-color: white;")

    def load_images(self):
        """Load all required images for the application."""
        src_dir = os.path.dirname(os.path.abspath(__file__))
        graphics_dir = os.path.join(src_dir, "graphics")

        # Initialize paths
        empty_outside_path = os.path.join(graphics_dir, "pH meter beaker empty.png")
        empty_inside_path = os.path.join(graphics_dir, "pH meter beaker empty inside.png")
        outside_path = os.path.join(graphics_dir, "pH meter beaker outside.png")
        inside_path = os.path.join(graphics_dir, "pH meter beaker inside.png")
        drop_path = os.path.join(graphics_dir, "drop.png")
        dropper_path = os.path.join(graphics_dir, "dropper.png")

        # Load images with resource manager caching
        def load_cached_image(path):
            cached = self.resource_manager.get_cached_image(path)
            if cached:
                return cached
            pixmap = QPixmap(path)
            return self.resource_manager.cache_image(path, pixmap)

        # Load the original pixmaps at full resolution
        self.ph_meter_empty_outside = load_cached_image(empty_outside_path)
        self.ph_meter_empty_inside = load_cached_image(empty_inside_path)
        self.ph_meter_outside = load_cached_image(outside_path)
        self.ph_meter_inside = load_cached_image(inside_path)

        # Create the drop label and load drop images
        self.child = QLabel(self)
        self.child.setAttribute(Qt.WA_TranslucentBackground)  # Make label background transparent
        self.dropPixMap = load_cached_image(drop_path)
        self.dropperPix = load_cached_image(dropper_path)

    def send_drop(self):
        """Starts the animation of the drop and updates pH based on drop type."""

        if not self.probe_inserted:
            # print("Probe must be inserted before adding a drop!")
            self.drops_added_label.hide()
            self.alert_label.setText("INSERT THE PROBE")
            self.alert_label.show()
            return

        if not self.solution_selected:
            # print("Please select a solution before adding a drop!")
            self.drops_added_label.hide()
            self.alert_label.setText("SELECT A SOLUTION")
            self.alert_label.show()
            return

        selected_drop_button = self.drop_button_group.checkedButton()
        if not selected_drop_button:
            # print("Please select a drop type before adding a drop!")
            self.drops_added_label.hide()
            self.alert_label.setText("SELECT DROP TYPE")
            self.alert_label.show()
            return

        # Extract drop type details
        addition, drop_molarity = self.check_drops()

        if drop_molarity == 0:
            # print("Invalid drop type selected!")
            self.drops_added_label.hide()
            return

        # Proceed with drop addition
        self.drop_counter += 1
        self.drops_added_label.setText(f"Number of Drops Added: {self.drop_counter}")
        self.drops_added_label.show()  # Ensure label is visible when a drop is added

        # Update animation coordinates with scaling
        pixmap_scaled = self.dropPixMap.scaled(
            int(25 * self.scale_factor),
            int(25 * self.scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.child.setPixmap(pixmap_scaled)
        self.child.resize(pixmap_scaled.width(), pixmap_scaled.height())
        self.child.show()
        self.anim = QPropertyAnimation(self.child, b"pos")
        self.anim.setStartValue(QPoint(
            int(755 * self.scale_factor),
            int(100 * self.scale_factor)
        ))
        self.anim.setEndValue(QPoint(
            int(755 * self.scale_factor),
            int(350 * self.scale_factor)
        ))
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.InCubic)

        # Track animation connection with resource manager instead of direct connection
        self.resource_manager.track_connection(self.anim, "finished", self.child.hide)

        self.anim.start()

        self.solution_volume += DROP_VOLUME
        self.solution_volume_label.setText(f"Solution volume: {round(self.solution_volume, 3)} ml")

        # Recalculate pH after drop is added
        selected_category = self.category_button_group.checkedButton()
        if selected_category:
            category_text = selected_category.text()
            if category_text == "Buffers":
                self.calculate_buffer_sliders()
            elif category_text == "Water":
                self.calculate_water_ph()

    def reset_state(self):
        """Reset application state variables to a consistent initial state."""
        # Reset counters and volumes
        self.drop_counter = 0
        self.solution_volume = 10
        # self.current_ph_value = 7
        self.toggle_indicator_button.setChecked(False)
        self.toggle_indicator_button.setText("pH Indicator: ON")
        self.solution_volume_label.setText(f"Solution volume: {round(self.solution_volume, 3)} ml")
        self.ph_strip_label.setStyleSheet("color: black; border: 2px solid black; background-color: white;")

        # Update UI elements
        self.drops_added_label.hide()
        self.alert_label.hide()
        self.drops_added_label.setText(f"Number of Drops Added: {self.drop_counter}")

        # Reset pH display if probe is not inserted
        if not self.probe_inserted:
            self.ph_value_label.setText("---")

    def on_category_changed(self, button):
        """Handle category selection change."""
        # Reset state
        self.reset_state()
        self.solution_selected = False

        # Determine which frame to show based on selected category
        category_frames = {
            "Acids/Bases": self.acids_bases_frame,
            "Salts": self.salts_frame,
            "Buffers": self.buffers_frame,
            "Household Items": self.household_items_frame,
            "Water": self.water_frame,
        }

        # Get selected category
        selected_category = button.text()

        # Clear all solution selections without affecting frame visibility
        solution_button_groups = [
            self.acids_bases_button_group,
            self.salts_button_group,
            self.buffers_button_group,
            self.household_items_button_group,
            self.water_button_group,
            self.drop_button_group
        ]

        for group in solution_button_groups:
            group.setExclusive(False)
            for button in group.buttons():
                button.setChecked(False)
            group.setExclusive(True)

        # Show only the selected category frame, hide others
        for category, frame in category_frames.items():
            frame.setVisible(category == selected_category)

        # Define categories that require the concentration slider/label
        categories_with_concentration = {"Acids/Bases", "Salts"}

        # Show or hide concentration controls accordingly
        show_concentration = selected_category in categories_with_concentration
        self.concentration_slider.setVisible(show_concentration)
        self.slider_frame.setVisible(show_concentration)
        self.concentration_label.setVisible(show_concentration)

        # Show or hide buffer sliders
        is_buffer_category = selected_category == "Buffers"
        self.buffer_sliders_frame.setVisible(is_buffer_category)

        # Show or hide dropper and add drop button
        show_dropper = selected_category in {"Buffers", "Water"}
        self.dropper_label.setVisible(show_dropper)
        self.add_drop_button.setVisible(show_dropper)
        self.drops_frame.setVisible(show_dropper)

        # If buffer category is selected, update the buffer slider labels
        if is_buffer_category:
            self.update_buffer_slider_labels()

        # Remove probe when changing categories
        self.remove_probe()

    def on_solution_changed(self, button):
        """Handle solution selection change."""
        self.solution_selected = True
        self.reset_state()
        self.solution_volume_label.show()
        if self.probe_inserted:
            # Get the selected category
            selected_category = self.category_button_group.checkedButton()
            if selected_category and selected_category.text() == "Buffers":
                # Update buffer labels based on selected buffer
                selected_buffer = button.text()
                if selected_buffer in self.buffer_formulas:
                    formulas = self.buffer_formulas[selected_buffer]
                    self.buffer_label_1.setText(f"Concentration (Molarity) Acid, {formulas['acid']}")
                    self.buffer_label_2.setText(f"Concentration (Molarity) Base, {formulas['base']}")
                # Update the buffer slider labels
                self.update_buffer_slider_labels()
                scaled_outside = self.ph_meter_inside.scaled(
                int(self.ph_meter_inside.width() * self.scale_factor),
                int(self.ph_meter_inside.height() * self.scale_factor),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_outside)
            else:
                # For other categories, recalculate pH with new solution
                self.insert_probe()
        else:
            # If probe is not inserted, ensure pH display is reset
            # and set image back to empty
            self.ph_value_label.setText("---")
            # Scale the outside pixmap with smooth transformation
            scaled_outside = self.ph_meter_outside.scaled(
                int(self.ph_meter_outside.width() * self.scale_factor),
                int(self.ph_meter_outside.height() * self.scale_factor),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_outside)

            # Still update buffer labels even if probe is not inserted
            selected_category = self.category_button_group.checkedButton()
            if selected_category and selected_category.text() == "Buffers":
                selected_buffer = button.text()
                if selected_buffer in self.buffer_formulas:
                    formulas = self.buffer_formulas[selected_buffer]
                    self.buffer_label_1.setText(f"Concentration (Molarity) Acid, {formulas['acid']}")
                    self.buffer_label_2.setText(f"Concentration (Molarity) Base, {formulas['base']}")

    def on_drop_changed(self):
        """Handle drop selection change."""
        # Save the current pH indicator state before resetting
        indicator_was_checked = self.toggle_indicator_button.isChecked()

        # Reset state when drop type changes
        self.reset_state()

        # Restore the pH indicator state
        if indicator_was_checked:
            self.toggle_indicator_button.setChecked(True)
            self.toggle_indicator_button.setText("pH Indicator: OFF")
            if self.probe_inserted and self.current_ph_value is not None:
                self.update_ph_strip(self.current_ph_value)

        if self.probe_inserted:
            self.insert_probe()
        else:
            self.remove_probe()



    def insert_probe(self):
        """Insert the probe and enable pH calculation updates."""
        if self.ph_meter_inside.isNull():
            return  # Exit early if the probe is null

        # Scale the inside pixmap with smooth transformation
        if not self.solution_selected:
            scaled_inside = self.ph_meter_empty_inside.scaled(
                int(self.ph_meter_inside.width() * self.scale_factor),
                int(self.ph_meter_inside.height() * self.scale_factor),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.solution_volume_label.hide()
        else:
            scaled_inside = self.ph_meter_inside.scaled(
            int(self.ph_meter_inside.width() * self.scale_factor),
            int(self.ph_meter_inside.height() * self.scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
            )
            self.solution_volume_label.show()
        self.image_label.setPixmap(scaled_inside)
        self.probe_inserted = True  # Set flag to indicate probe is inserted
        self.alert_label.hide()
        self.alert_label.setText("")

        # Get the selected category
        selected_category = self.category_button_group.checkedButton()
        if not selected_category:
            return  # Exit early if no category is selected

        category_text = selected_category.text()

        # Define actions for each category
        category_actions = {
            "Acids/Bases": lambda: self.calculate_acid_base_ph(
                self.concentration_values[self.concentration_slider.value()]),
            "Salts": lambda: self.calculate_salt_ph(self.concentration_values[self.concentration_slider.value()]),
            "Household Items": self.calculate_household_item_ph,
            "Buffers": self.calculate_buffer_sliders,
            "Water": self.calculate_water_ph
        }

        #check if solution is selceted
        if not self.solution_selected:
            # print("Please select a solution before adding a drop!")
            self.drops_added_label.hide()
            self.alert_label.setText("SELECT A SOLUTION")
            self.alert_label.show()
            return

        # Execute the corresponding action
        action = category_actions.get(category_text)
        if action:
            action()

    def calculate_household_item_ph(self):
        """Calculate pH for selected household item using constant values."""
        selected_button = self.household_items_button_group.checkedButton()

        if selected_button:
            item_ph_values = {
                "Table salt (sodium chloride)": 7.0,
                "Baking Soda (sodium bicarbonate)": 8.3,
                "Hydrogen Peroxide (3% H202)": 6.2,
                "Drano (contains sodium hydroxide)": 12.0,
                "Liquid Plumber (contains sulfuric acid)": 1.0,
                "Soft Drink (contains citric and carbonic acids)": 3.2,
                "Orange Juice (contains citric and ascorbic acid)": 3.9,
                "Milk": 6.8,
                "Dish Soap": 8.7,
                "Blood": 7.4,
                "Battery Acid (contains sulfuric acid)": 1.0,
                "Ammonia (2% ammonium hydroxide)": 11.6,
                "Vinegar (5% acetic acid)": 2.4,
            }

            # Get pH value from dictionary, defaulting to 7.0 if item not found
            ph = item_ph_values.get(selected_button.text(), 7.0)
            self.current_ph_value = ph
            if selected_button.text() == "Blood":
                self.ph_value_label.setText(f"{ph:.2f}")
            else:
                self.ph_value_label.setText(f"{ph:.1f}")
            self.update_ph_strip(ph)  # Update pH strip color

    def calculate_acid_base_ph(self, concentration):
        """Calculate pH for selected acid or base."""
        selected_button = self.acids_bases_button_group.checkedButton()

        if selected_button:
            # Dictionary mapping chemical names to their corresponding functions
            acid_base_functions = {
                u"Ba(OH)\u2082 Barium Hydroxide": h_conc_baoh2,
                "Ca(OH)\u2082 Calcium Hydroxide": h_conc_caoh2,
                "NaOH Sodium Hydroxide": h_conc_naoh,
                "NH\u2084OH Ammonium Hydroxide (NH\u2083/H\u2082O)": h_conc_nhamoh,
                "HCl Hydrochloric Acid": h_conc_hcl,
                "HNO\u2083 Nitric Acid": h_conc_hno3,
                "HC\u2082H\u2083O\u2082 Acetic Acid": h_conc_hc2h3o2,
                "H\u2082CO\u2083 Carbonic Acid": h_conc_h2co3,
            }

            # Get the corresponding function, defaulting to neutral pH if not found
            h_conc_func = acid_base_functions.get(selected_button.text(), lambda _: 1.0e-7)
            h_conc = h_conc_func(concentration)

            # Calculate pH from hydrogen ion concentration
            ph = ph_from_h_concentration(h_conc)
            self.current_ph_value = ph

            # Update the pH value label
            self.ph_value_label.setText(f"{ph:.3f}")
            self.update_ph_strip(ph)  # Update pH strip color

    def calculate_salt_ph(self, concentration):
        """Calculate pH for selected salt."""
        selected_button = self.salts_button_group.checkedButton()

        if selected_button:
            # Dictionary mapping salts to their corresponding hydrogen ion concentration functions
            salt_ph_functions = {
                "NaCl: Sodium Chloride": lambda _: ph_nacl(),  # Returns a fixed pH of 7.0
                "NH\u2084Cl: Ammonium Chloride": h_conc_nhg,
                "NaC\u2082H\u2083O\u2082: Sodium Acetate": h_conc_nac2h3o2,
                "NaHCO\u2083: Sodium Bicarbonate": h_conc_nahco3,
                "Na\u2082CO\u2083: Sodium Carbonate": h_conc_na2co3,
                "NaHSO\u2084: Sodium Bisulfate": h_conc_nahso4,
            }

            # Get the corresponding function, defaulting to a neutral pH function
            h_conc_func = salt_ph_functions.get(selected_button.text(), lambda _: 1.0e-7)
            h_conc = h_conc_func(concentration)

            # Calculate pH from hydrogen ion concentration, except for NaCl which has a fixed pH
            ph = ph_from_h_concentration(h_conc) if selected_button.text() != "NaCl: Sodium Chloride" else ph_nacl()
            self.current_ph_value = ph

            # Update the pH value label
            self.ph_value_label.setText(f"{ph:.3f}")
            self.update_ph_strip(ph)  # Update pH strip color

    def calculate_water_ph(self):
        """Calculate pH of water with added drops of strong acid or base."""
        if not self.probe_inserted:
            # print("Probe not inserted, skipping pH calculation")
            return

        selected_button = self.water_button_group.checkedButton()
        if not selected_button:
            # print("Select water")
            return

        # Get drop molarity and type
        addition, drop_molarity = self.check_drops()  #  Fetch drop_molarity before use

        ph = ph_from_h_concentration(h_conc_titration_general(drop_molarity=drop_molarity, drops=self.drop_counter,
                                                              initial_volume=self.solution_volume, addition=addition))
        self.current_ph_value = ph
        # print(f"Calculated pH: {ph}")
        self.ph_value_label.setText(f"{ph:.3f}")
        self.update_ph_strip(ph)
        return ph

    def remove_probe(self):
        """Switch back to the image without the probe and reset pH display"""
        if not self.ph_meter_outside.isNull():
            if not self.solution_selected:
                # Scale the outside pixmap with smooth transformation
                scaled_outside = self.ph_meter_empty_outside.scaled(
                    int(self.ph_meter_outside.width() * self.scale_factor),
                    int(self.ph_meter_outside.height() * self.scale_factor),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.solution_volume_label.hide()
            else:
                # Scale the outside pixmap with smooth transformation
                scaled_outside = self.ph_meter_outside.scaled(
                    int(self.ph_meter_outside.width() * self.scale_factor),
                    int(self.ph_meter_outside.height() * self.scale_factor),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.solution_volume_label.show()


            self.image_label.setPixmap(scaled_outside)
            self.probe_inserted = False  # Clear the flag to indicate probe is removed
            self.drops_added_label.hide()  # Hide drop counter when probe is removed
            self.ph_value_label.setText("---")  # Reset pH value display
            self.reset_state()

    def update_concentration_label(self, value):
        """Update the concentration label when slider value changes and recalculate pH if probe is inserted"""
        if 0 <= value < len(self.concentration_values):
            concentration = self.concentration_values[value]
            self.concentration_label.setText(f"{concentration:.4f} M")

            # If the probe is inserted, update the pH calculation
            if self.probe_inserted:
                # Get the selected category
                selected_category = self.category_button_group.checkedButton()
                if selected_category:
                    if selected_category.text() == "Acids/Bases":
                        self.calculate_acid_base_ph(concentration)
                    elif selected_category.text() == "Salts":
                        self.calculate_salt_ph(concentration)
                    elif selected_category.text() == "Water":
                        self.calculate_water_ph()

    def update_buffer_slider_labels(self):
        """Update buffer slider value labels dynamically and calculate pH only if the probe is inserted."""
        # Update displayed values
        acid_value = self.buffer_concentration_values[self.buffer_slider_1.value()]
        base_value = self.buffer_concentration_values[self.buffer_slider_2.value()]

        self.buffer_value_1.setText(f"{acid_value:.4f} M")
        self.buffer_value_2.setText(f"{base_value:.4f} M")

        # Only calculate and update pH if the probe is inserted
        if self.probe_inserted:
            self.calculate_buffer_sliders()

    def check_drops(self):
        # Check if a drop type is selected

        drop_molarity = 0
        addition = 'acid'
        selected_drop_button = self.drop_button_group.checkedButton()
        # print(selected_drop_button)
        if not selected_drop_button:
            # Default values if no drop is selected
            # print("Please select an acid or base drop first.")
            pass
        else:
            drop_type = selected_drop_button.text()
            if drop_type == "0.1 M HCl":
                addition = 'acid'
                drop_molarity = 0.1
            elif drop_type == "0.01 M HCl":
                addition = 'acid'
                drop_molarity = 0.01
            elif drop_type == "0.1 M NaOH":
                addition = 'base'
                drop_molarity = 0.1
            else:  # "0.01 M NaOH"
                addition = 'base'
                drop_molarity = 0.01
        return addition, drop_molarity

    def calculate_buffer_sliders(self):
        """Calculate pH for the selected buffer when the probe is inserted."""

        if not self.probe_inserted:
            # print("Probe not inserted, skipping buffer pH calculation")
            return

        selected_button = self.buffers_button_group.checkedButton()
        if not selected_button:
            # print("No buffer selected")
            return

        # Get the selected buffer name
        selected_buffer = selected_button.text()
        # print(f"Selected buffer: {selected_buffer}")

        # Get the simplified buffer name for pKa lookup
        buffer_key = BUFFER_NAME_MAPPING.get(selected_buffer)
        # print(f"Buffer key for pKa lookup: {buffer_key}")

        # Get pKa value for the selected buffer
        pKa = BUFFER_PKA_VALUES.get(buffer_key, 7.0)
        # print(f"pKa value: {pKa}")

        # Get updated concentration values from sliders
        acid_conc = self.buffer_concentration_values[self.buffer_slider_1.value()]
        base_conc = self.buffer_concentration_values[self.buffer_slider_2.value()]
        # print(f"Acid concentration: {acid_conc}, Base concentration: {base_conc}")

        # Prevent division errors
        acid_conc = max(acid_conc, 0.0001)
        base_conc = max(base_conc, 0.0001)

        # ✅ Ensure latest drop data is retrieved
        addition, drop_molarity = self.check_drops()

        # Calculate pH using Henderson-Hasselbalch equation
        try:
            ph = buffer_ph_general(acid_conc, base_conc, pKa, drop_molarity=drop_molarity, drops=self.drop_counter,
                                   addition=addition)
            self.current_ph_value = ph

            # If buffer_ph_general returns False, the buffer capacity is exceeded
            if ph is False:
                # print("Buffer capacity exceeded, calculating overflow pH")
                # Determine which concentration to use based on addition type
                buffer_conc = base_conc if addition == 'acid' else acid_conc
                # Calculate overflow pH
               # ph = buffer_overflow_ph_general(addition, buffer_conc, drop_molarity=drop_molarity, drops=self.drop_counter)
                ph = buffer_overflow_ph_general(acid_conc, base_conc, pKa, drop_molarity, self.drop_counter, addition=addition)
                self.current_ph_value = ph
                # print(f"Buffer exceeded! Calculated overflow pH: {ph}")
                # Show the buffer exceeded label
                self.alert_label.setText("BUFFER CAPACITY EXCEEDED")
                self.alert_label.show()
            else:
                # print(f"Calculated pH within buffer capacity: {ph}")
                # Hide the buffer exceeded label
                self.alert_label.hide()

            # Display the pH value
            self.ph_value_label.setText(f"{ph:.3f}")
            self.update_ph_strip(ph)  # Update pH strip color

        except ValueError as e:
            # print(f"Buffer calculation error: {e}")
            self.ph_value_label.setText("Error")
            self.alert_label.hide()

    def toggle_ph_strip_reset(self):
        if not self.probe_inserted:
            self.toggle_indicator_button.setChecked(False)
            self.alert_label.setText("INSERT THE PROBE")
            self.alert_label.show()
            return
        if not self.solution_selected:
            self.toggle_indicator_button.setChecked(False)
            self.drops_added_label.hide()
            self.alert_label.setText("SELECT A SOLUTION")
            self.alert_label.show()
            return
        if not self.toggle_indicator_button.isChecked():
            # Button is toggled ON - reset label
            self.ph_strip_label.setStyleSheet("color: black; border: 2px solid black; background-color: white;")
            self.toggle_indicator_button.setText("pH Indicator: ON")
        else:
            # Button is toggled OFF - allow updates again
            self.update_ph_strip(self.current_ph_value)
            self.toggle_indicator_button.setText("pH Indicator: OFF")
            return

    def update_ph_strip(self, ph_value):
        """Update the pH strip color based on the calculated pH value."""
        if not self.toggle_indicator_button.isChecked():
            self.ph_strip_label.setStyleSheet("color: black; border: 2px solid black; background-color: white;")
            return
        else:
            try:
                ph_value = float(ph_value)
            except ValueError:
                return  # Skip if pH is not a valid number

            # Find closest integer pH value
            closest_ph = max(0, min(14, round(ph_value)))
            strip_color = PH_COLORS.get(closest_ph, "#FFFFFF")  # Default to white if out of range

            # Apply color to pH strip
            self.ph_strip_label.setStyleSheet(f"color: black; border: 2px solid black; background-color: {strip_color};")

    def setup_layouts(self):
        """Set up the layouts for all frames."""
        # Create category buttons layout
        self.category_layout = QVBoxLayout(self.category_frame)
        self.category_layout.setContentsMargins(10, 10, 10, 10)
        self.category_layout.setSpacing(10)

        # Create acids/bases buttons layout
        self.acids_bases_layout = QHBoxLayout(self.acids_bases_frame)
        self.acids_bases_layout.setContentsMargins(10, 0, 10, 10)
        self.acids_bases_layout.setSpacing(10)

        # Create slider layout
        self.slider_layout = QVBoxLayout(self.slider_frame)
        self.slider_layout.setContentsMargins(10, 10, 10, 10)
        self.slider_layout.setSpacing(5)

        # Create a container for radio buttons
        self.acids_bases_radio_container = QWidget()
        self.acids_bases_radio_layout = QVBoxLayout(self.acids_bases_radio_container)
        self.acids_bases_layout.addWidget(self.acids_bases_radio_container)

        # Create salts buttons layout
        self.salts_layout = QVBoxLayout(self.salts_frame)
        self.salts_layout.setContentsMargins(10, 0, 10, 10)
        self.salts_layout.setSpacing(10)

        # Create buffers buttons layout
        self.buffers_layout = QVBoxLayout(self.buffers_frame)
        self.buffers_layout.setContentsMargins(10, 0, 10, 10)
        self.buffers_layout.setSpacing(10)

        # Create household buttons layout - using two columns
        self.household_items_layout = QHBoxLayout(self.household_items_frame)
        self.household_items_layout.setContentsMargins(10, 0, 10, 10)
        self.household_items_layout.setSpacing(10)

        # Create two columns for household items
        self.household_left_column = QWidget()
        self.household_right_column = QWidget()
        self.household_left_layout = QVBoxLayout(self.household_left_column)
        self.household_right_layout = QVBoxLayout(self.household_right_column)
        self.household_items_layout.addWidget(self.household_left_column)
        self.household_items_layout.addWidget(self.household_right_column)

        # Water button layout
        self.water_layout = QVBoxLayout(self.water_frame)
        self.water_layout.setContentsMargins(10, 0, 10, 10)
        self.water_layout.setSpacing(10)

        # Create drops buttons layout
        self.drops_layout = QVBoxLayout(self.drops_frame)
        self.drops_layout.setContentsMargins(10, 0, 10, 10)
        self.drops_layout.setSpacing(10)

    def initialize_data(self):
        """Initialize data structures and values for the application."""
        # Use concentration values from models
        self.concentration_values = CONCENTRATION_VALUES
        self.buffer_concentration_values = BUFFER_CONCENTRATION_VALUES

        # Buffer formulas mapping
        self.buffer_formulas = {
            "HC2H3O2 / NaC2H3O2: Acetic Acid / Sodium Acetate": {
                "acid": "HC<sub>2</sub>H<sub>3</sub>O<sub>2</sub>",
                "base": "NaC<sub>2</sub>H<sub>3</sub>O<sub>2</sub>"
            },
            "NH4Cl / NH3: Ammonium Chloride / Ammonia": {
                "acid": "NH<sub>4</sub>Cl",
                "base": "NH<sub>3</sub>"
            },
            "NaH2PO4 / Na2HPO4: Sodium Dihydrogen Phosphate / Disodium Hydrogen Phosphate": {
                "acid": "NaH<sub>2</sub>PO<sub>4</sub>",
                "base": "Na<sub>2</sub>HPO<sub>4</sub>"
            },
            "NaHCO3 / Na2CO3: Sodium Bicarbonate / Sodium Carbonate": {
                "acid": "NaHCO<sub>3</sub>",
                "base": "Na<sub>2</sub>CO<sub>3</sub>"
            },
            "H2CO3 / NaHCO3: Carbonic Acid / Sodium Bicarbonate": {
                "acid": "H<sub>2</sub>CO<sub>3</sub>",
                "base": "NaHCO<sub>3</sub>"
            }
        }

        # Create slider label
        self.slider_label = QLabel("Concentration (Molarity)", self.slider_frame)
        self.slider_label.setFont(QFont("Calibri", int(11 * self.scale_factor)))
        self.slider_label.setAlignment(Qt.AlignCenter)
        self.slider_layout.addWidget(self.slider_label)

        # Create concentration slider
        self.concentration_slider = QSlider(Qt.Horizontal)
        self.concentration_slider.setMinimum(0)
        self.concentration_slider.setMaximum(len(self.concentration_values) - 1)
        self.concentration_slider.setTickPosition(QSlider.TicksBelow)
        self.concentration_slider.setTickInterval(1)
        self.slider_layout.addWidget(self.concentration_slider)

        # Create concentration label
        self.concentration_label = QLabel(f"{self.concentration_values[0]:.4f} M")
        self.concentration_label.setFont(QFont("Calibri", int(12 * self.scale_factor)))
        self.concentration_label.setAlignment(Qt.AlignCenter)
        self.slider_layout.addWidget(self.concentration_label)

        # Setup buffer slider frame
        self.setup_buffer_sliders()

    def setup_buffer_sliders(self):
        """Set up the buffer sliders and their controls."""
        # Create buffer sliders frame with scaling
        self.buffer_sliders_frame = QFrame(self.central_widget)
        self.buffer_sliders_frame.setGeometry(
            int(810 * self.scale_factor),
            int(550 * self.scale_factor),
            int(300 * self.scale_factor),
            int(160 * self.scale_factor)
        )
        self.buffer_sliders_frame.setStyleSheet(f"background-color: {ASHIER_GREY};")
        self.buffer_sliders_frame.setProperty("class", "bordered_frames")
        self.buffer_sliders_frame.hide()

        # Buffer slider 1 (Acid)
        self.buffer_slider_1 = QSlider(Qt.Horizontal, self.buffer_sliders_frame)
        self.buffer_slider_1.setMinimum(0)
        self.buffer_slider_1.setMaximum(len(self.buffer_concentration_values) - 1)
        self.buffer_slider_1.setTickPosition(QSlider.TicksBelow)
        self.buffer_slider_1.setTickInterval(1)

        # Buffer slider 1 label (Acid)
        self.buffer_label_1 = QLabel("Concentration (Molarity) Acid", self.buffer_sliders_frame)
        self.buffer_label_1.setFont(QFont("Calibri", int(11 * self.scale_factor)))
        self.buffer_label_1.setAlignment(Qt.AlignCenter)

        # Buffer slider 1 value label
        self.buffer_value_1 = QLabel(f"{self.buffer_concentration_values[0]:.4f} M", self.buffer_sliders_frame)
        self.buffer_value_1.setFont(QFont("Calibri", int(12 * self.scale_factor)))
        self.buffer_value_1.setAlignment(Qt.AlignCenter)

        # Buffer slider 2 (Base)
        self.buffer_slider_2 = QSlider(Qt.Horizontal, self.buffer_sliders_frame)
        self.buffer_slider_2.setMinimum(0)
        self.buffer_slider_2.setMaximum(len(self.buffer_concentration_values) - 1)
        self.buffer_slider_2.setTickPosition(QSlider.TicksBelow)
        self.buffer_slider_2.setTickInterval(1)

        # Buffer slider 2 label (Base)
        self.buffer_label_2 = QLabel("Concentration (Molarity) Base", self.buffer_sliders_frame)
        self.buffer_label_2.setFont(QFont("Calibri", int(11 * self.scale_factor)))
        self.buffer_label_2.setAlignment(Qt.AlignCenter)

        # Buffer slider 2 value label
        self.buffer_value_2 = QLabel(f"{self.buffer_concentration_values[0]:.4f} M", self.buffer_sliders_frame)
        self.buffer_value_2.setFont(QFont("Calibri", int(12 * self.scale_factor)))
        self.buffer_value_2.setAlignment(Qt.AlignCenter)

        # Layout for buffer sliders
        buffer_layout = QVBoxLayout(self.buffer_sliders_frame)
        buffer_layout.addWidget(self.buffer_label_1)
        buffer_layout.addWidget(self.buffer_slider_1)
        buffer_layout.addWidget(self.buffer_value_1)
        buffer_layout.addWidget(self.buffer_label_2)
        buffer_layout.addWidget(self.buffer_slider_2)
        buffer_layout.addWidget(self.buffer_value_2)

    def setup_radio_buttons(self):
        """Set up all radio buttons and button groups."""
        # Create button groups
        self.category_button_group = QButtonGroup(self)
        self.acids_bases_button_group = QButtonGroup(self)
        self.salts_button_group = QButtonGroup(self)
        self.buffers_button_group = QButtonGroup(self)
        self.household_items_button_group = QButtonGroup(self)
        self.water_button_group = QButtonGroup(self)
        self.drop_button_group = QButtonGroup(self)

        # Define categories and options
        categories = ["Acids/Bases", "Salts", "Buffers", "Household Items", "Water"]
        acids_bases_categories = ["Ba(OH)\u2082 Barium Hydroxide", "Ca(OH)\u2082 Calcium Hydroxide",
                                "NaOH Sodium Hydroxide", "NH\u2084OH Ammonium Hydroxide (NH\u2083/H\u2082O)",
                                "HCl Hydrochloric Acid",
                                "HNO\u2083 Nitric Acid", "HC\u2082H\u2083O\u2082 Acetic Acid", "H\u2082CO\u2083 Carbonic Acid"]
        salts_categories = ["NaCl: Sodium Chloride", "NH\u2084Cl: Ammonium Chloride", "NaC\u2082H\u2083O\u2082: Sodium Acetate",
                          "NaHCO\u2083: Sodium Bicarbonate", "Na\u2082CO\u2083: Sodium Carbonate", "NaHSO\u2084: Sodium Bisulfate"]
        buffers_categories = ["HC\u2082H\u2083O\u2082 / NaC\u2082H\u2083O\u2082: Acetic Acid / Sodium Acetate",
                            "NH\u2084Cl / NH\u2083: Ammonium Chloride / Ammonia",
                            "NaH\u2082PO\u2084 / Na\u2082HPO\u2084: Sodium Dihydrogen Phosphate / Disodium Hydrogen Phosphate",
                            "NaHCO\u2083 / Na\u2082CO\u2083: Sodium Bicarbonate / Sodium Carbonate",
                            "H\u2082CO\u2083 / NaHCO\u2083: Carbonic Acid / Sodium Bicarbonate"]
        household_items_categories = ["Table salt(sodium chloride)", "Baking Soda (sodium bicarbonate)",
                                    "Hydrogen Peroxide (3% H\u2082O\u2082)",
                                    "Liquid Plumber (contains sulfuric acid)",
                                    "Soft Drink (contains citric and carbonic acids)",
                                    "Orange Juice (contains citric and ascorbic acid)",
                                    "Milk", "Dish Soap", "Blood", "Battery Acid (contains sulfuric acid)",
                                    "Ammonia (2% ammonium hydroxide)", "Vinegar (5% acetic acid)"]
        water_categories = ["Water"]
        drops_categories = ["0.1 M HCl", "0.01 M HCl", "0.1 M NaOH", "0.01 M NaOH"]

        # Create category radio buttons
        for i, category in enumerate(categories):
            rb = QRadioButton(category)
            rb.setFont(QFont("Calibri", int(12 * self.scale_factor)))
            rb.setStyleSheet(f"background-color: {ASHIER_GREY}; color: {BLACK};")
            self.category_layout.addWidget(rb)
            self.category_button_group.addButton(rb, i)

            # Set default selection
            if category == "Acids/Bases":
                rb.setChecked(True)

        # Create acids/bases buttons
        for i, category in enumerate(acids_bases_categories):
            rb = QRadioButton(category)
            rb.setFont(QFont("Calibri", int(12 * self.scale_factor)))
            rb.setStyleSheet(f"background-color: {ASHIER_GREY}; color: {BLACK};")
            self.acids_bases_radio_layout.addWidget(rb)
            self.acids_bases_button_group.addButton(rb, i)

        # Create salts buttons
        for i, salt in enumerate(salts_categories):
            rb = QRadioButton(salt)
            rb.setFont(QFont("Calibri", int(12 * self.scale_factor)))
            rb.setStyleSheet(f"background-color: {ASHIER_GREY}; color: {BLACK};")
            self.salts_layout.addWidget(rb)
            self.salts_button_group.addButton(rb, i)

        # Create buffers buttons
        for i, buffer in enumerate(buffers_categories):
            rb = QRadioButton(buffer)
            rb.setFont(QFont("Calibri", int(12 * self.scale_factor)))
            rb.setStyleSheet(f"background-color: {ASHIER_GREY}; color: {BLACK};")
            self.buffers_layout.addWidget(rb)
            self.buffers_button_group.addButton(rb, i)

        # Create Household buttons in two columns
        # Split household items into two columns
        household_items_midpoint = len(household_items_categories) // 2

        # Add first half to left column
        for i, item in enumerate(household_items_categories[:household_items_midpoint]):
            rb = QRadioButton(item)
            rb.setFont(QFont("Calibri", int(12 * self.scale_factor)))
            rb.setStyleSheet(f"background-color: {ASHIER_GREY}; color: {BLACK};")
            self.household_left_layout.addWidget(rb)
            self.household_items_button_group.addButton(rb, i)

        # Add second half to right column
        for i, item in enumerate(household_items_categories[household_items_midpoint:], start=household_items_midpoint):
            rb = QRadioButton(item)
            rb.setFont(QFont("Calibri", int(12 * self.scale_factor)))
            rb.setStyleSheet(f"background-color: {ASHIER_GREY}; color: {BLACK};")
            self.household_right_layout.addWidget(rb)
            self.household_items_button_group.addButton(rb, i)

        # Create water button
        for i, item in enumerate(water_categories):
            rb = QRadioButton(item)
            rb.setFont(QFont("Calibri", int(12 * self.scale_factor)))
            rb.setStyleSheet(f"background-color: {ASHIER_GREY}; color: {BLACK};")
            self.water_layout.addWidget(rb)
            self.water_button_group.addButton(rb, i)

        # Create Drops buttons
        for i, item in enumerate(drops_categories):
            rb = QRadioButton(item)
            rb.setFont(QFont("Calibri", int(12 * self.scale_factor)))
            rb.setStyleSheet(f"background-color: {ASHIER_GREY}; color: {BLACK};")
            self.drops_layout.addWidget(rb)
            self.drop_button_group.addButton(rb, i)

    def connect_signals(self):
        """Connect all signals to their handlers."""
        # Connect buffer slider signals using resource manager to track connections
        self.resource_manager.track_connection(
            self.buffer_slider_1, "valueChanged", self.update_buffer_slider_labels)
        self.resource_manager.track_connection(
            self.buffer_slider_2, "valueChanged", self.update_buffer_slider_labels)

        # Connect concentration slider signal
        self.resource_manager.track_connection(
            self.concentration_slider, "valueChanged", self.update_concentration_label)

        # Connect button group signals
        self.resource_manager.track_connection(
            self.category_button_group, "buttonClicked", self.on_category_changed)
        self.resource_manager.track_connection(
            self.acids_bases_button_group, "buttonClicked", self.on_solution_changed)
        self.resource_manager.track_connection(
            self.salts_button_group, "buttonClicked", self.on_solution_changed)
        self.resource_manager.track_connection(
            self.buffers_button_group, "buttonClicked", self.on_solution_changed)
        self.resource_manager.track_connection(
            self.household_items_button_group, "buttonClicked", self.on_solution_changed)
        self.resource_manager.track_connection(
            self.water_button_group, "buttonClicked", self.on_solution_changed)
        self.resource_manager.track_connection(
            self.drop_button_group, "buttonClicked", self.on_drop_changed)

    # Add closeEvent to handle proper cleanup
    def closeEvent(self, event):
        """Handle window close event with proper resource cleanup."""
        # Perform cleanup through resource manager
        self.resource_manager.cleanup()
        # Accept the close event
        event.accept()
