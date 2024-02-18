import numpy as np

def LTspice2Matlab( filename, *varargin ):
    # Initialise input structure
    raw_data = {}
    
    # Process function args
    if len( varargin ) == 0:
        selected_vars = 'all'
        downsamp_N = 1
    elif len( varargin ) == 1:
        selected_vars = varargin[0]
        if isinstance( selected_vars, str ):
            selected_vars = selected_vars.lower()
        downsamp_N = 1
    elif len( varargin ) == 2:
        selected_vars = varargin[0]
        if isinstance( selected_vars, str ):
            selected_vars = selected_vars.lower()
        downsamp_N = varargin[1]
    
    else:
        raise ValueError( 'LTspice2Matlab takes 1, 2, or 3 input parameters. Type "help LTspice2Matlab" for details' )
    
    if len( np.shape( downsamp_N ) ) != 0 or not isinstance( downsamp_N, ( int, np.integer ) ) or np.isnan( downsamp_N ) or downsamp_N % 1 != 0 or downsamp_N <= 0:
        raise ValueError( 'Optional parameter DOWNSAMP_N must be a positive integer >= 1' )
    
    # Try oppen file
    filename = filename.strip()
    
    fid = open( filename, 'rb' )
    
    print(fid)