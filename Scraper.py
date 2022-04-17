import requests 
import pandas as pd
from bs4 import BeautifulSoup

review_dict = {'name':[], 'date':[], 'rating':[], 'review':[], 'thumbs up':[], 'total thumbs':[]}
i = 0

for page in range(0, 785):
    user_agent = {'User-agent': 'Chrome/95.0.4638.69'}
    url = 'https://www.metacritic.com/game/playstation-4/the-last-of-us-part-ii/user-reviews?page='+str(page)
    response  = requests.get(url, headers = user_agent)

    soup = BeautifulSoup(response.text, 'html.parser')
    for review in soup.find_all('div', class_='review_content'):
        if review.find('div', class_='name') == None:
                       break 
        review_dict['name'].append(review.find('div', class_='name').find('a').text)
        review_dict['date'].append(review.find('div', class_='date').text)
        review_dict['rating'].append(review.find('div', class_='review_grade').find_all('div')[0].text)
        if review.find('span', class_='blurb blurb_expanded'):
            review_dict['review'].append(review.find('span', class_='blurb blurb_expanded').text)
        else:
            if review.find('div', class_='review_body').find('span') == None:
                review_dict['review'].append('#')
                review_dict['thumbs up'].append('#')
                review_dict['total thumbs'].append('#')
                continue
            review_dict['review'].append(review.find('div', class_='review_body').find('span').text)
        review_dict['thumbs up'].append(review.find('span', class_='total_ups').text)
        review_dict['total thumbs'].append(review.find('span', class_='total_thumbs').text)
        print(i)
        i+=1

game_reviews = pd.DataFrame(review_dict)

game_reviews.to_csv('./resources/TheLastofUsPartIIReviews_csv.csv')