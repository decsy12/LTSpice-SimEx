import sys
from SchematicMgr import *
from Simulation import *
from Parser import *
from PyQt6.QtWidgets import QFileDialog, QLineEdit, QPushButton, QGridLayout, QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QTextEdit, QTabWidget, QLabel

GUI_WINDOW_TITLE  = 'LTSPICE SIMEX'
GUI_WINDOW_WIDTH  = 800
GUI_WINDOW_HEIGHT = 400

tolerances = ["0.01%", "0.5%", "1%", "5%"]

MainWindow = None

class MainWindow( QMainWindow ):
    def __init__( self ):
        super().__init__()
        
        self.__selectedComponent = None
        self.__tolerance = None
        self.__componentList = None
        self.__sheetInfo = None
        
        self.setWindowTitle("Split GUI with Tab")
        self.setGeometry( 100, 100, 800, 600 )
        
        central_widget = QWidget( self )
        self.setCentralWidget( central_widget )
        
        layout = QVBoxLayout( central_widget )
        
        # Create blank left side with combo box
        self.blank_widget = QWidget( self )
        blank_layout = QVBoxLayout( self.blank_widget )
        
        # Adding log text box
        self.textEdit_log = QTextEdit( self )
        blank_layout.addWidget( self.textEdit_log )
        
        # Adding filepath text box
        self.lineEdit_filePath = QLineEdit(self)
        blank_layout.addWidget( self.lineEdit_filePath, stretch=1 )
        
        # Adding load button
        button_load = QPushButton( "Load", self )
        layout.addWidget( button_load, stretch=1 )
        
        # Adding top half of GUI
        layout.addWidget( self.blank_widget, stretch=1 )
        
        #-------------------------------------------------------------------------------#
        
        # Creating bottom simulation half of GUI
        sim_widget = QTabWidget( self )
        layout.addWidget( sim_widget, stretch=1 )
        
        self.comboBox_componentSelector = QComboBox( self )
        self.comboBox_toleranceSelector = QComboBox( self )
        self.button_tol = QPushButton( "Simulate", self )
        self.lineEdit_toleranceStack = QLineEdit( self )
        
        tab_tol = QWidget( self )
        sim_widget.addTab( tab_tol, "Tolerance Analysis" )
        tab_tol_layout = QVBoxLayout( tab_tol )
        tab_tol_layout.addWidget( self.comboBox_componentSelector )
        tab_tol_layout.addWidget( self.comboBox_toleranceSelector )
        tab_tol_layout.addWidget( self.lineEdit_toleranceStack )
        tab_tol_layout.addWidget( self.button_tol )
        self.comboBox_toleranceSelector.addItems( tolerances )
        tab_tol.setLayout( tab_tol_layout )
        
        tab_fault = QWidget( self )
        sim_widget.addTab( tab_fault, "Fault Analysis" )
        tab_fault.layout = QVBoxLayout( tab_fault )
        tab_fault.setLayout( tab_fault.layout )
        
        # -------------------------------------------------------------------------------#
        # Connect the button to a function
        self.button_tol.clicked.connect( self.run_tolerance_analysis )
        button_load.clicked.connect( lambda: self.loadSchematic( self.text_filePath.text() ) )
        
        # Connect combo box to a function
        self.comboBox_componentSelector.currentTextChanged.connect( self.componentChanged )
        self.comboBox_toleranceSelector.currentTextChanged.connect( self.toleranceChanged )
        
    def log( self, text ):
        self.textEdit_log.append( text )
        
        # Auto scroll to the bottom
        scroll_bar = self.textEdit_log.verticalScrollBar()
        scroll_bar.setValue( scroll_bar.maximum() )
        
    def loadSchematic( self, schematicFilepath ):
        if file_isFilepathValid( schematicFilepath ):
            self.log( f"Reading : {schematicFilepath}" )
            self.__sheetInfo = parser_parseFileForToken( schematicFilepath, 'SHEET' )
            self.__componentList = parser_parseFileForToken( schematicFilepath, 'SYMBOL' )
            
            arr = []
            for sym_obj in self.__componentList:
                arr.append( sym_obj.designator )
            self.comboBox_componentSelector.clear()
            self.comboBox_toleranceSelector.addItems(arr)
        else:
            self.log( f"{self.__selectedComponent} Tolerance = {self.comboBox_toleranceSelector.currentText()}" )
            
    def toleranceChanged( self ):
        #TODO Add support for non-resistor components'
        comboText = self.comboBox_toleranceSelector.currentText()
        tol_float = float( comboText.replace( '%', '' ) )
        self.__tolerance = tol_float
        self.log( f"{self.__selectedComponent} Tolerance = {self.comboBox_toleranceSelector.currentText()}" )
        
    def get_toleranceComboBox( self ):
        tolerance = self.comboBox_toleranceSelector.currentText()
        return float( tolerance.rstrip( '%' ) )
    
    def componentChanged( self ):
        self.__selectedComponent = self.comboBox_componentSelector.currentText()
        self.log( f"Selected component: {self.__selectedComponent}" ) 
        
    def parseToleranceBox( self ):
        tolerances = re.findall( r'{(.*?)}', self.lineEdit_toleranceStack.text() )
        toleranceInputs = []
        
        for tolerance in tolerances:
            params = tolerance.split()
            toleranceInputs.append( [element.strip() for element in params] )
        
        return createToleranceStack( toleranceInputs )
    
    def run_tolerance_analysis( self ):
        self.log( "Running tolerance analysis..." )
        
        # get component info
        comp = schematic_getComponent( self.__selectedComponent, self.__componentList )
        
        # copy file
        newFilepath = schematic_copySchmatic( comp, self.__tolerance )
        
        # update schematic info
        self.loadSchematic( newFilepath )
        
        # edit component value
        toleranceList = self.parseToleranceBox()
        
        for tolerance in toleranceList:
            targetComp = schematic_getComponent( tolerance[0], self.__componentList )
            targetComp.value[0] = targetComp.valueToFloat() * ( 1 + tolerance[1] )
            self.log( f"Setting {targetComp.designator} to {targetComp.valueToString()}" )
            schematic_changeResistorValue( newFilepath, targetComp, targetComp.valueToString() )
            
    def get_selected_component( self ):
        return self.__selectedComponent
    
#TODO dropdown box showing all components within schematic
#TODO selected component