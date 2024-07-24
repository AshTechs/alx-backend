#!/usr/bin/env python3
""" LFUCache module """

from collections import defaultdict, OrderedDict
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFUCache class defines cache with Least Frequently Used eviction policy
    and Least Recently Used tie-breaking.
    """
    def __init__(self):
        """ Initialize LFUCache """
        super().__init__()
        self.freq = defaultdict(int)  # Frequency of access
        self.items = defaultdict(OrderedDict)  # Items at each frequency
        self.min_freq = 0  # Minimum frequency in the cache

    def put(self, key, item):
        """ Add an item to the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq[key] += 1
            old_freq = self.freq[key] - 1
            del self.items[old_freq][key]
            if not self.items[old_freq] and old_freq == self.min_freq:
                self.min_freq += 1
            self.items[self.freq[key]][key] = item
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                key_to_remove, _ = (self.items
                                    [self.min_freq].popitem(last=False))
                del self.cache_data[key_to_remove]
                del self.freq[key_to_remove]
                print(f"DISCARD: {key_to_remove}")

            self.cache_data[key] = item
            self.freq[key] = 1
            self.items[1][key] = item
            self.min_freq = 1

    def get(self, key):
        """ Retrieve an item from the cache """
        if key is None or key not in self.cache_data:
            return None

        freq = self.freq[key]
        self.freq[key] += 1
        new_freq = self.freq[key]

        del self.items[freq][key]
        if not self.items[freq] and freq == self.min_freq:
            self.min_freq += 1

        self.items[new_freq][key] = self.cache_data[key]
        return self.cache_data[key]
