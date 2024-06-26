import requests

# add the url you want to scan below
# no slash at the end, and make sure to add http:// or https://
# e.g: https://example.com

BASE_URL = "" # ********** ADD BASE URL HERE **********

#functions
def find_between( s, first, last ):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def checkResponses(urls):
    response_200 = []
    for i in range(len(urls)):
        r = requests.get(url=urls[i])
        if r.status_code == 200:
            response_200.append(urls[i])
    return response_200
    
def scrape(base_url):
    #sets some needed variables
    endpoint = f"{base_url}/wp-json/"
    scraped_urls = []
    
    #response from website gotten
    r = requests.get(url=endpoint)
    response = r.text.split(",")
    for i in range(len(response)): # finds all urls in wp-json
        current_url = find_between(response[i], '"href":"', '"')
        current_url = current_url.replace('\\', '')
        if current_url == '':
            continue
        scraped_urls.append(current_url)
    
    #print(scraped_urls)
    
    #creates a list of valid urls
    r200 = checkResponses(scraped_urls)
    
    #writes them to file
    name = base_url.replace("https://", "")
    name = name.replace("http://", "")
    with open(f"{name}.txt", "+a") as f:
        for i in range(len(r200)):
            f.write(f"{r200[i]}\n")
    print(f"Program finished. Urls written to {name}.txt")

scrape(BASE_URL)