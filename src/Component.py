from Parser import *

componentPrefixLUT = [['p',     1e-12],
                      ['n',     1e-9 ],
                      ['u',     1e-6 ],
                      ['m',     1e-3 ],
                      ['k',     1e3  ],
                      ['Meg',   1e6  ]]

class Component():
    def __init__( self, fileInfo, instType, x, y, rotation, designator, value=None ):
        self.fileInfo = fileInfo
        self.componentName = instType
        self.designator = designator
        self.value = value
        self.x = x
        self.y = y
        self.valueSuffix = ''
        self.valueSuffixSN = 0
        self.rotation = rotation
        self.tolerance = 0.05
        self.parserInfo = []
        
    def apppendParseInfo( self, info_obj ):
        self.parserInfo.append( info_obj )
        
    def get_parseInfo( self ):
        return self.parserInfo
    
    def printParseInfo( self ):
        for obj in self.parserInfo:
            print( f"{str(obj.lineNumber)} : \t {str(obj.line).rstrip()}" )
            
    def extract_suffix( self, input_str ):
        try:
            match = re.search( r'[a-zA-Z]+$', input_str )
            return match.group() if match else None
        except TypeError:
            print( f"Error - could not find suffix for {input_str}" )
            
    def get_componentDesignatorPrefix( self ):
        match = re.match( r'([a-zA-Z]+)', self.designator )
        
        if match:
            return match.groupp(1)
        else:
            return None
        
    def get_valueAsString( self ):
        
        multiplier = 1        
        if self.value[1] == 'p':
            multiplier = 1e12
        if self.value[1] == 'n':
            multiplier = 1e9
        if self.value[1] == 'u':
            multiplier = 1e6
        if self.value[1] == 'm':
            multiplier = 1e3
        if self.value[1] == 'k':
            multiplier = 1e-3
        if self.value[1] == 'Meg':
            multiplier = 1e-6
            
        return str( round( self.value[0] * multiplier, 2 ) ) + self.value[1]
    

    def get_valueAsFloat( self ):
        number = float( re.sub( r'[a-zA-Z]', '', self.value[0] ) )
        
        multiplier = 1        
        if self.value[1] == 'p':
            multiplier = 1e-12
        if self.value[1] == 'n':
            multiplier = 1e-9
        if self.value[1] == 'u':
            multiplier = 1e-6
        if self.value[1] == 'm':
            multiplier = 1e-3
        if self.value[1] == 'k':
            multiplier = 1e3
        if self.value[1] == 'Meg':
            multiplier = 1e6
            
        return number * multiplier

    def set_valueSuffix( self, suffix:str ):
        if suffix == 'find':
            self.extract_suffix(self.value[1])
        else:
            self.valueSuffix = suffix
            
            
    def get_valueSuffix( self, suffix:str ):
        return self.valueSuffix
    
    def set_tolerancePer( self, tolPercent: str ):
        stripped_str = tolPercent.rstrip( '%' )
        self.set_toleranceDec( float( stripped_str ) / 100 )
        
    def set_toleranceDec( self, tolDecimal: float ):
        self.tolerance = tolDecimal
        
    def get_valueSuffixSN( self ):
        for i in componentPrefixLUT:
            if i[0] == self.valueSuffix:
                return i[1]
            
        return 1e0