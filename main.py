import requests
from bs4 import BeautifulSoup
import json

URL = 'https://emojiguide.org/'


def main():
    page = requests.get(URL)
    # print(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    categorie_list = soup.find('ul', class_='links')
    categories = categorie_list.find_all('a')
    for categorie in categories:
        # print(categorie.prettify())
        categorie_href = categorie['href']
        # print(href)
        get_categorie_page(URL + categorie_href)

        
def get_categorie_page(url):
    categorie_page = requests.get(url)
        
    soup = BeautifulSoup(categorie_page.content, 'html.parser')
    emoji_list = soup.find(id="content")
    emojis = emoji_list.find_all('a')

    for emoji in emojis:
        emoji_href = emoji['href']
        get_emoji(URL + emoji_href)

def get_emoji(url):
    emoji_page = requests.get(url)

    soup = BeautifulSoup(emoji_page.content, 'html.parser')

    emoji_specs = soup.find(id='specs')

    emoji_dict = dict()

    for dt in emoji_specs.find_all('dt'):
        key = dt.text
        value = dt.findNext("dd").string
        if key == "Keywords":
            value = list(map(lambda x: x.text, dt.findNext("dd").find_all('a')))
        emoji_dict[key] = value

    emoji_translation_list = soup.find(id='translations')

    translation_dict = dict()

    for li in emoji_translation_list.find_all('li'):
        lang = li.find('em').text
        translation = li.find('b').text

        translation_dict[lang] = translation


    emoji = Emoji(emoji_dict, translation_dict)


    emoji_json = json.dumps(emoji.to_dict())
    file_name = emoji.name.lower().replace(" ", "_") + '.json'

    print(emoji_dict)

    with open('emojis/' + file_name, 'w') as file:
        file.write(emoji_json)


class Emoji:
    def __init__(self, specs, translations):
        self.name = specs["Emoji name"]
        self.symbol = specs["Symbol"]
        self.codepoint = specs["Codepoint"]
        self.shortcode = specs["Shortcode"]
        self.category = specs["Category"]
        self.keywords = specs["Keywords"]
        self.windows_alt_code = specs["Windows Alt-code"]
        self.decimal_html_entity = specs["Decimal HTML Entity"]
        self.hex_html_entity = specs["Hex HTML Entity"]
        self.utf_16_hex = specs["UTF-16 hex"]
        self.encoded_url = specs["Encoded URL"]
        self.version = specs["Version"]
        self.year = specs["Year"]
        self.translations = translations 

    def to_dict(self):
        return {
            'name': self.name,
            'symbol': self.symbol,
            'codepoint': self.codepoint,
            'shortcode': self.shortcode,
            'category': self.category,
            'keywords': self.keywords,
            'windows_alt_code': self.windows_alt_code,
            'decimal_html_entity': self.decimal_html_entity,
            'hex_html_entity': self.hex_html_entity,
            'utf_16_hex': self.utf_16_hex ,
            'encoded_url': self.encoded_url,
            'version': self.version,
            'year': self.year,
            'translations': self.translations
        }
    
if __name__ == '__main__':
    # main()

    get_emoji('https://emojiguide.org/grinning-face')
