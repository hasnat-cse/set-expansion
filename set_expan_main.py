import util
import set_expan
import time


def main():
    # Loading Corpus
    # data_folder = "../../SetExpan_data/weblist/"
    data_folder = "./dataset/weblist/"

    start = time.time()

    print('loading Entity and skipgram maps')
    entity2patterns, pattern2entities = util.loadFeaturesAndEntityMap(
        data_folder + 'EntityFeatureCount.txt')  # EntityFeatureCount.txt

    print('loading skipgram strength map')
    entityAndPattern2strength = util.loadWeightByEntityAndFeatureMap(data_folder + 'EntityFeature2TFIDFStrength.txt',
                                                                     idx=-1)  # EntityFeature2TFIDFStrength.txt

    end = time.time()
    print("Finish loading all dataset, using %s seconds" % (end - start))

    query_count = 0
    while True:

        # Start set expansion
        user_input = input("Enter seed entities (separated with comma, q to exit): ")
        if user_input == 'q':
            break

        seed_enitites = user_input.split(',')

        # seed_enitites = ["United States", "China", "Japan", "Germany", "England", "Russia", "India"]
        query_count += 1

        seedEntitiesWithConfidence = [(ele, 0.0) for ele in seed_enitites]

        negativeSeedEntities = set()

        start = time.time()

        expandedEntitiesWithConfidence = set_expan.setExpan(
            seedEntitiesWithConfidence=seedEntitiesWithConfidence,
            negativeSeedEntities=negativeSeedEntities,
            entity2patterns=entity2patterns,
            pattern2entities=pattern2entities,
            entityAndPattern2strength=entityAndPattern2strength,
            FLAGS_VERBOSE=True,
            FLAGS_DEBUG=False,
        )

        end = time.time()
        print("Total time taken: %s" % (end - start))

        output_file = "./result/setexpan_result_query_" + str(query_count) + ".txt"
        with open(output_file, "w", encoding="utf8") as fout:
            fout.write("Seed Entities:" + "\n")
            for entity in seed_enitites:
                fout.write(entity + "\n")

            fout.write("\nExpanded Entities:" + "\n")
            for ele in expandedEntitiesWithConfidence:
                fout.write(ele[0] + "\n")

        fout.close()


if __name__ == "__main__":
    main()
