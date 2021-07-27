# pinterest_scraper
Image scraper for Pinterest

***

### Installation

1. Use Python of version 3.6 or greater
2. Clone repository: `git clone https://github.com/evjeny/pinterest_scraper`
3. Install package: `python setup.py install`
4. Download and install Firefox
5. Download `geckordriver`: [link](https://github.com/mozilla/geckodriver/releases)

### Usage

Run: `python -m pinterest_scraper.download_images` and provide arguments:
* `--url`: url to pinterest page with pins
* `--save_folder`: folder to save images, will be created if not exists
* `--max_scrolls`: how many scrolls script should do on `url` page
* `--max_no_scrolls`: how many times script should wait if scrolls doesn't update the page
* `--download_workers`: how many threads would be used while images are being downloaded
* `--firefox_binary`: path to firefox executable
* `--geckodriver`: path to geckodriver
* `--headless`: if provided, then headless browser mode will be used

! Notice: while scraping some of the links might be corrupted, that's why the result number of downloaded images may be less than number of pins on `url` page

Example run command:
```bash
python -m pinterest_scraper.download_images \
    --url "https://www.pinterest.ru/search/pins/?q=programming&rs=typed&term_meta[]=programming%7Ctyped" \
    --save_folder ~/Downloads/programming \
    --max_scrolls 10 \
    --geckodriver ~/Downloads/geckodriver \
    --firefox_binary /usr/bin/firefox \
    --headless
```
