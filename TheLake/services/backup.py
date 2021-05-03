import pathlib
import os
import time

def backupDb(host="NA", port="NA", username="NA", password="NA"):
    outputDir = str(pathlib.Path().absolute())
    actualOutputDir = outputDir + "/backups/" + time.strftime("%d-%m-%Y-%H:%M:%S")

    command = "mongodump"
    if host != 'NA':
        command += " --host " + host
    if port != 'NA':
        command += " --port " + port
    if username != 'NA':
        command += " --username " + username
    if password != 'NA':
        command += " --password " + password
    
    command += " --out " + actualOutputDir
    
    os.system(command)

    print("mongo backup progress started")
