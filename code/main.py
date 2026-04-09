import requests
import subprocess
import os
import time
import asyncio
import vt


print()
print("File Scanner by J1D1")
print("This program uses VirusTotal API to scan files")
print()
print("This program was only tested on Windows, it may not work on other systems.")
print()



while True:
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    print()
    print("Checking if VirusTotal is up and running...")
    try:
        virustotalstatus = int(requests.get("https://www.virustotal.com/gui/home/upload").status_code)
        break
    except Exception as e:
        print()
        print("There has been an error while trying to reach VirusTotal servers")
        print("Please check your internet connection and try again")
        print()
        whattodoaftererror = input("Type \"See More\" to display more info about the error, \"Retry\" to retry or \"Exit\" to quit the program: ").lower()
        if whattodoaftererror == "retry":
            pass
        elif whattodoaftererror == "exit":
            exit()
        elif whattodoaftererror == "see more":
            print()
            print(e)
            print()
            input("Press any key to continue...")
print()


if virustotalstatus == 200:
    print("VirusTotal is up and running")
    print()
    print("Starting...")
    print()
elif virustotalstatus:
    print("There has been an error")
    print("Error code:", virustotalstatus)

time.sleep(3)
subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
print()

inuseapikey = None
def askforapikey():
    global inuseapikey
    print()
    inuseapikey = input("Enter your VirusTotal API key: ")
    storeapikey = input("Do you want to store the api key? y/n: ").lower()
    if storeapikey == "y":
        open("stored_api_key.apikey", "w").flush()
        open("stored_api_key.apikey", "w").write(inuseapikey)
        print()
        print("Api key stored")
        print()
        print("Using provided api key...")
    elif storeapikey == "n":
        print()
        print("The key will not be written down")
        print()
        print("Using provided api key...")
    else:
        exit()

storedinfileapikey = open("stored_api_key.apikey", "r").read()
if storedinfileapikey:
    print("Api key found in storage")
    print()
    usestoredapikey = input("Use stored api key? y/n: ").lower()
    if usestoredapikey == "y":
        inuseapikey = storedinfileapikey
        print("Using stored api key...")
    elif usestoredapikey == "n":
        askforapikey()
    else:
        exit()
else:
    print()
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    print("No api key has been found in storage")
    askforapikey()

time.sleep(2)
print()
while True:
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    pathtofile = input("Enter the path to the file you want to scan: ")
    if os.path.isfile(pathtofile):
        confirmedpath = pathtofile
        break
    else:
        print("Error")
        print("The selected file does not exist, was moved or renamed")
        time.sleep(2)

# In the next code, the part where the asyncio module is used was mainly written by AI because I don't know how to use it (apart from that, everything is written by me, J1D1)
async def main():
    with open(pathtofile, "rb") as filetoscan:
        async with vt.Client(inuseapikey) as client:
            analysisresults = await client.scan_file_async(file=filetoscan)
            subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
            print()
            print("File has been sent to VirusTotal servers")
            print(pathtofile)
            print()
            print("Waiting for VirusTotal to respond...")
            print()
            processedanalysis = await client.wait_for_analysis_completion(analysisresults)
            subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
            print()
            print(f"File {pathtofile} has been analized and processed by VirusTotal")
            print()
            print("Here are the results:")
            print(processedanalysis.stats)
            print()
            print("Id of the scan:")
            print(processedanalysis.id)

asyncio.run(main())

print()
print("Thank you for using File Scanner by J1D1!")
print()
print("Please refer to https://github.com/J1D1-7398/File-Scanner-AntiVirus for more information.")
print()