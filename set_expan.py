'''
__author__: Jiaming Shen, Ellen Wu
__description__: Python Implementation of SetExpan algorithm
__latest_update__: 08/28/2017
__modified_by__: Arif, 03/11/2020
'''
import random
import time

# SAMPLE_RATE is the number of context feature sample rate. 0.8 means 80% of core skipgram features
# will be selected in each ranking pass.
# alpha
SAMPLE_RATE = 0.6
# TOP_K_SG is the maximum number of skipgrams that wil be selected to calculate the entity-entity
# distributional similarity.
# Q
TOP_K_SG = 200
# TOP_K_ENTITY is the number of candidate entities that we considered to calculate mrr score during
# each ranking pass.
TOP_K_ENTITY = 30
# MAX_ITER_SET is the maximum number of expansion iterations
MAX_ITER_SET = 10
# SAMPLES is the ensemble number
# T
SAMPLES = 60
# THRES_MRR is the threshold that determines whether a new entity will be included in the set or not
# T/r
THRES_MRR = SAMPLES * (1.0 / 5.0)
# Skipgrams with score >= (THRESHOLD * nOfSeedEntities) will be retained
THRESHOLD = 0.0
# Skipgrams that can cover [FLAGS_SG_POPULARITY_LOWER, FLAGS_SG_POPULARITY_UPPER] numbers of entities will be
# retained
FLAGS_SG_POPULARITY_LOWER = 3
FLAGS_SG_POPULARITY_UPPER = 30


def getSampledCoreSkipgrams(coreSkipgrams, sample_rate):
    sampledCoreSkipgrams = []
    for sg in coreSkipgrams:
        if random.random() <= sample_rate:
            sampledCoreSkipgrams.append(sg)
    return sampledCoreSkipgrams


def getCombinedWeightByFeatureMap(seedEntities, featuresByEntityMap, weightByEntityAndFeatureMap):
    combinedWeightByFeatureMap = {}
    for seed in seedEntities:
        featuresOfSeed = featuresByEntityMap[seed]
        for sg in featuresOfSeed:
            if sg in combinedWeightByFeatureMap:
                combinedWeightByFeatureMap[sg] += weightByEntityAndFeatureMap[(seed, sg)]
            else:
                combinedWeightByFeatureMap[sg] = weightByEntityAndFeatureMap[(seed, sg)]

    return combinedWeightByFeatureMap


def getFeatureSim(entity, seed, weightByEntityAndFeatureMap, features):
    simWithSeed = [0.0, 0.0]
    for f in features:
        if (entity, f) in weightByEntityAndFeatureMap:
            weight_entity = weightByEntityAndFeatureMap[(entity, f)]
        else:
            weight_entity = 0.0
        if (seed, f) in weightByEntityAndFeatureMap:
            weight_seed = weightByEntityAndFeatureMap[(seed, f)]
        else:
            weight_seed = 0.0
        # Weighted Jaccard similarity
        simWithSeed[0] += min(weight_entity, weight_seed)
        simWithSeed[1] += max(weight_entity, weight_seed)
    if simWithSeed[1] == 0:
        res = 0.0
    else:
        res = simWithSeed[0] * 1.0 / simWithSeed[1]
    return res


# expand the set of seedEntities and return entities by order, excluding seedEntities (original children)
def setExpan(seedEntitiesWithConfidence, negativeSeedEntities, entity2patterns, pattern2entities, entityAndPattern2strength,
             FLAGS_VERBOSE=False, FLAGS_DEBUG=False):
    ''' Note: currently the confidence score of each entity id is actually not used, just ignore it.

    :param seedEntitiesWithConfidence: a list of [entity (int), confidence_score (float)]
    :param negativeSeedEntities: a set of entities (int) that should not be included
    :param entity2patterns:
    :param pattern2entities:
    :param entityAndPattern2strength:

    :return: a list of expanded [entity (excluding the original input entities in seedEntities), confidence_score]
    '''

    seedEntities = [ele[0] for ele in seedEntitiesWithConfidence]
    entity2confidence = {ele[0]: ele[1] for ele in seedEntitiesWithConfidence}

    ## Cache the seedEntities for later use
    cached_seedEntities = set([ele for ele in seedEntities])
    if FLAGS_VERBOSE:
        print('Seed set: %s' % seedEntities)
        print("[INFO] Start SetExpan")

    iters = 0
    while iters < MAX_ITER_SET:
        iters += 1
        prev_seeds = set(seedEntities)
        start = time.time()
        # generate combined weight maps
        combinedWeightBySkipgramMap = getCombinedWeightByFeatureMap(seedEntities, entity2patterns, entityAndPattern2strength)

        nOfSeedEntities = len(seedEntities)

        # pruning skipgrams which can match too few or too many entities
        redundantSkipgrams = set()
        for i in combinedWeightBySkipgramMap:
            size = len(pattern2entities[i])
            if size < FLAGS_SG_POPULARITY_LOWER or size > FLAGS_SG_POPULARITY_UPPER:
                redundantSkipgrams.add(i)

        for sg in redundantSkipgrams:
            del combinedWeightBySkipgramMap[sg]

        # get final core pattern features
        coreSkipgrams = []
        count = 0
        for sg in sorted(combinedWeightBySkipgramMap, key=combinedWeightBySkipgramMap.__getitem__, reverse=True):
            if count >= TOP_K_SG:
                break
            count += 1
            if combinedWeightBySkipgramMap[sg] * 1.0 / nOfSeedEntities > THRESHOLD:
                coreSkipgrams.append(sg)

        end = time.time()
        print("[INFO] Finish context feature selection using time %s seconds" % (end - start))

        # terminate condition
        if len(coreSkipgrams) == 0:
            print("[INFO] Terminated due to no additional quality skipgrams at iteration %s" % iters)
            break

        # rank ensemble
        all_start = time.time()
        entity2mrr = {}
        if FLAGS_DEBUG:
            print("Start ranking ensemble at iteration %s:" % iters, end=" ")
        for i in range(SAMPLES):
            sampledCoreSkipgrams = getSampledCoreSkipgrams(coreSkipgrams, SAMPLE_RATE)
            combinedSgSimByCandidateEntity = {}
            candidates = set()

            for sg in sampledCoreSkipgrams:
                candidates = candidates.union(pattern2entities[sg])

            for entity in candidates:

                combinedSgSimByCandidateEntity[entity] = 0.0
                for seed in seedEntities:
                    combinedSgSimByCandidateEntity[entity] += getFeatureSim(entity, seed, entityAndPattern2strength,
                                                                      sampledCoreSkipgrams)

            # get top k candidates
            count = 0
            for entity in sorted(combinedSgSimByCandidateEntity, key=combinedSgSimByCandidateEntity.__getitem__, reverse=True):
                if count >= TOP_K_ENTITY:
                    break

                if entity not in seedEntities:
                    count += 1
                    if entity in entity2mrr:
                        entity2mrr[entity] += 1.0 / count
                    else:
                        entity2mrr[entity] = 1.0 / count
        all_end = time.time()

        if FLAGS_DEBUG:
            print("End ranking ensemble at iteration %s" % iters)
            print("Totally using time %s seconds" % (all_end - all_start))

        # Select entities to be added into the set
        entity_incremental = []
        max_mrr = max(entity2mrr.values())
        for ele in sorted(entity2mrr.items(), key=lambda x: -x[1]):
            entity = ele[0]
            mrr_score = ele[1]
            if mrr_score < THRES_MRR:
                break
            if FLAGS_DEBUG:
                print("Add entity %s with normalized mrr score %s" % (entity, mrr_score / max_mrr))

            ## exclude negative seed entities, and calculate confidence score (currently not used)
            if entity not in negativeSeedEntities:
                confidence_score = 0.0
                entity_incremental.append(entity)
                entity2confidence[entity] = confidence_score

        seedEntities.extend(entity_incremental)

        # if nothing been added, stop
        if len(set(seedEntities).difference(prev_seeds)) == 0 and len(prev_seeds.difference(set(seedEntities))) == 0:
            print("[INFO] Terminated due to no additional quality entities at iteration %s" % iters)
            break

    if FLAGS_VERBOSE:
        print('[INFO] Finish SetExpan for one set')
        print('Expanded Set Length: %s' % len(seedEntities))
        print('Expanded set: %s' % seedEntities)

    expanded = []
    for entity in seedEntities:
        if entity not in cached_seedEntities:
            expanded.append([entity, entity2confidence[entity]])

    return expanded


# Denoised Feature #
Q = 200
# Number of Ensemble
T = 60
# Ensemble rate
ALPHA = 0.6
# Average Rank
r = 5


# expand the set of seedEntities and return entities by order, excluding seedEntities (original children)
def setExpan_according_to_paper(seedEntitiesWithConfidence, entity2patterns, pattern2entities, entityAndPattern2strength, output_size):
    ''' Note: currently the confidence score of each entity id is actually not used, just ignore it.

    :param seedEntitiesWithConfidence: a list of [entity (int), confidence_score (float)]
    :param entity2patterns:
    :param pattern2entities:
    :param entityAndPattern2strength:
    :param output_size:

    :return: a list of expanded [entity (excluding the original input entities in seedEntities), confidence_score]
    '''

    seedEntities = [ele[0] for ele in seedEntitiesWithConfidence]
    entity2confidence = {ele[0]: ele[1] for ele in seedEntitiesWithConfidence}

    ## Cache the seedEntities for later use
    cached_seedEntities = set([ele for ele in seedEntities])

    print('Seed set: %s' % seedEntities)

    iters = 0
    while len(seedEntities) <= output_size:
        iters += 1
        start = time.time()
        # generate combined weight maps
        combinedWeightBySkipgramMap = getCombinedWeightByFeatureMap(seedEntities, entity2patterns, entityAndPattern2strength)

        # get final core pattern features
        coreSkipgrams = []
        count = 0
        for sg in sorted(combinedWeightBySkipgramMap, key=combinedWeightBySkipgramMap.__getitem__, reverse=True):
            if count >= Q:
                break

            count += 1
            coreSkipgrams.append(sg)

        end = time.time()
        print("Finish context feature selection at iteration %s using time %s seconds" % (iters, (end - start)))

        # rank ensemble
        all_start = time.time()
        entity2mrr = {}

        for i in range(T):
            sampledCoreSkipgrams = getSampledCoreSkipgrams(coreSkipgrams, ALPHA)

            combinedSgSimByCandidateEntity = {}
            candidates = set()

            for sg in sampledCoreSkipgrams:
                candidates = candidates.union(pattern2entities[sg])

            for entity in candidates:

                combinedSgSimByCandidateEntity[entity] = 0.0
                for seed in seedEntities:
                    combinedSgSimByCandidateEntity[entity] += getFeatureSim(entity, seed, entityAndPattern2strength,
                                                                      sampledCoreSkipgrams)

            count = 0
            for entity in sorted(combinedSgSimByCandidateEntity, key=combinedSgSimByCandidateEntity.__getitem__, reverse=True):
                if entity not in seedEntities:
                    count += 1
                    if entity in entity2mrr:
                        entity2mrr[entity] += 1.0 / count
                    else:
                        entity2mrr[entity] = 1.0 / count

        all_end = time.time()

        print("End ranking ensemble at iteration %s using time %s seconds" % (iters, (all_end - all_start)))

        # Select entities to be added into the set
        entity_incremental = []
        for ele in sorted(entity2mrr.items(), key=lambda x: -x[1]):
            entity = ele[0]
            mrr_score = ele[1]
            if mrr_score < T/r:
                break

            confidence_score = 0.0
            entity_incremental.append(entity)
            entity2confidence[entity] = confidence_score

        seedEntities.extend(entity_incremental)

        print('Expanded set after iteration %s: %s ' % (iters, seedEntities))

    print('Expanded Set Length: %s' % len(seedEntities))
    print('Expanded set: %s' % seedEntities)

    expanded = []
    for entity in seedEntities:
        if entity not in cached_seedEntities:
            expanded.append([entity, entity2confidence[entity]])

    return expanded
