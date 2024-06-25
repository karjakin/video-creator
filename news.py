from newsplease import NewsPlease
import json




article = NewsPlease.from_url('https://www.bbc.co.uk/news/uk-51768274')
print(article.title)

with open('Video 2/article.json', 'w') as f:
    json.dump(article.get_serializable_dict(), f)