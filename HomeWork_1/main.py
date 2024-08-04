import functools
import sys
from collections import OrderedDict, defaultdict
import requests


def memory_profiler_decorator(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        mem_before = sum(sys.getsizeof(arg) for arg in args) + sum(sys.getsizeof(val) for val in kwargs.values())
        mem_before += sys.getsizeof(f)
        result = f(*args, **kwargs)
        mem_after = sum(sys.getsizeof(arg) for arg in args) + sum(sys.getsizeof(val) for val in kwargs.values())
        mem_after += sys.getsizeof(result) + sys.getsizeof(f)
        print(f"Memory usage before: {mem_before} bytes")
        print(f"Memory usage after: {mem_after} bytes")
        return result
    return wrapper


def lfu_cache(max_limit=64):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in deco._cache:
                deco._frequency[cache_key] += 1
                # Переміщуємо в кінець для підтримки порядку частоти
                deco._freq_order[deco._frequency[cache_key]].remove(cache_key)
                if not deco._freq_order[deco._frequency[cache_key]]:
                    del deco._freq_order[deco._frequency[cache_key]]
                deco._freq_order[deco._frequency[cache_key] + 1].append(cache_key)
                return deco._cache[cache_key]
            result = f(*args, **kwargs)

            # Видаляємо елементи, якщо досягли ліміту
            if len(deco._cache) >= max_limit:
                # Знаходимо найменшу частоту
                min_freq = min(deco._freq_order.keys())
                # Видаляємо перший елемент з найменшою частотою
                oldest_key = deco._freq_order[min_freq].pop(0)
                if not deco._freq_order[min_freq]:
                    del deco._freq_order[min_freq]
                del deco._cache[oldest_key]
                del deco._frequency[oldest_key]
            # Додаємо новий елемент
            deco._cache[cache_key] = result
            deco._frequency[cache_key] = 1
            deco._freq_order[1].append(cache_key)
            return result
        deco._cache = OrderedDict()
        deco._frequency = defaultdict(int)
        deco._freq_order = defaultdict(list)
        return deco
    return internal


@lfu_cache(max_limit=64)
@memory_profiler_decorator
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content
