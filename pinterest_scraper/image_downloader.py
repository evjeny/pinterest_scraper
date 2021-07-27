import typing
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


def download_image(url: str) -> bytes:
    response = requests.get(url, stream=True)
    return response.raw.read()


def download_multiple_images(
    urls: typing.List[str], max_workers: int = 16,
    update_callback: typing.Union[typing.Callable[[], None], None] = None
) -> typing.List[typing.Union[bytes, None]]:

    result = [None] * len(urls)

    with ThreadPoolExecutor(max_workers) as executor:
        future_to_index = {executor.submit(download_image, url): index for index, url in enumerate(urls)}
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            try:
                image_data = future.result()
                result[index] = image_data
            except Exception as e:
                pass
            
            if update_callback is not None:
                update_callback()
    
    return result
