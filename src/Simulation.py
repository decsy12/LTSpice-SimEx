from SchematicMgr import *
from ResultsMgr import *
from Parser import *

def runBatchSimulation( netlistFilepath ):
    cmd = '"' + LTSPICE_PATH + '"' + ' ' + '-b' + ' ' + '"' + netlistFilepath + '"'

    print( f"Running cmd {cmd}" )
    
    subprocess.run( cmd, shell=True )
    
def simulation_cleanUpSimulationFiles( filename ):
    file_deleteFile( filename + '.net' )
    file_deleteFile( filename + '.log' )
    file_deleteFile( filename + '.op.raw' )
    
def simulation_run( schematicFilepath ):
    netFilepath = schematic_generateNetlist( schematicFilepath )
    runBatchSimulation( schematicFilepath )
    simulation_cleanUpSimulationFiles( file_getFileName( netFilepath ) )
    return netFilepath.replace( ".net", "" ) + '.raw'

def createToleranceStack( stack ):
    for set in stack:
        tolerance = set[1]
        direction = 0
        
        #TODO Add error handling
        if tolerance[0] == '+':
            direction = 1
            tolerance = tolerance.lstrip( '-' )
        elif tolerance[0] == '-':
            direction = -1
            tolerance = tolerance.lstrip( '-' )
            
        # Remove chars but save polarity
        numericPart = re.search( r'[+-]?(\d*.\d+|\d+)', tolerance ).group()
        
        # Divide by 100
        set[1] = ( float( numericPart ) * direction ) / 100
        
    return stack