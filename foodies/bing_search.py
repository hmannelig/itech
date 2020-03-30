import json
import requests

# function that will register the key for the seach in Bing
def read_bing_key():
 
    bing_api_key = None

    # opening the file bing.key
    # if the files exists the key inside is registered in the variable bing_api_key
    # if not return error
    try:
        with open('bing.key', 'r') as f:
            bing_api_key = f.readline().strip()
    except:
        try:
            with open('../bing.key') as f:
                bing_api_key = f.readline().strip()
        except:
            raise IOError('bing.key file not found')
    
    # if the file does not contain anything return error
    if not bing_api_key:
        raise KeyError('Bing key not found')
    
    return bing_api_key

# function to get the query to search in Bing
def run_query(search_terms):
    # obtain bing key
    bing_key = read_bing_key()
    # set bing URL to make the query
    search_url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'
    # setting the header to be sent for the query
    headers = {'Ocp-Apim-Subscription-Key': bing_key}
    # Parameter of the search
    params = {'q': search_terms, 'textDecorations': True, 'textFormat': 'HTML'}

    # making the query
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    # Obtaining the results of the query
    search_results = response.json()

    # storing the results in a more structured way so it cna be displayed in the website
    results = []
    for result in search_results['webPages']['value']:
        results.append({'title': result['name'], 'link': result['url'], 'summary': result['snippet']})
    
    return results

# Main funciton to make the query
def main():
    
    # Setting the placeholder for the input search
    search_terms = input("Enter your query terms: ")
    # making the query and storing the results
    results = run_query(search_terms)

    # Showing the results
    for result in results:
        print(result['title'])
        print(result['link'])
        print(result['summary'])
        print('===============')

if __name__ == '__main__':
    main()