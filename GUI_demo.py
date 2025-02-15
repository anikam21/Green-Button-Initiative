import sys
import os
import re
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QTabWidget, QDialog, QRadioButton, QFileDialog
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import water_file_combine  # Assuming this module is present for processing water-related data
import electricity_file_combine
from forecasting_model import water_linear_regression
from forecasting_model import Water_Random_Forest
from forecasting_model import electricity_linear_regression
from forecasting_model import electricity_random_forest
import weather_forecast

current_path = os.path.abspath(__file__)
current_path = os.path.dirname(current_path)

class StartDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Choose Option')
        self.showMaximized()  # Maximize the window
        self.initUI()

    def initUI(self):
        font = QFont()
        font.setPointSize(16)
        self.label = QLabel('Select an option:', self)
        self.label.setFont(font)
        self.open_module_radio = QRadioButton('Open Existing Module', self)
        self.open_module_radio.setFont(font)
        self.create_module_radio = QRadioButton('Create a New Module', self)
        self.create_module_radio.setFont(font)
        self.button = QPushButton('OK', self)
        self.button.setFont(font)
        self.button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.open_module_radio, alignment=Qt.AlignCenter)
        layout.addWidget(self.create_module_radio, alignment=Qt.AlignCenter)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)
        layout.addStretch(1)
        self.setLayout(layout)

    def get_selected_option(self):
        if self.open_module_radio.isChecked():
            return "Open Existing Module"
        elif self.create_module_radio.isChecked():
            return "Create a New Module"
        return None

class MyWindow(QWidget):
    def __init__(self, module_option, reopen_start_dialog):
        super().__init__()
        self.setWindowTitle('BV06 Green Button')
        self.showMaximized()
        self.module_option = module_option
        self.reopen_start_dialog = reopen_start_dialog
        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget(self)
        self.electricity_tab = QWidget()
        self.hydro_tab = QWidget()
        self.tabs.addTab(self.electricity_tab, 'Electricity')
        self.tabs.addTab(self.hydro_tab, 'Hydro')

        self.setupTab(self.electricity_tab, "Electricity")
        self.setupTab(self.hydro_tab, "Hydro")

        self.back_button = QPushButton('Back to Choose Option', self)
        self.back_button.clicked.connect(self.on_back_click)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.back_button)
        self.setLayout(main_layout)
        
    def load_png_to_tab(self, tab, image_path):
        # Create a QLabel to hold the image
        image_label = QLabel(tab)
        # Load the image into a QPixmap
        pixmap = QPixmap(image_path)
        # Set the QPixmap onto the QLabel
        image_label.setPixmap(pixmap)
        # Optionally, adjust the label's size to fit the image:
        image_label.resize(pixmap.width(), pixmap.height())
        # Center the image
        image_label.setAlignment(Qt.AlignCenter)
        
        # Create a layout for the tab if it doesn't already have one
        if tab.layout() is None:
            layout = QVBoxLayout(tab)
            tab.setLayout(layout)
        else:
            layout = tab.layout()

        # Add the image label to the tab's layout
        layout.addWidget(image_label)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
    
    def setupHydroTabs(self, directory_path, year_tabs_layout):
        if self.hydro_tab.layout() is None:
            hydro_layout = QVBoxLayout(self.hydro_tab)
            self.hydro_tab.setLayout(hydro_layout)
        else:
            hydro_layout = self.hydro_tab.layout()

        hydro_sub_tabs = QTabWidget(self.hydro_tab)  # Make sure the year tabs are part of the hydro_tab layout
        hydro_layout.addWidget(hydro_sub_tabs)  # Add the year tabs widget to the hydro tab's layout

        try:
            for filename in os.listdir(directory_path):
                if re.search(r"\b\d{4}\b", filename):  # Check if the filename indicates a year
                    year_tab = QWidget()  # This will be the container for the "Annual" tab and any other subtabs
                    hydro_sub_sub_tabs = QTabWidget(year_tab)  # Subtabs widget created inside the year tab
                    year_tabs_layout.addWidget(hydro_sub_tabs)
                    # Create and add the "Annual" tab with an image
                    annual_tab = QWidget()
                    self.loadImageToTab(annual_tab, os.path.join(directory_path, filename, "annual.png"))
                    hydro_sub_sub_tabs.addTab(annual_tab, "Annual")

                    # Create and add monthly tabs with images
                    for month_index in range(1, 13):
                        month_tab = QWidget()
                        month_name = self.getMonthName(month_index)
                        image_path = os.path.join(directory_path, filename, f"{month_index}.png")
                        self.loadImageToTab(month_tab, image_path)
                        hydro_sub_sub_tabs.addTab(month_tab, month_name)

                    # Set the layout for the year tab to include the subtabs widget
                    year_tab_layout = QVBoxLayout(year_tab)
                    year_tab_layout.addWidget(hydro_sub_sub_tabs)
                    year_tab.setLayout(year_tab_layout)

                    hydro_sub_tabs.addTab(year_tab, filename)  # Add the year tab to the main year tabs widget
                    #hydro_layout.insertWidget(2,hydro_sub_sub_tabs)

        except FileNotFoundError:
            print(f"Directory not found: {directory_path}")
        
        
    def setupElectricityTabs(self, directory_path, year_tabs_layout):
        # This function is similar to setupHydroTabs but for electricity data visualization
        if self.electricity_tab.layout() is None:
            electricity_layout = QVBoxLayout(self.electricity_tab)
            self.electricity_tab.setLayout(electricity_layout)
        else:
            electricity_layout = self.electricity_tab.layout()

        electricity_sub_tabs = QTabWidget(self.electricity_tab)
        electricity_layout.addWidget(electricity_sub_tabs)

        try:
            for filename in os.listdir(directory_path):
                if re.search(r"\b\d{4}\b", filename):
                    year_tab = QWidget()
                    electricity_sub_sub_tabs = QTabWidget(year_tab)
                    year_tabs_layout.addWidget(electricity_sub_tabs)
                    annual_tab = QWidget()
                    self.load_png_to_tab(annual_tab, os.path.join(directory_path, filename, "annual_electricity_usage.png"))
                    electricity_sub_sub_tabs.addTab(annual_tab, "Annual")

                    for month_index in range(1, 13):
                        month_tab = QWidget()
                        month_name = self.getMonthName(month_index)
                        self.load_png_to_tab(month_tab, os.path.join(directory_path, filename, f"month_{month_index}_electricity_usage.png"))
                        electricity_sub_sub_tabs.addTab(month_tab, month_name)

                    year_tab_layout = QVBoxLayout(year_tab)
                    year_tab_layout.addWidget(electricity_sub_sub_tabs)
                    year_tab.setLayout(year_tab_layout)

                    electricity_sub_tabs.addTab(year_tab, filename)

        except FileNotFoundError:
            print(f"Directory not found: {directory_path}")
            
            
    def loadImageToTab(self, tab, image_path):
        label = QLabel(tab)
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        tab.setLayout(layout)

    def getMonthName(self, month_index):
        import calendar
        return calendar.month_name[month_index]
        
       
    def setupTab(self, tab, tab_name):
        open_button = QPushButton('Open File', tab)
        process_button = QPushButton('Process Data', tab)
        process_button.setEnabled(False)
        file_label = QLabel('', tab)
        year_tabs_placeholder = QWidget(tab)  # Placeholder widget for year tabs
        year_tabs_placeholder_layout = QVBoxLayout(year_tabs_placeholder)


        open_button.clicked.connect(lambda: self.on_open_file_click(tab_name, file_label, process_button))
        process_button.clicked.connect(lambda: self.on_process_data_click(tab_name, year_tabs_placeholder_layout))


        tab_layout = QVBoxLayout(tab)
        tab_layout.addWidget(open_button)
        tab_layout.addWidget(process_button)
        tab_layout.addWidget(file_label)
        tab_layout.addWidget(year_tabs_placeholder)  # Add the placeholder to the layout
        tab_layout.addStretch(1)

    def on_back_click(self):
        self.close()
        self.reopen_start_dialog()

    def on_open_file_click(self, tab_name, file_label, process_button):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setWindowTitle("Open Files")
        file_paths, _ = file_dialog.getOpenFileNames(self, "Open Files", "", "All Files (*)")
        if file_paths:
            # print(tab_name)
            if tab_name == "Electricity":  
                # Define the regex pattern for the expected filename format
              #  pattern = r"Electricity Use For (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}"
                
                # Filter file_paths to include only those that match the pattern
               # filtered_file_paths = [path for path in file_paths if re.search(pattern, path, re.IGNORECASE)]
                electricity_file_combine.combine_files(file_paths)
            
                
            elif tab_name == "Hydro":
                # Define the regex pattern for the expected filename format
                pattern = r"Water Use For (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}"
                
                # Filter file_paths to include only those that match the pattern
                filtered_file_paths = [path for path in file_paths if re.search(pattern, path, re.IGNORECASE)]
                water_file_combine.combine_files(file_paths)
            
            process_button.setEnabled(True)
            

    def on_process_data_click(self, tab_name, year_tabs_layout):
        print(f"Processing Data for {tab_name}...")
        
        # Clear the existing year tabs first
        self.clearLayout(year_tabs_layout)

        if tab_name == "Electricity":                  
            # Assuming electricity_file_combine has a method for post-combination processing
            #electricity_file_combine.process_data()
            # Implement your logic for processing electricity data here
            module_path = os.path.abspath(__file__)
            current_dir = os.path.dirname(module_path)
            folder_path = os.path.join(current_dir, rf'Electricity\Combine')
            #folder_path = 'Water/Combine'  # Example path to "Combine" folder
            # Ensure this path logic and processing matches your project structure and requirements
            file_paths = {file.split('_')[3].split('.')[0]: os.path.join(folder_path, file) 
                          for file in os.listdir(folder_path) if file.endswith('.csv')}
        
            
            # Assuming process_files_and_get_best_year is a method to handle file processing and get the best year
            results, best_year = electricity_linear_regression.process_files_and_get_best_model_electricity(file_paths)
            results, best_year = electricity_linear_regression.process_files_and_get_best_model_electricity_cost(file_paths)

            # Assuming process_files_and_get_best_year is a method to handle file processing and get the best year         
            results, best_year = electricity_random_forest.process_files_and_get_best_year(file_paths)
            results, best_year = electricity_random_forest.process_files_and_get_best_year_cost(file_paths)


            
            
            # dynamiclly create year tabs, such 2020, 2021, ...
            folder_path_2_find = os.path.join(current_path, 'Electricity', 'Graphs')
            self.setupElectricityTabs(folder_path_2_find, year_tabs_layout)
 

            
        elif tab_name == "Hydro":
            # Assuming water_file_combine has a method for post-combination processing
            # Example usage of water_linear_regression assuming its methods are as below
            # Get the current working directory
            #current_dir = os.getcwd()
            module_path = os.path.abspath(__file__)
            current_dir = os.path.dirname(module_path)
            folder_path = os.path.join(current_dir, rf'Water\Combine')
            #folder_path = 'Water/Combine'  # Example path to "Combine" folder
            # Ensure this path logic and processing matches your project structure and requirements
            file_paths = {file.split('_')[3].split('.')[0]: os.path.join(folder_path, file) 
                          for file in os.listdir(folder_path) if file.endswith('.csv')}
        
            
            # Assuming process_files_and_get_best_year is a method to handle file processing and get the best year
            wlr_good_year = {}
            wlr_results, wlr_good_year = water_linear_regression.process_files_and_get_years_with_good_r2(file_paths)
            #print("Results:", wlr_results)
            #print("Good Year:", wlr_good_year)

            # Assuming process_files_and_get_best_year is a method to handle file processing and get the best year
            wrf_good_year = {}
            wrf_results, wrf_good_year = Water_Random_Forest.process_files_and_get_years_with_good_r2(file_paths)
            #print("Results:", wrf_results)
            #print("Good Year:", wrf_good_year)

            
            
            # dynamiclly create year tabs, such 2020, 2021, ...
            folder_path_2_find = os.path.join(current_path, 'Water', 'Graph')
            self.setupHydroTabs(folder_path_2_find, year_tabs_layout)
            
            prediction_temperature, prediction_precipitation = weather_forecast.get_weather_forecast()

            prediction_precipitation = 0.0  # Example precipitation
            predicted_water_use_wlr = water_linear_regression.predict_water_use(prediction_temperature, prediction_precipitation, file_paths, wlr_good_year)
            predicted_water_use_wrf = Water_Random_Forest.predict_water_use(prediction_temperature, prediction_precipitation, file_paths, wrf_good_year)
            print("Predicted Water Use linear:", predicted_water_use_wlr)
            print("Predicted Water Use forest:", predicted_water_use_wrf)


               

def main():
    app = QApplication(sys.argv)
    def reopen_start_dialog():
        while True:
            start_dialog = StartDialog()
            if start_dialog.exec_() == QDialog.Accepted:
                selected_option = start_dialog.get_selected_option()
                window = MyWindow(selected_option, reopen_start_dialog)
                window.show()
                break
            else:
                break
    reopen_start_dialog()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
