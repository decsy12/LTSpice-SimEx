import math
import numpy as np

standardToleranceValues_dec = [0.05, 0.01, 0.005, 0.001, 0.0001]

def createToleranceTable( componentList, analysisType ):
    numComponents = len( componentList )
    newList = []
    
    i = 0
    if analysisType == 'distribution':
        for component_obj in componentList:
            newGaussValue = value_randomGauss( component_obj.get_valueAsFloat(), component_obj.tolerance )
            newGaussValue = ( round( newGaussValue * ( 1.0 / component_obj.get_valueSuffixSN() ), 2 ) ) * component_obj.get_valueSuffixSN()
            
            newList.append( newGaussValue )
            i += 1
            
    return newList

def binary( inc, idx ):
    math.floor( inc / ( 2 ** idx ) ) - 2 * math.floor( inc / ( 2 ** ( idx + 1 ) ) )
    
def tolerance_worstCase( inc, numSims, nominalResistance, tolerance, index ):
    if binary( inc, index ):
        nominalResistance * ( 1 + tolerance )
    else:
        nominalResistance * ( 1 - tolerance )
        
def value_randomGauss( value_dec, tolerance_dec ):
    maximumDeviation = 20
    mean = value_dec
    stdDev = value_dec * ( maximumDeviation / 100 )
    
    try:
        index = standardToleranceValues_dec.index( tolerance_dec )
    except:
        print( f"{tolerance_dec} is not in the array" )
        
    min_neg = value_dec - ( value_dec * standardToleranceValues_dec[index] )
    max_neg = value_dec - ( value_dec * standardToleranceValues_dec[index+1] )
    min_pos = value_dec + ( value_dec * standardToleranceValues_dec[index] )
    max_pos = value_dec + ( value_dec * standardToleranceValues_dec[index+1] )
    
    foundValue = 0 
    
    while not foundValue:
        newValue = np.random.normal( mean, stdDev )
        
        #TODO Make into LUT
        if ( min_neg <= newValue <= max_neg ) or ( min_pos <= newValue <= max_pos ):
            foundValue = 1
            
    return newValue