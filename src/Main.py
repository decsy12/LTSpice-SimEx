from File import *
from Parser import *
from SchematicMgr import *
from GUI import *
from ToleranceGen import *
from RawReader import *
import pandas as pd

#--STORIES--#
#TODO Implement netlist parser
#TODO Store component value change in history structure
#TODO FSMs for simulation sequences
#TODO IC Pin support
#TODO Support net placement across all components
#TODO Timed fault support
#TODO Add tolerance system
#TODO Better error handling
#TODO Make Singletons and more things into classes

#--EPICS--#
#TODO Program should serve as advanced sim tool
    #TODO Automated montecarlo
    #TODO Short & open circuits
    #TODO Sensitivity analysis [https://www.simetrix.co.uk/whatsnew/8.3/sensitivity-worst-case.html]
    #TODO Worst case analysis [PPerforms normal test, grabs nominal, sequnces simulations and determine delta from nominal]
    #TODO Convergence, accuracy, performance


def tmp_openComponent( sym_obj ):
    schematic_removeComponent( sym_obj )
    
if __name__ == "__main__":
    
    #NetlistFile_cls
        #History (changes)
        #filepath
        #Source schematic file
        #Component list
            #Parser information
            
    #Simulation_cls
        #State machine
        #fetched data
        
    '''
    In short/open circuit analysis user can select compponents-of-interest
        Caan set time to short certain components out
        Can determine delta at time t from which the net-under-test has deviated e.g. V(+5V)
    '''
    
    FILENAME = 'Test'
    schematicFilepath = BASE_DIRECTORY_FP + FILENAME + '.asc'
    
    netlistFilepath = schematic_generateNetlist( schematicFilepath )
    
    
    
    
    # originalFilepath = BASE_DIRECTORY_FP + FILENAME + '.asc'
    # targetNet = 'V(+5V)'
    # numSims = 3
    # filePathList = []
    # resistorValueList = []
    
    # for simN in range( 1, numSims ):
    #     copyFilepath = BASE_DIRECTORY_FP + FILENAME + '_copy' + str(simN) + '.asc'
    #     print( f"copyFilepath = {copyFilepath}" )
    #     file_copyFile( BASE_DIRECTORY_FP + FILENAME + '.asc', copyFilepath )
        
    #     componentList = parser_parseFileForToken( copyFilepath, 'SYMBOL' )
    #     resistorsList = schematic_fetchAllComponents( componentList, 'R' )
    #     toleranceList = []
        
    #     newValues = createToleranceTable( resistorsList, 'distribution' )
    #     resistorValueList.append( newValues )
        
    #     for value, resistor_obj in zip( newValues, resistorsList ):
    #         schematic_changeResistorValue( copyFilepath, resistor_obj, value )
            
    #     componentList = parser_parseFileForToken( copyFilepath, 'SYMBOL' )
    #     resistorsList = schematic_fetchAllComponents( componentList, 'R' )
        
    #     filePathList.append( simulation_run( copyFilepath ) )
        
    # for x in resistorValueList:
    #     print( x )
        
    """
    for i in range( 0, numSims-1 ):
        results_plotMultiWaveforms( filepathList[i], ['V(+5V)', 'V(voutlow_mon)'], [0,5], 'Voltage (V)' )
        
    # GUI #
    app = QApplication( sys.argv )
    window = myWindow()
    
    window.loadSchematic( BASE_DIRECTORY_FP + SCHEMATIC_FILE_NAME )
    
    window.show()
    sys.exit( app.exec() )
    
    """