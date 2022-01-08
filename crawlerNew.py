import requests
import json 
import os


# configs

CONFIG_FILE = "config.json"
MAX_ARTICLE_COUNT = 30
FILE_DIR = """./"""
ERROR_TOLERANCE = 4


def saveStatus(key,status,fn=CONFIG_FILE):
    f = open(fn,'r+')
    jsonFile = json.loads(f.read())

    f.close()
    f = open(fn,'w')
    jsonFile[key]["lastArticleIndex"] = status["lastArticleIndex"]
    jsonFile[key]["pageNo"] = status["pageNo"]
    json.dump(jsonFile,f)
    f.close()



def getStatus(key,fn=CONFIG_FILE): #key == query string , returns the next pageNo to resume the fetching process
    files = os.listdir(FILE_DIR)
    pageNo = 1
    lastArticleIndex = 0
    
    if fn not in files:
        #create new file
        with open(fn, 'w') as file_object:  #open the file in write mode
            file_object.write("{}")

    
    #read config file
    with open(fn,'r') as file_object:
        confObj = json.loads(file_object.read())
    #check if the query keyword status is present or not
    #if key is presend
        if key in confObj:
            pageNo = confObj[key]["pageNo"]
            lastArticleIndex = confObj[key]["lastArticleIndex"]
        #else create new key value pair with the initial value 1
        else:
            pageNo = 1
            confObj[key] = {"pageNo" : pageNo ,"lastArticleIndex" : lastArticleIndex}
            #update config file
            with open(fn, 'w') as file_object:  
              json.dump(confObj,file_object)
        return confObj[key]


def getJson(fn):
    files = os.listdir(FILE_DIR)
    jsonObj = []
    if fn in files:
      with open(fn,'r') as f:
         jsonObj = json.loads(f.read())
    return jsonObj


def scrapAnnarpurnaPost(pageNo,query="प्रचण्"):
    url = "https://bg.annapurnapost.com/api/search"
    
    #transforming pageNo into relevant form for the query processing
    
    
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



def runScraper(query="प्रचण्",maxArticleCount=MAX_ARTICLE_COUNT):
    status = getStatus(query,fn="config.json") #return the last number of article and corresponding page if the same script has been run already
    lastArticleIndex, pageCounter = status["lastArticleIndex"], status["pageNo"]
    scraptedData = getJson(fn=query+".json")
    errorTolerance = ERROR_TOLERANCE # re-fetch data if error occrured for errorTolerance time
   
    while True:
        print(pageCounter)

        #terminate scraping if max article count reached

        if(lastArticleIndex >= maxArticleCount):
            break;

        # request 
        response = scrapAnnarpurnaPost(pageCounter,query)

        if response.status_code == 200:
            pageCounter += 1
        else:
           errorTolerance -= 1
           if errorTolerance == 0:
              break;
           continue;
        
        # converting text into json/python dic object
        jsonObj = json.loads(response.text)["data"]["items"]

        #--appending response into json file-- 
        for article in jsonObj:
          scraptedData.append(article)
          lastArticleIndex += 1
          

        #store status of the scraper
        status = {"pageNo":pageCounter,"lastArticleIndex":lastArticleIndex}
        print(status)
        saveStatus(query,status)

       


    #saving result
    with open(query+".json", 'w') as file_object:  #open the file in write mode
         json.dump(scraptedData, file_object)





if __name__ == "__main__":
    runScraper()