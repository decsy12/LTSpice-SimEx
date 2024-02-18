import os
import subprocess
from Parser import *
from Component import *

SHORT_VALUE = '0.01'

TEST_SPOT_X = -976
TEST_SPOT_Y = 144
GRID_SIZE   = 16

BASE_DIRECTORY_FP   = 'C:\\Users\\Declan\\Documents\\Projects\\LTSpice_SimEx\\'
FILE_TYPE           = '.asc'
SCHEMATIC_FILE_TYPE = 'Test3.asc'
COPY_FILE_NAME      = 'TestCopy' + FILE_TYPE
FP                  = BASE_DIRECTORY_FP + COPY_FILE_NAME
LTSPICE_PATH        = 'C:\\Program Files\\LTSpice\\LTspiceXVII\\XVIIx64.exe'
TEMPLATE_FP         = BASE_DIRECTORY_FP + SCHEMATIC_FILE_TYPE



def schematic_snapToGrid_x( schematicSym_obj ):
    return round( schematicSym_obj.size_x / GRID_SIZE ) * GRID_SIZE



def schematic_snapToGrid_y( schematicSym_obj ):
    return round( schematicSym_obj.size_y / GRID_SIZE ) * GRID_SIZE



def schematic_getComponent( designator, componentList ):
    for component_obj in componentList:
        if component_obj.designator == designator:
            return component_obj
        
        
        
def schematic_fetchAllComponents( componentList, componentPrefix: str ):
    targetList = []
    
    for component_obj in componentList:
        prefix = component_obj.get_componentDesignatorPrefix()
        if component_obj.get_componentDesignatorPrefix() == componentPrefix:
            targetList.append(component_obj)
    
    return targetList



def schematic_insertNet( filepath, x, y, name ):
    newNet = 'FLAG'+' '+str(x)+' '+str(y)+' '+name+'\n'
    file_appendLine( filepath, file_findNext( filepath, 'FLAG', 1 ), newNet )
    
    
    
def schematic_insertWire( filepath, x1, y1, x2, y2 ):
    newWire = 'WIRE'+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+' '+'\n'
    file_appendLine( filepath, file_findNext( filepath, 'WIRE', 1 ), newWire )
    
    
    
def schematic_insertResistor( filepath, x, y, rotation, name, value ):
    if rotation == 'V':
        R = 'R0'
    elif rotation == 'H':
        R = 'R90'
        
    newR_1 = 'SYMBOL'+' '+'res'+' '+str(x)+' '+str(y)+' '+str(R)+'\n'
    newR_2 = 'SYMATTR'+' '+'InstName'+' '+str(name)+'\n'
    newR_3 = 'SYMATTR'+' '+'Value'+' '+str(value)+'\n'
    
    file_apppendLine( filepath, file_findNext( filepath, 'SYMBOL', 1 )   , newR_1 )
    file_apppendLine( filepath, file_findNext( filepath, 'SYMBOL', 1 )+1 , newR_2 )
    file_apppendLine( filepath, file_findNext( filepath, 'SYMBOL', 1 )+2 , newR_3 )
    
    
    
def schematic_placeNetsAtResistor( filepath, targetResistor_obj: Component, name ):
    if targetResistor_obj.rotation == 'R0':
        RESISTOR_PIN1_OFFSET_X = +1*GRID_SIZE
        RESISTOR_PIN1_OFFSET_Y = +1*GRID_SIZE
        RESISTOR_PIN2_OFFSET_X = +1*GRID_SIZE
        RESISTOR_PIN2_OFFSET_Y = +6*GRID_SIZE
    if targetResistor_obj.rotation == 'R90':
        RESISTOR_PIN1_OFFSET_X = -6*GRID_SIZE
        RESISTOR_PIN1_OFFSET_Y = +1*GRID_SIZE
        RESISTOR_PIN2_OFFSET_X = -1*GRID_SIZE
        RESISTOR_PIN2_OFFSET_Y = +1*GRID_SIZE
    if targetResistor_obj.rotation == 'R270':
        RESISTOR_PIN1_OFFSET_X = +1*GRID_SIZE
        RESISTOR_PIN1_OFFSET_Y = -1*GRID_SIZE
        RESISTOR_PIN2_OFFSET_X = +6*GRID_SIZE
        RESISTOR_PIN2_OFFSET_Y = -1*GRID_SIZE
    
    schematic_insertNet( filepath, targetResistor_obj.x+RESISTOR_PIN1_OFFSET_X, targetResistor_obj.y+RESISTOR_PIN1_OFFSET_Y, name + '_1' )
    schematic_insertNet( filepath, targetResistor_obj.x+RESISTOR_PIN2_OFFSET_X, targetResistor_obj.y+RESISTOR_PIN2_OFFSET_Y, name + '_2' )
    
    
    
    
def schematic_removeComponent( sym_obj: Component ):
    for paramParseInfo in sym_obj.parseInfo:
        file_deleteLine( paramParseInfo.fp, paramParseInfo.lineNumber )
        
        
        
def schematic_changeResistorValue( filepath: str, sym_obj: Component, newValue: str ):
    #TODO Make generic, add handling of any passive component
    sym_obj.value = newValue
        
    fileInfo_obj = sym_obj.getParseInfo()
    
    newLine = f"SYMATTR Value {newValue}"
    
    # Edit the file text
    for info in fileInfo_obj:
        if info.parameterName == 'Value'
        file_modifyLine( filepath, info.lineNumber, newLine )
        
        
        
def schematic_shortComponent( filepath, sym_obj: Component ):
    schematic_insertResistor( filepath, TEST_SPOT_X, TEST_SPOT_Y, 'V', 'R_SHORT', SHORT_VALUE )
    
    tempSymbols = parser_parseFileForToken( filepath, 'SYMBOL' )
    
    schematic_placeNetsAtResistor( filepath, schematic_getComponent( 'R_SHORT', tempSymbols ), 'RSHORT' )
    schematic_placeNetsAtResistor( filepath, sym_obj, 'RSHORT' )
    
    
    
def schematic_copySchmatic( sym_obj: Component, extraInfo = " " ):
    fileInfo = sym_obj.parserInfo
    
    baseFileName = file_getFileName( fileInfo[0].fp )[0]
    info = str(extraInfo).replace('.','-')
    
    copyFileName = baseFileName+'-'+sym_obj.designator+('_' + info if info != None else '')
    copyFileName = BASE_DIRECTORY_FP + copyFileName + '.asc'
    
    file_deleteFile( coppyFilePath )
    file_copyFile( TEMPLATE_FP, copyFileName )
    
    return copyFileName


def schematic_generateNetlist( schematicFilePath ):
    cmd = '"' + LTSPICE_PATH + '"' + ' ' + '-netlist' + ' ' + '"' + schematicFilePath + '"'
    
    subprocess.run( cmd, shell=True )
    
    print( f"Returning {BASE_DIRECTORY_FP + file_getFileName( schematicFilePath ) + '.net'}" )
    return BASE_DIRECTORY_FP + file_getFileName( schematicFilePath ) + '.net'


