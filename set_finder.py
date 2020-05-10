import util
import time


def get_sorted_key_and_value_based_on_value(entity_score_dict, reverse):
    sorted_entities = []
    sorted_scores = []

    for k, v in sorted(entity_score_dict.items(), key=lambda item: item[1], reverse=reverse):
        sorted_entities.append(k)
        sorted_scores.append(v)

    return sorted_entities, sorted_scores


def find_set(seed_entities, feature2entities, entity2features):
    common_lists = set()
    for i, entity in enumerate(seed_entities):
        if i == 0:
            common_lists = entity2features[entity]

        else:
            common_lists = common_lists.intersection(entity2features[entity])

    positive_entity_list = seed_entities
    negative_entity_list = []

    while len(common_lists) > 1:
        print("\nCommon lists among seed entities: %s" % len(common_lists))

        entity2count = {}
        for l in common_lists:
            for e in feature2entities[l]:
                if e not in positive_entity_list:
                    if e in entity2count:
                        entity2count[e] += 1

                    else:
                        entity2count[e] = 1

        entity_pair2score = {}
        for entity1 in entity2count:
            for entity2 in entity2count:
                if entity2 != entity1 and (entity1, entity2) not in entity_pair2score:
                    entity_pair2score[(entity1, entity2)] = (entity2count[entity1] + entity2count[entity2] + 1) / (len(
                        entity2features[entity1].intersection(entity2features[entity2])) + 1)

        if len(entity2count) > 0:
            sorted_entity_pairs, sorted_pair_scores = get_sorted_key_and_value_based_on_value(entity_pair2score, True)

            entity1 = sorted_entity_pairs[0][0]
            entity2 = sorted_entity_pairs[0][1]

        else:
            break

        entity1_exists = input("\nIs %s in your set? Type y or n: " % entity1)
        entity2_exists = input("\nIs %s in your set? Type y or n: " % entity2)

        if entity1_exists == 'n':
            common_lists = common_lists.difference(entity2features[entity1])
            negative_entity_list.append(entity1)

        else:
            common_lists = common_lists.intersection(entity2features[entity1])
            positive_entity_list.append(entity1)

        if entity2_exists == 'n':
            common_lists = common_lists.difference(entity2features[entity2])
            negative_entity_list.append(entity2)

        else:
            common_lists = common_lists.intersection(entity2features[entity2])
            positive_entity_list.append(entity2)

    print("\nOutput set is: ")
    for l in common_lists:
        print(feature2entities[l])

    print("\nPositive Entities considered during searching:\n %s" % positive_entity_list)
    print("\nNegative Entities considered during searching:\n %s" % negative_entity_list)


def find_set_v2(seed_entities, feature2entities, entity2features):
    start = time.time()

    common_lists = set()
    for i, entity in enumerate(seed_entities):
        if i == 0:
            common_lists = entity2features[entity]

        else:
            common_lists = common_lists.intersection(entity2features[entity])

    positive_entity_list = seed_entities
    negative_entity_list = []

    question_count = 0
    question_time = 0
    while len(common_lists) > 1:
        print("\nCommon lists among seed entities: %s" % len(common_lists))

        entity2count = {}
        for l in common_lists:
            for e in feature2entities[l]:
                if e not in positive_entity_list:
                    if e in entity2count:
                        entity2count[e] += 1

                    else:
                        entity2count[e] = 1

        entity2diff = {}
        min_freq = len(common_lists)
        for entity in entity2count:
            diff = abs(entity2count[entity] - (len(common_lists) - entity2count[entity]))
            entity2diff[entity] = diff

            if diff < min_freq:
                min_freq = diff

        # No unexplored entity in the lists or all the lists are identical
        if min_freq == len(common_lists):
            break

        sorted_entities, sorted_diffs = get_sorted_key_and_value_based_on_value(entity2diff, False)

        entity_with_min_diff = sorted_entities[0]

        question_start_time = time.time()
        entity_exists = input("\nIs %s in your set? Type y or n: " % entity_with_min_diff)
        question_end_time = time.time()

        question_time += question_end_time - question_start_time
        question_count += 1

        if entity_exists == 'n':
            common_lists = common_lists.difference(entity2features[entity_with_min_diff])
            negative_entity_list.append(entity_with_min_diff)

        else:
            common_lists = common_lists.intersection(entity2features[entity_with_min_diff])
            positive_entity_list.append(entity_with_min_diff)

    print("\nOutput set: ")
    for l in common_lists:
        print("%s : %s" % (l, feature2entities[l]))

    print("\nNumber of question asked: %s" % question_count)
    print("\nPositive Entities considered during searching:\n %s" % positive_entity_list)
    print("\nNegative Entities considered during searching:\n %s" % negative_entity_list)

    end = time.time()
    total_time = (end - start)

    print("\nProcessing time: %s" % (total_time - question_time))
    print("Total time: %s" % total_time)


def main():
    # Loading Corpus
    data_folder = "../../setExpan_data/weblist/"
    # data_folder = "./dataset/weblist/"

    start = time.time()

    print('loading Entity and feature maps')
    entity2features, feature2entities = util.loadFeaturesAndEntityMap(
        data_folder + 'EntityFeatureCount.txt')  # EnitityFeatureCount.txt

    print("Number of entities: %s" % len(entity2features))
    print("Number of features: %s" % len(feature2entities))

    end = time.time()
    print("Finish loading all dataset, using %s seconds" % (end - start))

    while True:

        # Start set finding
        user_input = input("\nEnter seed entities (separated with comma, q to exit): ")
        if user_input == 'q':
            break

        seed_enitites = user_input.split(',')

        find_set_v2(seed_enitites, feature2entities, entity2features)


if __name__ == "__main__":
    main()
