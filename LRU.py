
from constants import *


class LRU:
    cache_dict = {}
    cache = []
    max_chunks = 0
    def __init__(self,max_chunk_len):
        self.max_chunks = n*1024//max_chunk_len
    
    def get(self,index):
        if index in self.cache:
            self.cache.remove(index)
            self.cache.append(index)
            return self.cache_dict[index]
        else:
            return  ""

    def put(self,index,message):
        if index not in self.cache_dict and self.max_chunks != 0:
            if len(self.cache) >= self.max_chunks:
                self.cache_dict.pop(self.cache[0])
                self.cache.pop(0)
            self.cache.append(index)
            self.cache_dict[index] = message
            
    

            