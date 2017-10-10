# Introduction Serial Communications with a MicroController
#

#Import the necessary libraries
from PyQt5.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QLabel,
                             QGridLayout,
                             QPushButton,
                             QSlider,
                             QAction)
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QIcon

import serial

#Define the main window class that inherits the predifined QMainWindow object.
class MainWindow(QMainWindow):
    # All classes (objects) have an __init__() function that is executed when the 
    # class is instanciated. This runs when an instance of the object is created.
    def __init__(self):
        #The super command makes sure the inhereted class is also initiated. 
        super().__init__()

        #Connect to the Teensy using a serial port. This will be different for everyone
        #Mac computers will us /dev/tty* 
        #The Arduino Software can tell you what your com port is.
        self.comport = None
        self.ser = None
        
        #We call a function to initialize the user interface. 
        self.init_ui()

    # Now define the function that initializes the user interface.
    # all functions within a class need to reference itself.
    def connect_to_serial(self):
        if self.comport is None:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Oh no!')
        else:
            self.ser = serial.Serial(self.comport)

    def init_ui(self): 
        
        # A simple example of some built in functionality is the status bar.
        self.statusBar().showMessage(self.comport)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(20)
        self.slider.setMaximum(1000)
        self.slider.setTickInterval(20)
        self.slider.setSingleStep(5)
        self.slider.valueChanged.connect(self.send_serial)
        

        # Let's make a simple label widget to keep track of a count
        self.slider_label = QLabel("LED Blink Spacing")

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
        #assign the button to the grid
        grid_layout.addWidget(self.slider,1,0,1,1)

        #Setup the window title and make it appear
        self.setWindowTitle("Blink Rate App")
        self.show() #This is needed for the window to appear.
    
    def send_serial(self):
        #put together a string that holds the current numerical value for the slider.
        command_string = "{}".format(self.slider.value())
        #See what we plan on sending. 
        print(bytes(command_string,'ascii'))
        #Send the command as a bytes string
        self.ser.write(bytes(command_string,'ascii'))
        #get some feedback that the command worked.
        print(self.ser.readline()) 
    
# This line is run when the to get everything started.      
if __name__ == '__main__':
    app = QApplication([]) #The empty list ([]) is passed inplace of system arguments.
    execute = MainWindow() #Calls the main window class we defined earlier.
    app.exec_() #this starts the event handling loop to accept interaction.