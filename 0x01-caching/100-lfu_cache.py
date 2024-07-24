#!/usr/bin/env python3
""" LFUCache module """

from collections import defaultdict, OrderedDict
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ Defines a caching system using the Least Frequently Used algorithm.
    with Least Recently Used (LRU) tie-breaking.
    """
    def __init__(self):
        """ Initialize LFUCache """
        super().__init__()
        self.freq = defaultdict(int)
        self.order = OrderedDict()

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq[key] += 1
            self.order.move_to_end(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_freq = min(self.freq.values())
                lfu_candidates = ([k for k, v in self.freq.items()
                                if v == min_freq])
                if lfu_candidates:
                    lru_key = min(lfu_candidates, key=lambda k: self.order[k])
                    del self.cache_data[lru_key]
                    del self.freq[lru_key]
                    self.order.pop(lru_key)
                    print(f"DISCARD: {lru_key}")

            self.cache_data[key] = item
            self.freq[key] = 1
            self.order[key] = None

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None

        self.freq[key] += 1
        self.order.move_to_end(key)
        return self.cache_data[key]
