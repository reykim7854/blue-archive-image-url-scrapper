# blue-archive-image-url-scrapper
This python script scraps Blue Archive character image URLs from [Blue Archive Wiki](https://bluearchive.wiki/wiki) using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/).
## Requirements
- python 3.6+
- beautifulsoup4
- requests
## How to use
- install the required library from `requirements.txt`
  ```
  pip install -r requirements.txt
  ```
- run scrapper.py
  - Windows
    ```
    py scrapper.py
    ```
  - linux / mac
    ```
    python3 scrapper.py
    ```
- file will be outputed as `characters.json`
  
  example:
  ```json
  {
    "Airi": {
        "avatar": "https://static.miraheze.org/bluearchivewiki/9/96/Airi.png",
        "full_image": "https://static.miraheze.org/bluearchivewiki/4/4b/Airi_full.png"
    },
    ...
    "Yuzu": {
      "avatar": "https://static.miraheze.org/bluearchivewiki/7/71/Yuzu.png",
      "full_image": "https://static.miraheze.org/bluearchivewiki/0/0d/Yuzu_full.png"
    }
  }
  ```