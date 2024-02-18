import copy
import re
from File import *
from Component import *

DEFAULT_TOLERACNE = 0.05

TYPE_OFFSET = 0

SYMBOL_NAME_OFFSET = 1
SYMBOL_XPOS_OFFSET = 2
SYMBOL_YPOS_OFFSET = 3
SYMBOL_ROT_OFFSET  = 4

STMATTR_NAME_OFFSET  = 1
SYMATTR_PARAM_OFFSET = 2

WIRE_X1POS_OFFSET = 1
WIRE_X2POS_OFFSET = 3
WIRE_Y1POS_OFFSET = 2
WIRE_Y2POS_OFFSET = 4

FLAG_XPOS_OFFSET = 1
FLAG_YPOS_OFFSET = 2
FLAG_NAME_OFFSET = 3

SHEET_NUMBER_OFFSET = 1
SHEET_XSIZE_OFFSET  = 2
SHEET_YSIZE_OFFSET  = 3

#TODO Investigate what the first parameter in the WINDOW line does
WINDOW_UNKNOWN_OFFSET   = 1
WINDOW_XPOS_OFFSET      = 2
WINDOW_YPOS_OFFSET      = 2
WINDOW_ALIGNMENT_OFFSET = 3
WINDOW_TEXTSIZE_OFFSET  = 4

SYMATTR_INSTRUCTION = ['NAME', 'VALUE']

#TODO Support WINDOW text extraction
#TODO Move all parsing config to a seperate config or JSON file
#TODO Consolidate a better object layout using inheritance

class Sheet():
    def __init__( self, sheetNumber, xSize, ySize ):
        self.number = sheetNumber
        self.size_x = xSize
        self.size_y = ySize
        self.parserInfo = []
        
        #TODO Add list of component, the sheet object should contain everything that is in the sheet
        #    ---------SHEET--------
        #   /             \        \
        #  COMPONENT    TEXT      SPICE_DIRECTIVES
        
    def appendParseInfo( self, info_obj ):
        self.parserInfo.append( info_obj )
        
    def getParseInfo( self ):
        return self.parserInfo
    
    def printParseInfo( self ):
        for obj in self.parserInfo:
            print( f"{str(obj.lineNumber)} : \t {str(obj.line).rstrip()} \t\t {obj.parameterName}" )
            


class ParseInfo():
    def __init__( self, filepath, line, lineNumber, paramType = None ):
        self.fp = filepath
        self.line = line
        self.lineNumber = lineNumber
        self.parameterName = paramType
        
    def appendLine( self, line ):
        self.line.append( line )
        

def parser_printAllParseInfo( sym_list ):
    #TODO Add a check if sheet or symbol class
    for sym_obj in sym_list:
        sym_obj.printParseInfo()
        
        
def parser_printComponent( sym_obj: Component ):
    print( "TPYE\t\t\tDESIGNATOR\t\tVALUE\t\tX\y\yY\t\tROTATION" )
    print( "----\t\t\t----------\t\t-----\t\t---\t\t---\t\t----------" )
    print( str(sym_obj.componentName) + '\t\t\t\t' + str(sym_obj.designator) + '\t\t\t' + str(sym_obj.value) + '\t\t' + str(sym_obj.x) + '\t\t' + str(sym_obj.y) + '\t\t' + str(sym_obj.rotation) )
    
def parser_printComponents( sym_list ):
    print( "TPYE\t\t\tDESIGNATOR\t\tVALUE\t\tX\y\yY\t\tROTATION" )
    print( "----\t\t\t----------\t\t-----\t\t---\t\t---\t\t----------" )
    for sym_obj in sym_list:
        print( str(sym_obj.componentName) + '\t\t\t\t' + str(sym_obj.designator) + '\t\t\t' + str(sym_obj.value) + '\t\t' + str(sym_obj.x) + '\t\t' + str(sym_obj.y) + '\t\t' + str(sym_obj.rotation) )

def parser_lineType( filepath, lineNum ):
    line = file_readLine( filepath, lineNum )
    tokens = line.split()
    return tokens[TYPE_OFFSET]

def parser_parseLine( filepath, type, line, lineNum = 0, passObj=None ):
    Obj = None
    if type == 'SYMBOL':
        info_obj = ParseInfo( None, None, None, None )
        Obj = Component( None, None, None, None, None, None, None )
        info_obj.fp = filepath
        info_obj.line = line
        info_obj.lineNumber = lineNum
        
        tokens = line.strip().split()
        Obj.componentName   = tokens[SYMBOL_NAME_OFFSET]
        Obj.x               = int( tokens[SYMBOL_XPOS_OFFSET] )
        Obj.y               = int( tokens[SYMBOL_YPOS_OFFSET] )
        Obj.rotation        = tokens[SYMBOL_ROT_OFFSET]
        Obj.tolerance       = DEFAULT_TOLERACNE
        Obj.apppendParseInfo( copy.deepcopy(info_obj) )
        
        # Grab following symbol attributes
        attrLineNum = file_findNext( filepath, 'SYMATTR', lineNum )
        inc = 0
        while parser_lineType( filepath, lineNum = attrLineNum + inc ) == 'STMATTR':
            parser_parseLine( filepath, type = 'SYMATTR', passObj = Obj, lineNum = attrLineNum + inc, line = file_readLine( filepath, attrLineNum + inc ) )
            inc += 1
            
    elif type == 'SYMATTR':
        tokens = line.split()
        
        info_obj = ParseInfo( None, None, None, None )
        info_obj.fp = filepath
        info_obj.line = line
        info_obj.lineNumber = lineNum
        info_obj.parameterName = tokens[SYMATTR_PARAM_OFFSET]
        info_obj.appendParseInfo( copy.deepcopy( info_obj ) )
        
        if info_obj.parameterName == 'InstName':
            passObj.designator = tokens[SYMATTR_PARAM_OFFSET]
            
        elif info_obj.parameterName == 'Value':
            paramText = tokens[SYMATTR_PARAM_OFFSET]
            if paramText.startswith( "PULSE(" ):
                passObj.value = line[line.index("PULSE(") + len("PULSE("):line.rindex(")")]
            elif paramText.startswith( "PWL(" ):
                passObj.value = line[line.index("PWL(") + len("PWL("):line.rindex(")")]
            else:
                passObj.value = [parser_stripSuffix( paramText ), passObj.extract_suffix( paramText )]
                passObj.set_valueSuffix( passObj.extract_suffix( paramText ) )
            
        elif info_obj.parameterName == 'SpiceLine':
            paramText = tokens[SYMATTR_PARAM_OFFSET]
            match = re.search( r'tol=(\d+\.\d+)', paramText )
            passObj.set_tolerancePer( match.group(1)+'%' )
            
        else:
            pass
                
    elif type == 'SHEET':
        info_obj = ParseInfo( None, None, None, None )
        info_obj.fp = filepath
        info_obj.line = line
        info_obj.lineNumber = lineNum
        Obj = Sheet( None, None, None )
        tokens = line.strip().split()
        Obj.number = int( tokens[SHEET_NUMBER_OFFSET] )
        Obj.size_x = int( tokens[SHEET_XSIZE_OFFSET] )
        Obj.size_y = int( tokens[SHEET_YSIZE_OFFSET] )
        Obj.appendParseInfo( copy.deepcopy( info_obj ) )
    
    elif type == 'FLAG':
        pass
    
    elif type == 'WIRE':
        pass
    
    else:
        return -1
    
    return Obj


def parser_parseFileForToken( filepath, token ):
    objList = []
    lines = file_findAll( filepath, token )
    
    print( f"Parsing {filepath} for {token}" )                
    
    for i in range(0, len(lines)):
        objList.append( parser_parseLine( filepath, type = token, line = file_readLine( filepath, lines[i] ), lineNum=lines(i) ) )
        
    return objList
                
def parser_stripSuffix( strValue ):
    return re.sub( r'[a-zA-Z]', '', strValue )