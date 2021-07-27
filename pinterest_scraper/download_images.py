import argparse
import os
import typing

from tqdm import tqdm

from pinterest_scraper.pin_scraper import PinterestScraper, ImageGetter
from pinterest_scraper.image_downloader import download_multiple_images


def get_pin_urls(url: str, max_scrolls: int, max_no_scrolls: int, headless: bool, **kwargs):
    pp = PinterestScraper(headless, **kwargs)

    with tqdm(total=max_scrolls, desc="Get pin urls") as pbar:
        pin_urls = pp.get_pin_urls(
            url, max_scrolls, max_not_scroll_waits=max_no_scrolls,
            scroll_callback=lambda: pbar.update()
        )
    
    return pin_urls


def get_image_urls(pin_urls: typing.List[str], headless: bool, **kwargs) -> typing.List[str]:
    image_getter = ImageGetter(headless, **kwargs)
    with tqdm(total=len(pin_urls), desc="Get image urls") as pbar:
        image_urls = image_getter.get_image_urls(pin_urls, update_callback=lambda: pbar.update())
    
    return [url for url in image_urls if url is not None]


def download_images(image_urls: typing.List[str], save_folder: str, n_workers: int):
    os.makedirs(save_folder, exist_ok=True)
    
    with tqdm(total=len(image_urls), desc="Download images") as pbar:
        images = download_multiple_images(image_urls, n_workers, update_callback=lambda: pbar.update())
    
    images = [image for image in images if image is not None]

    for i, image in enumerate(images):
        with open(os.path.join(save_folder, f"{i}"), "wb+") as f:
            f.write(image)


def main():
    parser = argparse.ArgumentParser("Download images from Pinterest")
    parser.add_argument("--url", type=str, help="url for page with pins")
    parser.add_argument("--save_folder", type=str, help="path to save the images")
    parser.add_argument("--max_scrolls", default=5, type=int, help="max scrolls of pinterest url")
    parser.add_argument("--max_no_scrolls", default=30, type=int, help="max tries to scroll before quiting")
    parser.add_argument("--download_workers", default=2, type=int, help="number of threads to download images")
    parser.add_argument("--firefox_binary", default=None, type=str, help="path to firefox binary")
    parser.add_argument("--geckodriver", default="geckodriver", type=str, help="path to gecko driver")
    parser.add_argument("--headless", action="store_true", help="whether to use headless mode")
    parser.set_defaults(headless=False)
    args = parser.parse_args()

    selenium_kwargs = {
        "firefox_binary": args.firefox_binary,
        "executable_path": args.geckodriver,
    }

    pin_urls = get_pin_urls(args.url, args.max_scrolls, args.max_no_scrolls, args.headless, **selenium_kwargs)
    image_urls = get_image_urls(pin_urls, args.headless, **selenium_kwargs)
    download_images(image_urls, args.save_folder, args.download_workers)


if __name__ == "__main__":
    main()
