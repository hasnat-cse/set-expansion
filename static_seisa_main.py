import util
import seisa
import time


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

    # print('loading Entity 2 Entity similarity map')
    # entity2entity_sim = util.load_entity2entity_sim_map(
    #     data_folder + 'Entity2EntitySim.txt')  # Entity2EntitySim.txt

    end = time.time()
    print("Finish loading all dataset, using %s seconds" % (end - start))

    while True:

        # Start set expansion
        user_input = input("Enter seed entities (separated with comma, q to exit): ")
        if user_input == 'q':
            break

        seed_enitites = user_input.split(',')

        threshold = int(input("Enter expected output size: "))

        alpha = float(input("Enter value of alpha: "))

        start = time.time()

        # expanded_entities = seisa.static_seisa(seed_enitites, entity2features, alpha)
        expanded_entities = seisa.static_seisa_optimized(seed_enitites, entity2features, feature2entities, alpha, threshold)

        end = time.time()
        print("Total time taken: %s" % (end - start))

        milli_sec = int(round(time.time() * 1000))

        output_file = "./result/static/static_seisa_result_query_" + str(milli_sec) + "_" + str(alpha) + ".txt"
        with open(output_file, "w", encoding="utf8") as fout:
            fout.write("Seed Entities:" + "\n")
            for entity in seed_enitites:
                fout.write(entity + "\n")

            fout.write("\nExpanded Entities:" + "\n")
            # for ele in expanded_entities:
            #     fout.write(ele + "\n")

            fout.write(str(expanded_entities))

            fout.write("\n\nTime Spent: " + str(end - start) + "\n")

            fout.close()


if __name__ == "__main__":
    main()
