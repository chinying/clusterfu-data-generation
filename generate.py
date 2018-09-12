import numpy as np
import pyproj
import scipy.spatial.distance

import csv
import random

import itertools

svy21 = pyproj.Proj(init='epsg:3414')  # produces x, y from lng, lat


class PostalGenerator:

    def __init__(self, infile):
        self.locations = None
        with open(infile) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(csvreader)
            self.contents = list(csvreader)
            csvfile.close()

    def receive(self, origins, destinations, randomness=.1, dist=300, k=100):
        near_origin = list(itertools.chain.from_iterable(
            [list(x[0] for x in self.find_nearby(pt['lat'], pt['lng'], dist)) for pt in origins]
        ))
        near_destination = list(itertools.chain.from_iterable(
            [list(x[0] for x in self.find_nearby(pt['lat'], pt['lng'], dist)) for pt in destinations]
        ))
        # TODO: fix 80% * (1 - randomness) of points to be within origins and destinations
        random_size = round(k * randomness)
        non_random_size = k - random_size
        outside = random.choices([l[0] for l in self.contents], k=random_size*2)
        sz = len(outside) // 2

        return {
            'o': random.choices(near_origin, k=non_random_size) + outside[:sz],
            'd': random.choices(near_destination, k=non_random_size) + outside[sz:]
        }

    """
    rtype: (postal, distance(m))
    """
    def find_nearby(self, lat, lng, cluster_distance=300):
        contents = self.contents
        picked_loc = np.array([svy21(lng, lat)])
        # don't regenerate locations if it is already cached
        self.locations = self.locations if self.locations else list(map(lambda x: [x[3], x[4]], contents))
        dist = zip([c[0] for c in contents], scipy.spatial.distance.cdist(self.locations, picked_loc))
        filtered_locs = list(map(lambda y: [y[0], y[1].tolist()[0]],
            filter(lambda x: x[1] < cluster_distance, dist)))
        return filtered_locs

# if __name__ == "__main__":
#     infile = "./postal_code_to_address.csv"

#     pg = PostalGenerator(infile)
#     print(pg.find_nearby(1.333358, 103.847199, 500))
