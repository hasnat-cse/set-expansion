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


def get_context_dependent_weighted_jaccard_sim(entity1, entity2, feature2entities, top_features, feature2rank):
    numerator = 0
    denominator = 0
    for feature in top_features:
        if entity1 in feature2entities[feature]:
            entity1_weight = 1
        else:
            entity1_weight = 0

        if entity2 in feature2entities[feature]:
            entity2_weight = 1
        else:
            entity2_weight = 0

        numerator += min(entity1_weight, entity2_weight)
        denominator += max(entity1_weight, entity2_weight)

    if denominator == 0:
        sim = 0

    else:
        sim = numerator / denominator

    return sim


def get_sorted_key_and_value_based_on_value(entity_score_dict):
    sorted_entities = []
    sorted_scores = []

    for k, v in sorted(entity_score_dict.items(), key=lambda item: item[1], reverse=True):
        sorted_entities.append(k)
        sorted_scores.append(v)

    return sorted_entities, sorted_scores


def get_sim_score(expanded_entities, entity2features, feature2entities):

    feature2score = {}
    for entity in expanded_entities:
        for feature in entity2features[entity]:
            if feature in feature2score:
                feature2score[feature] += 1

            else:
                feature2score[feature] = 1

    for feature in feature2score:
        feature2score[feature] = feature2score[feature] / len(expanded_entities)

    sorted_features, sorted_scores = get_sorted_key_and_value_based_on_value(feature2score)

    top_features = sorted_features[:200]

    entity2related_entities = {}
    for entity in expanded_entities:
        entity2related_entities[entity] = set()
        entity_top_features = entity2features[entity].intersection(top_features)
        for feature in entity_top_features:
            entity2related_entities[entity] = entity2related_entities[entity].union(feature2entities[feature])

    entity2total_sim = {}
    for entity in expanded_entities:
        for related_entity in entity2related_entities[entity]:
            sim = get_context_dependent_weighted_jaccard_sim(related_entity, entity, feature2entities, top_features, feature2score)
            if related_entity in entity2total_sim:
                entity2total_sim[related_entity] += sim

            else:
                entity2total_sim[related_entity] = sim

    entity2sim_score = {}
    for entity in entity2total_sim:
        entity2sim_score[entity] = entity2total_sim[entity] / len(expanded_entities)

    return entity2sim_score


# expand the set of seedEntities and return entities by order
def experiment_algorithm(seed_entities, entity2features, feature2entities, alpha, k):
    global entity2entity_sim
    entity2entity_sim = {}

    print("Seed entities inside algorithm: %s" % seed_entities)

    rel_score_dict = get_sim_score(seed_entities, entity2features, feature2entities)

    print("number of candidate entities: %s" % len(rel_score_dict))

    sorted_entities, sorted_scores = get_sorted_key_and_value_based_on_value(rel_score_dict)

    candidate_entities = sorted_entities[:k]

    expanded_entities = seed_entities

    new_candidate_entities = [entity for entity in candidate_entities if entity not in expanded_entities]
    expanded_entities.append(new_candidate_entities[0])
    print("Expanded entities after step %s: %s" % (0, expanded_entities))

    iter = 1
    while len(expanded_entities) < k:
        sim_score_dict = get_sim_score(expanded_entities, entity2features, feature2entities)
        print("number of candidate entities: %s" % len(sim_score_dict))

        combined_score_dict = {}

        for entity in sim_score_dict:
            if entity in rel_score_dict:
                combined_score_dict[entity] = alpha * rel_score_dict[entity] + (1 - alpha) * sim_score_dict[entity]

            else:
                combined_score_dict[entity] = (1 - alpha) * sim_score_dict[entity]

        sorted_candidate_entities, sorted_candidate_scores = get_sorted_key_and_value_based_on_value(
            combined_score_dict)

        candidate_entities = sorted_candidate_entities[:k]

        sorted_expanded_entities = seed_entities
        for entity in sorted_candidate_entities:
            if entity in expanded_entities and entity not in seed_entities:
                sorted_expanded_entities.append(entity)

        expanded_entities = sorted_expanded_entities

        if set(candidate_entities) != set(expanded_entities):
            new_candidate_entities = [entity for entity in candidate_entities if entity not in expanded_entities]
            expanded_entities.append(new_candidate_entities[0])
            print("Expanded entities after step %s: %s" % (iter, expanded_entities))

        else:
            break

        iter += 1

    print("Expanded entities length: %s" % len(expanded_entities))
    print("Expanded entities after Algorithm: %s" % expanded_entities)
    return expanded_entities
