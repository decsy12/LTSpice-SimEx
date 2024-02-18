import ltspice as lt
import matplotlib.pyplot as plt
from SchematicMgr import *

def results_plotWaveform( rawFilepath:str, netName:str, axesData, yAxisName ):
    l = lt.Ltspice( rawFilepath )
    l.parse()
    
    time = l.get_time()
    V1 = l.get_data( netName )
    
    plt.plot( time, V1 )
    plt.ylim( axesData[0], axesData[1] )
    plt.xlabel( 'Time (s)' )
    plt.ylabel( yAxisName )
    plt.grid()
    plt.show()
    

def results_plotMultiWaveforms( rawFilepath:str, netNames, axesData, yAxisName ):
    l = lt.Ltspice( rawFilepath )
    l.parse()
    
    fig, ( ax1, ax2 ) = plt.subplots( 2, 1, figsize=( 8, 6 ) )
    time = l.get_time()
    
    ax1.plot( time, l.get_data( netNames[0] ), label='Vout' )
    ax1.set_title('Vout')
    
    ax1.plot( time, l.get_data( netNames[1] ), label='Iin' )
    ax1.set_title('Iin')
    
    plt.set_title('Iin')
    
    plt.tight_layout()
    
    plt.show()