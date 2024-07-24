#!/usr/bin/env python3
""" LIFOCache module
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache defines:
      - a caching system that follows LIFO algorithm
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
        discard the last item put in cache (LIFO algorithm) and print DISCARD.
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.order.remove(key)
            self.order.append(key)
            self.cache_data[key] = item

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                discard_key = self.order.pop(-2)
                del self.cache_data[discard_key]
                print("DISCARD: {}".format(discard_key))

    def get(self, key):
        """ Get an item by key
        If key is None or if the key doesn’t exist, return None.
        """
        return self.cache_data.get(key)
