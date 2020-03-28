'''
__author__: Ellen Wu (modified by Jiaming Shen)
__description__: A bunch of utility functions
__latest_update__: 08/31/2017
__modified_by__: Arif, 03/11/2020
'''
from collections import defaultdict

codec = "utf8"


def loadFeaturesAndEntityMap(filename):
    featuresetByEntity = defaultdict(set)
    entitiesByFeature = defaultdict(set)
    with open(filename, 'r', encoding=codec) as fin:
        for line in fin:
            seg = line.strip('\r\n').split('\t')
            entity = seg[0]
            feature = seg[1]
            featuresetByEntity[entity].add(feature)
            entitiesByFeature[feature].add(entity)
    return featuresetByEntity, entitiesByFeature


def loadWeightByEntityAndFeatureMap(filename, idx=-1):
    ''' Load the (entity, feature) -> strength

    :param filename:
    :param idx: The index column of weight, default is the last column
    :return:
    '''
    weightByEntityAndFeatureMap = {}
    with open(filename, 'r', encoding=codec) as fin:
        for line in fin:
            seg = line.strip('\r\n').split('\t')
            entity = seg[0]
            feature = seg[1]
            weight = float(seg[idx])
            weightByEntityAndFeatureMap[(entity, feature)] = weight
    return weightByEntityAndFeatureMap


# https://en.wikipedia.org/wiki/Otsu%27s_method
# some modifications
def get_otsu_threshold(data_list):
    top = len(data_list)

    sum = 0
    total = 0
    for k, value in enumerate(data_list):
        sum += k * value
        total += k

    wb = 0
    sum_b = 0
    var_max = 0
    threshold = 0
    for k in range(1, top):
        wf = total - wb

        if wb > 0 and wf > 0:
            mf = (sum - sum_b) / wf
            mb = sum_b / wb
            var_between = wb * wf * (mb - mf) * (mb - mf)

            if var_between >= var_max:
                var_max = var_between
                threshold = k + 1   # index k means (k + 1 th element)

        wb += k
        sum_b += k * data_list[k]
    return threshold
