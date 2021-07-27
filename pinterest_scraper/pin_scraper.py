from os import EX_UNAVAILABLE
import typing
import time
import multiprocessing
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


context = multiprocessing.get_context()


class PinterestScraper:
    def __init__(self, headless: bool, **kwargs):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("permissions.default.image", 2)
        
        options = Options()
        options.headless = headless
        
        self.browser = webdriver.Firefox(
            firefox_profile=profile, options=options,
            **kwargs
        )

        self.base_url = "https://www.pinterest.com"
    
    def get_pin_urls(self, url: str, number_of_scrolls: int, scroll_pause: float = 0.5,
        max_not_scroll_waits: int = 10,
        scroll_callback: typing.Union[typing.Callable[[], None], None] = None) -> typing.List[str]:

        self.browser.get(url)

        last_height = self.browser.execute_script("return document.body.scrollHeight")
        i = 0
        not_scrolls = 0
        while i < number_of_scrolls and not_scrolls < max_not_scroll_waits:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause)

            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height != last_height:
                i += 1
                not_scrolls = 0
                if scroll_callback:
                    scroll_callback()
            else:
                not_scrolls += 1
            
            last_height = new_height

        pins = self.browser.find_elements_by_css_selector('a[href^="/pin/"]')
        return [pin.get_attribute("href") for pin in pins]


class ImageGetter:
    def __init__(self, headless: bool, **kwargs):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("permissions.default.image", 2)

        caps = webdriver.DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "eager"
        
        options = Options()
        options.headless = headless

        self.browser = webdriver.Firefox(
            capabilities=caps, firefox_profile=profile,
            options=options, **kwargs
        )
    
    def get_image_url(self, pin_url: str) -> typing.Union[str, None]:
        self.browser.get(pin_url)
        try:
            image = self.browser.find_element_by_css_selector('div[data-test-id="pin-closeup-image"] img')
            return image.get_attribute("src")
        except:
            return None
    
    def get_image_urls(
        self, pin_urls: typing.List[str],
        update_callback: typing.Union[typing.Callable[[], None], None] = None
    ) -> typing.List[typing.Union[str, None]]:
        result = []
        for pin_url in pin_urls:
            result.append(self.get_image_url(pin_url))
            if update_callback:
                update_callback()
        return result


class ImageGetterWorker(context.Process):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.image_getter = ImageGetter()

    @classmethod
    def register(cls, context):
        context.Process = cls


ImageGetterWorker.register(context)


def get_image_url_mp(args) -> typing.Union[str, None]:
    index, pin_url = args
    cur_process = multiprocessing.current_process()
    return index, cur_process.image_getter.get_image_url(pin_url)


class ParallelImageGetter:
    def __init__(self, n_workers: int = 8, **kwargs):
        self.n_workers = n_workers
        self.kwargs = kwargs
    
    def get_image_urls(self,
        pin_urls: typing.List[str],
        update_callback: typing.Union[typing.Callable[[], None], None] = None
    ) -> typing.List[typing.Union[str, None]]:
        
        result = [None] * len(pin_urls)
        args = zip(range(len(pin_urls)), pin_urls)
        with context.Pool(self.n_workers) as pool:
            for (index, url) in pool.imap_unordered(get_image_url_mp, args):
                result[index] = url
                if update_callback is not None:
                    update_callback()
        
        return result

