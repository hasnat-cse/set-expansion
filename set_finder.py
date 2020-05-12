import util
import time


def one_step_lookahead(common_lists_len, entity2count):
    max_guaranteed_pruning = 0
    entity_with_max_guaranteed_pruning = None
    for entity in entity2count:
        pruning_neg = entity2count[entity]
        pruning_pos = common_lists_len - pruning_neg

        # the entity is in all the lists
        if pruning_pos == 0:
            continue

        min_pruning = min(pruning_pos, pruning_neg)

        if min_pruning >= max_guaranteed_pruning:
            max_guaranteed_pruning = min_pruning
            entity_with_max_guaranteed_pruning = entity

    return entity_with_max_guaranteed_pruning, max_guaranteed_pruning


def two_step_lookahead(common_lists, entity2count, entity2features, feature2entities, entity_list):
    max_guaranteed_pruning = 0
    entity_with_max_guaranteed_pruning = None

    for entity in entity2count:
        common_lists_neg = common_lists.difference(entity2features[entity])

        # the entity is in all the lists
        if len(common_lists_neg) == 0:
            continue

        entity2count_neg = {}
        for l in common_lists_neg:
            for e in feature2entities[l]:
                if e not in entity_list:
                    if e in entity2count_neg:
                        entity2count_neg[e] += 1

                    else:
                        entity2count_neg[e] = 1

        common_lists_pos = common_lists.intersection(entity2features[entity])

        positive_entity_list = entity_list[:]
        positive_entity_list.append(entity)

        entity2count_pos = {}
        for l in common_lists_pos:
            for e in feature2entities[l]:
                if e not in positive_entity_list:
                    if e in entity2count_pos:
                        entity2count_pos[e] += 1

                    else:
                        entity2count_pos[e] = 1

        entity_neg, max_pruning_neg = one_step_lookahead(len(common_lists_neg), entity2count_neg)
        entity_pos, max_pruning_pos = one_step_lookahead(len(common_lists_pos), entity2count_pos)

        min_max_pruning = min(max_pruning_neg, max_pruning_pos)

        if min_max_pruning >= max_guaranteed_pruning:
            max_guaranteed_pruning = min_max_pruning
            entity_with_max_guaranteed_pruning = entity

    return entity_with_max_guaranteed_pruning


def find_set(seed_entities, feature2entities, entity2features, lookahead):
    start = time.time()

    common_lists = set()
    for i, entity in enumerate(seed_entities):
        if i == 0:
            common_lists = entity2features[entity]

        else:
            common_lists = common_lists.intersection(entity2features[entity])

    positive_entity_list = seed_entities[:]
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

        if lookahead == 'o':
            selected_entity, max_guaranteed_pruning = one_step_lookahead(len(common_lists), entity2count)
        else:
            selected_entity = two_step_lookahead(common_lists, entity2count, entity2features, feature2entities, positive_entity_list)

        # all entities are in all the lists
        if selected_entity is None:
            break

        question_start_time = time.time()
        entity_exists = input("\nIs %s in your set? Type y or n: " % selected_entity)
        question_end_time = time.time()

        question_time += question_end_time - question_start_time
        question_count += 1

        if entity_exists == 'n':
            common_lists = common_lists.difference(entity2features[selected_entity])
            negative_entity_list.append(selected_entity)

        else:
            common_lists = common_lists.intersection(entity2features[selected_entity])
            positive_entity_list.append(selected_entity)

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

        method = input("\nEnter method ('o' for one-step, 't' for two-step): ")

        find_set(seed_enitites, feature2entities, entity2features, method)


if __name__ == "__main__":
    main()
