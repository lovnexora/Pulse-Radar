# importing necessary libraries, pandas for excel in code , requests for API or scrapping data
import pandas as pd 
import requests

def fetch_trending_topics(limit=25):
    ''' fetch most viewed articles from wikipedia '''
    
    try:
        # Keep the URL clean. Let the 'param' dictionary do the work!
        url = 'https://en.wikipedia.org/w/api.php'
        
        param = {
            'action': 'query',
            'format': 'json',
            'list': 'mostviewed',
            'pvmlimit': limit  # Wikipedia uses 'pvmlimit' for page view limits
        }

        # header for polite request to get things done with wikipedia 
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=header, params=param)
        
        if response.status_code == 200:
            data = response.json()
            articles = data['query']['mostviewed']
            topics_data = []

            for item in articles:
                title = item['title'].replace("_", " ")
                
                # Fixed "Main Page" casing to match Wikipedia's exact spelling
                if "Main Page" not in title and "Special:" not in title:
                    topics_data.append({
                        'title': title,
                        'views': item['count'] # Wikipedia uses 'count' instead of 'views' inside the data
                    })

            # Hand back the beautiful, completed data table!
            return pd.DataFrame(topics_data)
            
        else:
            print('Failed to fetch data from Wikipedia API. Status code:', response.status_code)
            return pd.DataFrame() # Returns empty table instead of an empty list [] to keep app.py happy
            
    except Exception as e:
        print(f'An error fetching data from wikipedia occurred: {e}')
        return pd.DataFrame()