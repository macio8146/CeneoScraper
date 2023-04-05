import requests
from bs4 import BeautifulSoup


def get_smth(ancestor, selector = None, attribute = None, return_list = False):
    try:
        if return_list:
            return [tag.text.strip() for tag in ancestor.select(selector)].copy()
        
        if not selector:
            return ancestor[attribute]
        
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        
        return ancestor.select_one(selector).text.strip()
    
    except AttributeError:
        return None


# product_code = input("Podaj kod produktu: ")
product_code = "91714422"
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
response = requests.get(url)
page_dom = BeautifulSoup(response.text, "html.parser")

opinions = page_dom.select("div.js_product-review")
all_opinions = []
for opinion in opinions:
    print(opinion["data-entry-id"])
    single_opinion = {
        "opinion_id": opinion["data-entry-id"],
        "author": opinion.select_one("span.user-post__author-name").get_text().strip(),
        "recommendation": opinion.select_one("span.user-post__author-recomendation > em").get_text().strip(),
        "score": opinion.select_one("span.user-post__score-count").get_text().strip(),
        "confirmed": opinion.select_one("div.review-pz").get_text().strip(),
        "opinion_date": opinion.select_one("span.user-post__published > time:nth-child(1)")["datetime"].strip(),
        "purchase_date": opinion.select_one("span.user-post__published > time:nth-child(2)")["datetime"].strip(),
        "up_votes": opinion.select_one("span[id^='votes-yes']").get_text().strip(),
        "down_votes": opinion.select_one("span[id^='votes-no']").get_text().strip(),
        "content": opinion.select_one("div.user-post__text").get_text().strip(),
        "cons": [p.text.strip() for p in opinion.select("div.review-feature__col:has(> div.review-feature__title--negatives) > div.review-feature__item")],
        "pros": [p.text.strip() for p in opinion.select("div.review-feature__col:has(> div.review-feature__title--positives) > div.review-feature__item")]
    }

all_opinions.append(single_opinion)
print(all_opinions)
