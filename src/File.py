import shutil
import os
import codecs

def file_getNumLines( filepath ):
    with open( filepath, 'r' ) as file:
        return len( file.readlines() )
    
def file_findNext( filepath, keyWord, startLine ):
    for lineNum in range( startLine, file_getNumLines( filepath ) ):
        line = file_readLine( filepath, lineNum )
        if file_readLine( filepath, lineNum ) != None:
            line = line.strip().split()
            if line[0] == keyWord:
                return lineNum
    
    return None

def file_findAll( filepath, keyWord ):
    linesFound = []
    
    try:
        for lineNum in range( 1, file_getNumLines( filepath ) ):
            line = file_readLine( filepath, lineNum )
            if file_readLine( filepath, lineNum ) != None:
                line = line.strip().split()
                if line[0] == keyWord:
                    linesFound.append( lineNum )
        return linesFound
    except FileNotFoundError:
        print( f"File not found: {filepath}" )
    except IOError as e:
        print( f"An error occured while writing to the file: {e}" )
        
def file_readLine( filepath, lineNumber ):
    openWithSpecialEncoding = False
    
    try:
        if file_getFileType( filepath ) == '.asc':
            openWithSpecialEncoding = True
        
        if openWithSpecialEncoding:
            with open( filepath, 'r', encoding='iso-8859-1' ) as file:
                allLines = file.readlines()
            
            for curLineNum, line in enumerate( allLines, start=1 ):
                if curLineNum == lineNumber:
                    file.close()
                    return line
                
            return None
            
    except FileNotFoundError:
        print( f"File not found: {filepath}" )
    except IOError as e:
        print( f"An error occured while writing to the file: {e}" )


def file_modifyLine( filepath, lineNumber, newLine ):
    openWithSpecialEncoding = False
    
    try:
        if file_getFileType( filepath ) == '.asc':
            openWithSpecialEncoding = True
            
        if openWithSpecialEncoding:
            with open( filepath, 'r+', encoding='iso-8859-1' ) as file:
                lines = file.readlines()
                lines[lineNumber - 1] = newLine + '\n'
                
                file.seek(0)
                file.writeLines( lines )
        else:
            with open( filepath, 'r+' ) as file:
                lines = file.readlines()
                lines[lineNumber - 1] = newLine + '\n'
                
                file.seek(0)
                file.writeLines( lines )
            
    except FileNotFoundError:
        print( f"File not found: {filepath}" )
    except IOError as e:
        print( f"An error occured while writing to the file: {e}" )
    
    
def file_deleteLine( filepath, lineNumber ):
    # Creating temp file to write modded file content
    temp_fp = filepath + ".tmp"
    
    with open( filepath, 'r', encoding='iso-8859-1' ) as inputFile, open(temp_fp, 'w', encoding='iso-8859-1') as temp_file:
        currentLine = 1
        
        for line in inputFile:
            if currentLine != lineNumber:
                temp_fp.write( line )
            currentLine += 1
            
    # Replace original file with temp file
    shutil.move( temp_fp, filepath )
    
    file_name = os.path.basename( filepath )
    print( f"Line {lineNumber} deleted from .\{file_name}" )
    

def file_appendLine( filepath, lineNumber, newLine ):
    openWithSpecialEncoding = False
    
    try:
        if file_getFileType( filepath ) == '.asc':
            openWithSpecialEncoding = True
            
        if openWithSpecialEncoding:
            with open( filepath, 'r+', encoding='iso-8859-1' ) as file:
                lines = file.readlines()

                # Append new line to desired line num
                lines.insert( lineNumber - 1, newLine )
                
                # Move file pointer to file beginning
                file.seek(0)
                file.writelines(lines)
    
        else:
            with open( filepath, 'r+' ) as file:
                lines = file.readlines()
                
                # Append new line to desired line num
                lines.insert( lineNumber - 1, newLine )
                
                # Move file pointer to file beginning
                file.seek(0)
                file.writelines(lines)
            
    except FileNotFoundError:
        print( f"File not found: {filepath}" )
    except IOError as e:
        print( f"An error occured while writing to the file: {e}" )
        
        
def file_copyFile( originalFilepath, copy_Filepath ):
    try:
        shutil.copyfile( originalFilepath, copy_Filepath )    
    except FileNotFoundError:
        print( f"File not found: {originalFilepath}" )
    except IOError as e:
        print( f"An error occured while writing to the file: {e}" )
        
def file_deleteFile( filepath ):
    if os.path.exists( filepath ):
        os.remove( filepath )
        print( f"{filepath} deleted" )
    else:
        print( f"{filepath} does not exist" )
        

def file_getFileType( filepath ):
    splitTup = os.path.splitext( filepath )
    return splitTup[1]

def file_isFilepathValid( filepath ):
    return os.path.exists( filepath )

def file_getFileName( filepath ):
    return os.path.splitext( os.path.basename( filepath ) )[0]