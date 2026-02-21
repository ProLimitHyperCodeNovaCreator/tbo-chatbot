import numpy as np

PRICE = {"low": 0, "mid": 1, "high": 2}
DIST = {"near": 0, "mid": 1, "far": 2}
RATING = {"low": 0, "mid": 1, "high": 2}

def featurize(opt):
    return np.array([
        PRICE.get(opt["price_bucket"], 1),
        DIST.get(opt["distance_bucket"], 1),
        RATING.get(opt["rating_bucket"], 1),
        1 if opt["refundable"] else 0,
        hash(opt["supplier_id"]) % 1000 / 1000.0
    ])
