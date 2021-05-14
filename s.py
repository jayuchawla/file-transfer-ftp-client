import os
from ftplib import FTP
from jproperties import Properties
import progressbar

def connectToServer(MODE, HOST, PORT, USERNAME, PASSWORD):

    ftp = None
    
    if(isinstance(PORT, str)):
        PORT = int(PORT)

    if MODE == "a":
        ftp = FTP()
        ftp.connect(HOST, PORT)
        ftp.login(USERNAME, PASSWORD)
    else:
        ftp = FTP(HOST, USERNAME, PASSWORD)
    
    ftp.encoding="utf-8"
    print(ftp.getwelcome())
    return ftp
    

def getFromServer(filepath, ftp, generatedFilepath):
    # extracting extension and traversing to directory where file is present on host
    filename=filepath.split("/")[-1]
    ext=filename.split(".")[-1]
    filepath="/".join(filepath.split("/")[:-1])
    ftp.cwd(filepath)

    # sanitise filename on client
    outputFilename = generatedFilepath.split("\\")[-1]
    sanitisedOutputFilename = ".".join(outputFilename.split(".")[:-1]) + "." +ext
    outputFilePath = "/".join(generatedFilepath.split("\\")[:-1])


    filesize=ftp.size(filename)
    try:
        down_progress = progressbar.AnimatedProgressBar(end=filesize, width=50)
        with open(outputFilePath + sanitisedOutputFilename, 'wb') as f:
            def download_progress(chunk):
                f.write(chunk)
                down_progress + len(chunk)
                down_progress.show_progress()

            print('downloading: {} | size: {}'.format(filename, filesize))
            ftp.retrbinary('RETR {}'.format(filename), download_progress)
            print('\n{} successfully downloaded'.format(filename))
    except Exception as exc:
        print('Error downloading file {}!'.format(filename), exc)


def storeOnServer(filepath, ftp, filename):
    with open(filepath, 'rb') as f:
        ftp.storbinary("STOR %s"%filename, f)

def getProps():
    configs=Properties()
    with open('app.properties', 'rb') as f:
        configs.load(f)
    return configs

def closeConnection(ftp):
    if not ftp is None:
        ftp.quit()

if __name__ == '__main__':
    
    configs ={}
    for item in getProps().items():
        configs[item[0]] = item[1].data
    
    ftp=connectToServer (
        configs['MODE'], 
        configs['HOST'], 
        configs['PORT'], 
        configs['USERNAME'], 
        configs['PASSWORD']
    )
    
    #storeOnServer("F:\\work_learning\\python_practice\\ftp\\s\\s.docx", ftp, 'jayu.docx')
    getFromServer(configs['serverFilePath'], ftp, configs['storeAsFilepath'])
    # print(ftp.dir())

    closeConnection(ftp)
  
    # # ftp.cwd('/Temp2/')
    # #serverfilepath='/Temp2/tabooheat.21.04.17.cory.chase.and.melanie.hicks.stuck.step.family.mp4'
    # serverfilepath='/Temp2/H.docx'
    # ftp.retrbinary('RETR %s'%serverfilepath, transfer('F:\\work_learning\\python_practice\\ftp\\s\\s.docx'))


