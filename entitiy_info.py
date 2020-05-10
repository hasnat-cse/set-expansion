import util


def main():
    # Loading Corpus
    data_folder = "../../setExpan_data/weblist/"
    # data_folder = "./dataset/weblist/"

    print('loading Entity and feature maps')
    entity2features, feature2entities = util.loadFeaturesAndEntityMap(
        data_folder + 'EntityFeatureCount.txt')  # EnitityFeatureCount.txt

    while True:
        user_input = input("Enter seed entities(separated with comma, q to exit): ")
        if user_input == 'q':
            break

        seed_enitites = user_input.split(',')

        candidate_entity = input("Enter the candidate entity: ")
        print("Feature count for candidate %s: %s" % (candidate_entity, len(entity2features[candidate_entity])))

        for entity in seed_enitites:
            print("Feature count for seed %s: %s" % (entity, len(entity2features[entity])))
            common_features_count = len(entity2features[candidate_entity].intersection(entity2features[entity]))
            print("Common Features count for candidate %s with seed %s: %s" % (candidate_entity, entity, common_features_count))

        common_features = entity2features[seed_enitites[0]]
        for entity in seed_enitites:
            common_features = common_features.intersection(entity2features[entity])

        print("Common Features count between all seeds: %s" % len(common_features))

        common_features = entity2features[candidate_entity]
        for entity in seed_enitites:
            common_features = common_features.intersection(entity2features[entity])

        print("Common Features count for candidate %s with all seeds: %s" % (candidate_entity, len(common_features)))


if __name__ == "__main__":
    main()
