# Introduction Serial Communications with a MicroController
#

#Import the necessary libraries
from PyQt5.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QLabel,
                             QGridLayout,
                             QPushButton,
                             QErrorMessage,
                             QInputDialog,
                             QSlider,
                             QAction)
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QIcon

import serial
import serial.tools.list_ports

#Define the main window class that inherits the predifined QMainWindow object.
class MainWindow(QMainWindow):
    # All classes (objects) have an __init__() function that is executed when the 
    # class is instanciated. This runs when an instance of the object is created.
    def __init__(self):
        #The super command makes sure the inhereted class is also initiated. 
        super().__init__()

        
        self.comport = None
        self.ser = None
        self.statusBar().showMessage("No Device Connected.")
        
        #We call a function to initialize the user interface. 
        self.init_ui()

    # Now define the function that initializes the user interface.
    # all functions within a class need to reference itself.
    def connect_to_serial(self):
        #Connect to the Teensy using a serial port. This will be different for everyone
        #Mac computers will us /dev/tty* 
        #The Arduino Software can tell you what your com port is.
        
        # See http://pyserial.readthedocs.io/en/latest/tools.html
        available_ports = sorted(serial.tools.list_ports.comports(),reverse=True)
        
        port_choices = []
        for p in available_ports:
            if "16C0" in p.hwid: #This identifies a Teensy
                port_choices.append("{}: {}".format(p.device,p.description))
        
        # Open a dialog box to get the COM port.
        com_port_text, ok = QInputDialog.getItem(self, 'Select Serial Port', 
            'Available Ports:', port_choices, 0, False)
        
        if ok and com_port_text:
            #extract just the device string
            self.comport = com_port_text.split(":")[0]
            # This code runs when the user has selected a COM port.
            # Use a try-except block to help troubleshoot connectivity problems.
            try:
                self.ser = serial.Serial(self.comport)
                self.statusBar().showMessage(self.comport)
            except Exception as e:
                error_dialog = QErrorMessage()
                error_dialog.showMessage(repr(e))
                error_dialog.exec_()
        else:
            self.statusBar().showMessage("Serial Port Not Connected.")
    def serial_error(self):
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Serial Port Not Responding.')
            error_dialog.exec_()

    def init_ui(self): 
         
        # Build common menu options
        menubar = self.menuBar()
        
        # Connection Menu Items
        connect_menu = menubar.addMenu('&Connect')
        connect_serial = QAction(QIcon(r'icons/icons8_Connected_48px.png'), '&Connect Serial Port', self)
        connect_serial.setShortcut('Ctrl+Shift+C')
        connect_serial.triggered.connect(self.connect_to_serial)
        connect_menu.addAction(connect_serial)

        # Let's make a simple label widget to keep track of a count
        self.slider_label = QLabel("LED Blink Spacing")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(20)
        self.slider.setMaximum(1000)
        self.slider.setTickInterval(20)
        self.slider.setSingleStep(5)
        self.slider.valueChanged.connect(self.send_slider)
        
        self.slider_label = QLabel("Blink Rate: 20 ms")

        LED_button = QPushButton("Press and hold for LED")
        LED_button.pressed.connect(self.send_LED_ON)        
        LED_button.released.connect(self.send_LED_OFF)        
        

        toolbar = self.addToolBar("Main")
        toolbar.addAction(connect_serial)

        ###
        # Assignment
        # 1. Make a button that turns on the LED when pressed and turns it off when released.
        # 2. Add a label that gets updated from the serial messages from the Teensy. You'll have to set up a thread
        #    and queue to run the processes asynchronously.
        # 3. Make a widget with menu item that let's the user select the COM port
        ####

        #Define a main widget that will contain all the other widgets and set
        #it as the central widget. 
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        #A layout manager is needed to put things where we want. Let's use a grid.
        grid_layout = QGridLayout(main_widget)
        #assign the label to the grid.
        grid_layout.addWidget(self.slider_label,0,0,1,1)
        #assign the slider to the grid
        grid_layout.addWidget(self.slider,1,0,1,1)
        #assign the button to the grid
        grid_layout.addWidget(LED_button,2,0,1,1)

        #Setup the window title and make it appear
        self.setWindowTitle("Blink Rate App")
        self.show() #This is needed for the window to appear.
    
    def send_slider(self):
        #put together a string that holds the current numerical value for the slider.
        command_string = "{}".format(self.slider.value())
        self.send_serial(command_string)
    
    def send_LED_OFF(self):
        self.send_serial("OFF")

    def send_LED_ON(self):
       self.send_serial("ON")


    def send_serial(self,command_string):
        #See what we plan on sending. 
        print(bytes(command_string,'ascii'))
        #Send the command as a bytes string
        try:
            self.ser.write(bytes(command_string+'\n','ascii'))
            #get some feedback that the command worked.
            rate = self.ser.readline().decode('ascii','ignore').strip() #remove whitespace

            self.slider_label.setText("Blink Rate: {} ms".format(rate))

        except Exception as e:
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage(repr(e) + "\nPlease reconnect the serial device.")
            error_dialog.setWindowModality(Qt.ApplicationModal)
            error_dialog.exec_() 
    
# This line is run when the to get everything started.      
if __name__ == '__main__':
    app = QApplication([]) #The empty list ([]) is passed inplace of system arguments.
    execute = MainWindow() #Calls the main window class we defined earlier.
    app.exec_() #this starts the event handling loop to accept interaction.