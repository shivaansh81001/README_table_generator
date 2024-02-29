'''essential imports'''
import requests as rq
import base64 
import json


'''basic user parameters'''

USERNAME='YOUR_USERNAME'
REPO='YOUR REPO'
PATH_FOLDER='FOLDER_IF_ANY'
PATH_README='README.md'
TOKEN='YOUR_TOKEN'



def check_connection(response):
    '''returns True if the connection has been established successfully'''
    
    if response.status_code==200:
        return True
    print(f"bad request :{response.status_code}")
    return False



def readme(response):
    '''returns the sha for a file/folder'''
    
    return response.json()['sha']



def content_concat(text):
    '''concatinates table heading to the rest of the elementsin markdown'''
    
    pre="|PROBLEM|SOLUTION|\n|-|-|\n"
    post=text
    return pre+post



def main():
    
    '''establishing a connection for the folder that needs to be tablized using github API'''
    
    url_folder=f"https://api.github.com/repos/{USERNAME}/{REPO}/contents/{PATH_FOLDER}"
    headers={'Authorization':f'token {TOKEN}'}  #Authorization Token
    response_1=rq.get(url_folder,headers=headers)   #object dictionary of the current folder/repo
    #print(response.text)
    
    
    
    '''establishing a connection for the readme file for updation'''
    
    url_readme=f"https://api.github.com/repos/{USERNAME}/{REPO}/contents/{PATH_README}"
    response_2=rq.get(url_readme,headers=headers)
    
    
    '''check connection and fetch sha'''
    if check_connection(response_2):
        sha=readme(response_2)
    else:
        print(f"Error fetching readme data {response_2.status_code}")
        exit()
        
        
    '''looping over file names and using string formatting to generate the needed markdown'''
    text=""   
    if check_connection(response_1):
        content=response_1.json()
        for cont in content:
            temp=f"|{cont['name'][:-3]}|[{cont['name']}](kattis_solutions/{cont['name']})|\n"
            text+=temp
    else:
         print(f"Error fetching file name {response_2.status_code}")
         exit()
    
    
    
    '''joining the table headers and content in a single string'''
    new_content=content_concat(text)
    #print(new_content)
    
    
    
    '''preparing data for updation'''
    new_data={
        #commit message
        'message':'updated README', 
        
        #decoding the update content after encoding in base 64 format for readme
        'content':base64.b64encode(new_content.encode()).decode(),  
        
        #assigning back the sha
        'sha':sha
        
        }
    
    
    '''pushing the request using put , converting objects to json'''
    update=rq.put(url_readme,headers=headers,data=json.dumps(new_data))
    
    
    
    '''success message'''
    if check_connection(update):
        print('Successful Update')
    else:
        print(f"Failed to update README {update.status_code}")
    
    
        
main()
    