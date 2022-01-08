import requests
import os
import json

def scrapAnnarpurnaPost(pageNo,query="प्रचण्"):
    url = "https://bg.annapurnapost.com/api/search"
    
    
    querystring = {"title":query,"page":str(pageNo)}

    payload = ""
    headers = {
        "authority": "bg.annapurnapost.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "sec-ch-ua": "' Not A;Brand';v='99', 'Chromium';v='96', 'Microsoft Edge';v='96'",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
        "sec-ch-ua-platform": "\"Windows\"",
        "accept": "*/*",
        "origin": "https://annapurnapost.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://annapurnapost.com/",
        "accept-language": "en-US,en;q=0.9"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    return response


def runScraper(fileName = "dataSet.json",maxPage=30):
    pageCounter = 1;
    result =[]
    while pageCounter < maxPage:
        response = scrapAnnarpurnaPost(pageCounter)

		# display status 
        status = "success" if response.status_code == 200 else "error" 
        print("page"+str(pageCounter)+ ": status = "+status)

        # if error re-download the page 
        if response.status_code == 200:
            pageCounter+=1 


        # converting text into json/python dic object
        jsonObj = json.loads(response.text)
		
		#--appending response into json file--        
        result.append(jsonObj)
     
    #saving result
    with open(fileName, 'w') as file_object:  #open the file in write mode
         json.dump(result, file_object)
    

if __name__ == "__main__":
	runScraper()