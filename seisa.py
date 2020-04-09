import util

entity2entity_sim = {}


def get_jaccard_sim(entity1, entity2, entity2features):
    if tuple(sorted((entity1, entity2))) in entity2entity_sim:
        sim = entity2entity_sim[tuple(sorted((entity1, entity2)))]
        # print("Reused sim: " + entity1 + ', ' + entity2)

    else:

        entity1_features = set(entity2features[entity1])
        entity2_features = set(entity2features[entity2])

        sim = len(entity1_features.intersection(entity2_features)) / len(entity1_features.union(entity2_features))

        # (key1, key2) and (key2, key1) are same in this context, so storing it sorted to access later in both way
        entity2entity_sim[tuple(sorted((entity1, entity2)))] = sim
        # print("Calculated sim: " + entity1 + ', ' + entity2)

    return sim


def get_rel_score(candidate_entity, expanded_entities, entity2features):
    total_sim_score = 0
    for expanded_entity in expanded_entities:
        total_sim_score += get_jaccard_sim(candidate_entity, expanded_entity, entity2features)

    return total_sim_score / len(expanded_entities)


def get_sorted_key_and_value_based_on_value(entity_score_dict):
    sorted_entities = []
    sorted_scores = []

    for k, v in sorted(entity_score_dict.items(), key=lambda item: item[1], reverse=True):
        sorted_entities.append(k)
        sorted_scores.append(v)

    return sorted_entities, sorted_scores


# expand the set of seedEntities and return entities by order
def static_seisa(seed_entities, entity2features, alpha):
    print("Seed entities in Static Seisa: %s" % seed_entities)

    rel_score_dict = {}
    for entity in entity2features:
        rel_score_dict[entity] = get_rel_score(entity, seed_entities, entity2features)

    sorted_entities, sorted_scores = get_sorted_key_and_value_based_on_value(rel_score_dict)

    k = util.get_otsu_threshold(sorted_scores)

    print("Threshold: %s" % k)

    expanded_entities = sorted_entities[:k]

    print("Expanded entities: after step 0: %s" % expanded_entities)

    iter = 1
    while True:

        sim_score_dict = {}
        combined_score_dict = {}
        for entity in entity2features:
            sim_score_dict[entity] = get_rel_score(entity, expanded_entities, entity2features)
            combined_score_dict[entity] = alpha * rel_score_dict[entity] + (1 - alpha) * sim_score_dict[entity]

        sorted_candidate_entities, sorted_candidate_scores = get_sorted_key_and_value_based_on_value(combined_score_dict)

        candidate_entities = sorted_candidate_entities[:k]

        sorted_expanded_entities = []
        for entity in sorted_candidate_entities:
            if entity in expanded_entities:
                sorted_expanded_entities.append(entity)

        expanded_entities = sorted_expanded_entities

        if set(candidate_entities) != set(expanded_entities):
            new_candidate_entities = [entity for entity in candidate_entities if entity not in expanded_entities]
            expanded_entities.pop()
            expanded_entities.append(new_candidate_entities[0])
            print("Expanded entities: after step %s: %s" % (iter, expanded_entities))

        else:
            break

        iter += 1

    print("Expanded entities after Static Seisa: %s" % expanded_entities)
    return expanded_entities


# expand the set of seedEntities and return entities by order
def dynamic_seisa(seed_entities, entity2features, alpha):
    max_iter = 10

    print("Seed entities in Dynamic Seisa: %s" % seed_entities)

    rel_score_dict = {}
    for entity in entity2features:
        rel_score_dict[entity] = get_rel_score(entity, seed_entities, entity2features)

    sorted_entities, sorted_scores = get_sorted_key_and_value_based_on_value(rel_score_dict)

    k = util.get_otsu_threshold(sorted_scores)

    print("Threshold: %s" % k)

    expanded_entities = sorted_entities[:k]

    print("Expanded entities: after step 0: %s" % expanded_entities)

    iter = 1
    while iter <= max_iter:

        sim_score_dict = {}
        combined_score_dict = {}
        for entity in entity2features:
            sim_score_dict[entity] = get_rel_score(entity, expanded_entities, entity2features)
            combined_score_dict[entity] = alpha * rel_score_dict[entity] + (1 - alpha) * sim_score_dict[entity]

        sorted_candidate_entities, sorted_candidate_scores = get_sorted_key_and_value_based_on_value(combined_score_dict)

        k = util.get_otsu_threshold(sorted_candidate_scores)

        print("Threshold: %s" % k)

        expanded_entities = sorted_candidate_entities[:k]

        print("Expanded entities: after step %s: %s" % (iter, expanded_entities))

        iter += 1

    print("Expanded entities after Dynamic Seisa: %s" % expanded_entities)
    return expanded_entities


# get only those entities that have at least one common list with any of the expanded_entities
def get_refined_entities(expanded_entities, entity2features, feature2entities):

    candidate_features = set()
    for entity in expanded_entities:
        for feature in entity2features[entity]:
            candidate_features.add(feature)

    refined_entities = set()
    for feature in candidate_features:
        for entity in feature2entities[feature]:
            refined_entities.add(entity)

    return refined_entities


# expand the set of seedEntities and return entities by order
def static_seisa_optimized(seed_entities, entity2features, feature2entities, alpha, threshold):

    print("Seed entities in Static Seisa: %s" % seed_entities)

    rel_score_dict = {}

    refined_entities = get_refined_entities(seed_entities, entity2features, feature2entities)

    # print("Refined entites: in step 0: %s" % refined_entities)
    # print("Refined entites length: %s" % len(refined_entities))

    for entity in refined_entities:
        rel_score_dict[entity] = get_rel_score(entity, seed_entities, entity2features)

    sorted_entities, sorted_scores = get_sorted_key_and_value_based_on_value(rel_score_dict)

    # k = util.get_otsu_threshold(sorted_scores)
    #
    # print("Threshold: %s" % k)

    k = threshold

    expanded_entities = sorted_entities[:k]

    print("Expanded entities after step 0: %s" % expanded_entities)

    iter = 1
    while True:
        sim_score_dict = {}
        combined_score_dict = {}

        refined_entities_prev = refined_entities
        refined_entities = get_refined_entities(expanded_entities, entity2features, feature2entities)

        # print("Refined entites: in step %s: %s" % (iter, refined_entities))
        # print("Refined entites length: %s" % len(refined_entities))

        new_refined_entities = refined_entities.difference(refined_entities_prev)

        # print("New Refined entites: in step %s: %s" % (iter, new_refined_entities))
        # print("New Refined entites length: %s" % len(new_refined_entities))

        for entity in new_refined_entities:
            rel_score_dict[entity] = get_rel_score(entity, seed_entities, entity2features)

        for entity in refined_entities:

            sim_score_dict[entity] = get_rel_score(entity, expanded_entities, entity2features)
            combined_score_dict[entity] = alpha * rel_score_dict[entity] + (1 - alpha) * sim_score_dict[entity]

        sorted_candidate_entities, sorted_candidate_scores = get_sorted_key_and_value_based_on_value(combined_score_dict)

        candidate_entities = sorted_candidate_entities[:k]

        sorted_expanded_entities = []
        for entity in sorted_candidate_entities:
            if entity in expanded_entities:
                sorted_expanded_entities.append(entity)

        expanded_entities = sorted_expanded_entities

        if set(candidate_entities) != set(expanded_entities):
            new_candidate_entities = [entity for entity in candidate_entities if entity not in expanded_entities]
            expanded_entities.pop()
            expanded_entities.append(new_candidate_entities[0])
            print("Expanded entities after step %s: %s" % (iter, expanded_entities))

        else:
            break

        iter += 1

    print("Expanded entities length: %s" % len(expanded_entities))
    print("Expanded entities after Static Seisa: %s" % expanded_entities)
    return expanded_entities


# expand the set of seedEntities and return entities by order
def dynamic_seisa_optimized(seed_entities, entity2features, feature2entities, alpha, threshold):

    max_iter = 10

    print("Seed entities in Dynamic Seisa: %s" % seed_entities)

    rel_score_dict = {}

    refined_entities = get_refined_entities(seed_entities, entity2features, feature2entities)

    # print("Refined entites: in step 0: %s" % refined_entities)
    # print("Refined entites length: %s" % len(refined_entities))

    for entity in refined_entities:
        rel_score_dict[entity] = get_rel_score(entity, seed_entities, entity2features)

    sorted_entities, sorted_scores = get_sorted_key_and_value_based_on_value(rel_score_dict)

    k = util.get_otsu_threshold(sorted_scores)

    print("Threshold: %s" % k)

    if k > threshold:
        k = threshold

    expanded_entities = sorted_entities[:k]

    print("Expanded entities after step 0: %s" % expanded_entities)

    iter = 1
    while iter <= max_iter:

        sim_score_dict = {}
        combined_score_dict = {}

        refined_entities_prev = refined_entities
        refined_entities = get_refined_entities(expanded_entities, entity2features, feature2entities)

        # print("Refined entites: in step %s: %s" % (iter, refined_entities))
        # print("Refined entites length: %s" % len(refined_entities))

        new_refined_entities = refined_entities.difference(refined_entities_prev)

        # print("New Refined entites: in step %s: %s" % (iter, new_refined_entities))
        # print("New Refined entites length: %s" % len(new_refined_entities))

        for entity in new_refined_entities:
            rel_score_dict[entity] = get_rel_score(entity, seed_entities, entity2features)

        for entity in refined_entities:

            sim_score_dict[entity] = get_rel_score(entity, expanded_entities, entity2features)
            combined_score_dict[entity] = alpha * rel_score_dict[entity] + (1 - alpha) * sim_score_dict[entity]

        sorted_candidate_entities, sorted_candidate_scores = get_sorted_key_and_value_based_on_value(combined_score_dict)

        k = util.get_otsu_threshold(sorted_candidate_scores)

        print("Threshold: %s" % k)

        if k > threshold:
            k = threshold

        expanded_entities = sorted_candidate_entities[:k]

        print("Expanded entities after step %s: %s" % (iter, expanded_entities))

        iter += 1

    print("Expanded entities after Dynamic Seisa: %s" % expanded_entities)
    return expanded_entities
