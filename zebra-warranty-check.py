#!/usr/bin/python3
#copyright Charles Lerant 2021

import requests
import json
import sys
import getopt

#set up the arguments and get the serial number from arguments
def main(argv):
    serialNumber = ''
    try:
        opts, args = getopt.getopt(argv, "hs:f:", ["serial=","file="])
    except getopt.GetoptError:
        print('zebra-warranty-check.py -s <serial number> -f <path to file>')
        sys.exit(2)
    if len(sys.argv) == 1:
        print('zebra-warranty-check.py -s <serial number> -f <path to file>')
    for opt, arg in opts:
        if opt == '-h':
            print('zebra-warranty-check.py -s <serial number> -f <path to file>')
            sys.exit()
        elif opt in ("-s", "--serial"):
                #grab the serial number
                serialNumber = arg
                #print(serialNumber)
                checkSerial(serialNumber)
        elif opt in ("-f", "--file"):
             fileName = arg
             try:
                 serialFile = open(fileName, 'r')
             except:
                 print("Something went wrong. Check the file name and path and try again")
                 sys.exit()
             lines = serialFile.readlines()
             for l in lines:
                print("\nGetting warranty information for serial number: " + l.strip() + "\n***********************************************************************************\n")
                checkSerial(l.strip())
                 
def checkSerial(serialNumber):
    #this part of the code was exported from burp using the extension -Copy As Python-Requests-
#in this case I use -copy request as session object-
#begin burp export we made one slight adjustment with the variable serialNumber to take the place of the test number we used to capture the request
    try:
        session = requests.session()
        burp0_url = "https://supportcommunity.zebra.com:443/s/sfsites/aura?r=3&other.RMAR2_Aura_CaseExtract_CCOM.serialCalloutEVM=1"
        burp0_cookies = {
                        "renderCtx": "%7B%22pageId%22%3A%222a137160-7481-46b1-88da-99792c311563%22%2C%22schema%22%3A%22Published%22%2C%22viewType%22%3A%22Published%22%2C%22brandingSetId%22%3A%220f49f1f3-52b6-4775-b24d-fb3f7027c91b%22%2C%22audienceIds%22%3A%226Au0H000000fxlL%2C6Au0H000000PB9d%2C6Au0H000000blma%22%7D",
                        "guest_uuid_essential_0DMi0000000Chop": "acf2ffda-ab9a-443d-bc37-df8d281b3d80", "CookieConsentPolicy": "0:0",
                        "AMCV_912302BE532950CA0A490D4C%40AdobeOrg": "-1124106680%7CMCIDTS%7C18847%7CMCMID%7C57534213072688422861976192202756969693%7CMCOPTOUT-1628311764s%7CNONE%7CvVersion%7C5.2.0",
                        "AMCVS_912302BE532950CA0A490D4C%40AdobeOrg": "1", "language-detected": "yes",
                        "sfdc-stream": "!iUSYurEJHO9Xhz0rjXpoLThgi0D1t170NFhKRYArYBxoiwH9cO+Z4Qm2AG+pRd+D+X3SbYLJZWAAikE=",
                        "s_ht": "1628304564003", "s_hc": "1%7C0%7C0%7C0%7C0",
                        "s_ptc": "7.40%5E%5E0.00%5E%5E0.00%5E%5E0.00%5E%5E9.71%5E%5E0.00%5E%5E1.79%5E%5E0.00%5E%5E18.91", "s_cc": "true",
                        "pctrk": "669aa4a7-f0d2-4208-a6e1-1381db9255b1", "s_gad": "1"}
        burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
                                     "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
                                     "X-Sfdc-Page-Scope-Id": "0be3fb04-2007-4918-83cc-c77c02cecf84",
                                     "X-Sfdc-Request-Id": "615650000004a01b53",
                                     "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                                     "Origin": "https://supportcommunity.zebra.com",
                                     "Referer": "https://supportcommunity.zebra.com/s/warrantycheck?language=en_US",
                                     "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Sec-Gpc": "1",
                                     "Te": "trailers", "Connection": "close"}
        burp0_data = {
                        "message": "{\"actions\":[{\"id\":\"210;a\",\"descriptor\":\"apex://RMAR2_Aura_CaseExtract_CCOM/ACTION$serialCalloutEVM\",\"callingDescriptor\":\"markup://c:RMAR2_WarrantyCheck\",\"params\":{\"serialNumber\":\""+serialNumber+"\"}}]}",
                        "aura.context": "{\"mode\":\"PROD\",\"fwuid\":\"YeF9IbuOAuhiq8yQ65xJFA\",\"app\":\"siteforce:communityApp\",\"loaded\":{\"APPLICATION@markup://siteforce:communityApp\":\"vWooY-QygCWQvHP4L_Kncg\"},\"dn\":[],\"globals\":{},\"uad\":false}",
                        "aura.pageURI": "/s/warrantycheck?language=en_US", "aura.token": "undefined"}
        r = session.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
                  
    #end burp data
    #dump the response to a json dict check if no serial number is returned if we get a return parse the data and print it out
        warranty_info = json.loads(r.text)
        if warranty_info['actions'][0]['returnValue']['ListOfZEBSerialNumber'] == {}:
            print("Serial Number Was Not Found!!!")
        else:
            for data in warranty_info['actions']:
                print("Warranty Information______")
                for assetNum in range(len(data['returnValue']['ListOfZEBSerialNumber']['Asset'])):
                    print("\n\tAccount Number:" + data['returnValue']['ListOfZEBSerialNumber']['Asset'][assetNum]['OwnerAccountNumber'])
                    print("\tProduct: " + data['returnValue']['ListOfZEBSerialNumber']['Asset'][assetNum]['Product'])
                    print("\tSerialNumber:" + data['returnValue']['ListOfZEBSerialNumber']['Asset'][assetNum]['SerialNumber'])
                    print("\tWarranty Status: " + data['returnValue']['ListOfZEBSerialNumber']['Asset'][assetNum]['Status'])
                    print("\tWarranty Start Date: " + data['returnValue']['ListOfZEBSerialNumber']['Asset'][assetNum]['WarrantyStartDate'])
                    print("\tWarranty End Date: " + data['returnValue']['ListOfZEBSerialNumber']['Asset'][assetNum]['WarrantyEndDate'])
                    if data['returnValue']['ListOfZEBSerialNumber']['Asset'][assetNum]['ListOfServiceDetails'] == {}:
                        print("\nNo Entitlements Found!!!")
                    else:
                        print("\nEntitlements______")
                        for records in data['returnValue']['ListOfZEBSerialNumber']['Asset'][assetNum]['ListOfServiceDetails']['ServiceDetails']:
                            print("\n\tEntitlement Type: " + records['Type_x'])
                            print("\t\tStart Date: " + records['EntitlementStartDate'])
                            print("\t\tEnd Date: " + records['EntitlementEndDate'])
    except getopt.GetoptError:
        print("Something Went Wrong. Oops!!!")
    return
if __name__ == "__main__":
   main(sys.argv[1:])
