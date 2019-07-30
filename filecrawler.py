from flask import Flask
import app.db as db
import FrameWork.debug as debug
import FrameWork.TimeFunctions as tm
import app.MiddleWare as mw
import app.crawls as crawl
import vars
import os



#functions
app = Flask(__name__)
#routing
@app.route("/")
def main():
    #strPath=os.path.dirname(__file__) + vars._indexFile
    strPath=os.path.dirname(__file__) + vars._WelcomeFile
    debug.debugPrint("PATH FOUND: " + strPath)
    #print(strPath)
    debug.debugPrint("Reading file")
    strRet = mw.readHTMLFile(strPath)
    #mw.writeTxtFile()
    return strRet

@app.route("/crawl")
def crawler():
	retval= crawl.Crawl(vars.rootdir)
	return retval[1]


@app.route("/show")
def showfiles():
    print("showing")
    retVal= db.ShowAllFiles()
    #retVal=retVal.replace("@","<br>")
    #retVal= vars.strHTMLHeader + retVal
    #debug.debugPrint(retVal)
    strPath=os.path.dirname(__file__) + vars._indexFile
    strContent=mw.CreateTableContent(retVal)
    print("Content: " + strContent)
    #tm.SleepSeconds(5)
    strRet = mw.readHTMLFile(strPath).replace("%tbl_cntnt%",strContent)
    retVal = strRet

    return retVal


@app.route("/info")
def showInfo():
    strInfo, strDistinct, strMP3, strWav, strflv, strAvi =db.showInfo()
    strBMP, strJPG, strpng, strTiff = db.showPictureInfo()
    strDOC , strDOCX, strODT, strTXT = db.showDocumentInfo()
    strPY,strC,strBAS,strH, strCPP, strPY_L,strC_L,strBAS_L,strH_L,strCPP_L  = db.showProjectInfo()
    #strList=db.showGetInfoOnFileExtention()
    print("Collecting summery")
    #strSummery=db.getOverAllSummery()
    strSummery=""
    strPath=os.path.dirname(__file__) + vars._infoFile
    strHTML= mw.readHTMLFile(strPath).replace("%info%",strInfo).replace("%info2%",strDistinct).replace("%MP3%",strMP3).replace("%WAV%",strWav).replace("%summery%",strSummery).replace("%avi%",strAvi).replace("%flv%",strflv)
    strHTML=strHTML.replace("%BMP%",strBMP).replace("%JPG%",strJPG).replace("%PNG%",strpng).replace("%TIFF%",strTiff).replace("%DOC%",strDOC).replace("%DOCX%",strDOCX).replace("%ODT%",strODT).replace("%TXT%",strTXT)
    strHTML=strHTML.replace("%T_PY%",strPY).replace("%T_C%",strC).replace("%T_BAS%",strBAS).replace("%T_h%",strH)
    strHTML=strHTML.replace("%T_PY_L%",strPY_L).replace("%T_C_L%",strC_L).replace("%T_BAS_L%",strBAS_L).replace("%T_h_L%",strH_L).replace("%T_CPP_L%",strCPP_L).replace("%T_CPP%",strCPP)
    return strHTML

@app.route("/whipe")
def whipefiles():
    print("Clearing out database")
    strQuery="delete from FileNames"
    retVal= db.executeQuery(strQuery)
    return "Data Cleared"

@app.route("/nothing")
def donothing():
	return "nothing"


@app.route("/init")
def initsystem():
    strQuery="DROP TABLE FileNames;"
    print("Dropping table")
    retVal= db.executeQuery(strQuery)
    db.sql_table()
    return "Database Created"

@app.route('/test')
def dostuff():
    debug.debugPrint("Testing")
    db.dostuff()
    return "Done"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
