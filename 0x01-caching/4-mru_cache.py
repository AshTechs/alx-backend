#!/usr/bin/env python3
""" MRUCache module
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache defines:
      - a caching system that follows MRU algorithm
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add an item in the cache
        If key or item is None, this method should not do anything.
        If the number of items in self.cache_data is higher than BaseCaching.
        discard the most recently used item (MRU algorithm) and print DISCARD.
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.order.remove(key)
            self.cache_data[key] = item
            self.order.append(key)
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                discard_key = self.order.pop(-2)
                del self.cache_data[discard_key]
                print("DISCARD: {}".format(discard_key))

    def get(self, key):
        """ Get an item by key
        If key is None or if the key doesn’t exist in self.cache_data, return None.
        """
        if key is None or key not in self.cache_data:
            return None
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
