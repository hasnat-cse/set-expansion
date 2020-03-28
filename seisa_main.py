import util
import seisa
import time


def main():
    # Loading Corpus
    # data_folder = "../../setExpan_data/weblist/"
    data_folder = "./dataset/weblist/"

    start = time.time()

    print('loading Entity and feature maps')
    entity2features, feature2entities = util.loadFeaturesAndEntityMap(
        data_folder + 'EntityFeatureCount.txt')  # EnitityFeatureCount.txt

    end = time.time()
    print("Finish loading all dataset, using %s seconds" % (end - start))

    query_count = 0
    while True:

        # entity2features = {
        #     'Canon': ["list1", "list2", "list3"],
        #     'Nikon': ["list1", "list3"],
        #     'Leica': ["list1", "list2", "list3", "list4"],
        #     'VW': ["list4", "list5"],
        #     'BMW': ["list4", "list5"],
        #     'Sony': ["list1", "list2", "list3"]
        # }
        #
        # feature2entities = {
        #     'list1': ["Canon", "Nikon", "Leica", "Sony"],
        #     'list2': ["Canon", "Leica", "Sony"],
        #     'list3': ["Canon", "Nikon", "Leica", "Sony"],
        #     'list4': ["Leica", "VW", "BMW"],
        #     'list5': ["VW", "BMW"],
        # }

        # Start set expansion
        user_input = input("Enter seed entities (separated with comma, q to exit): ")
        if user_input == 'q':
            break

        seed_enitites = user_input.split(',')

        # seed_enitites = ["facebook", "twitter"]
        # seed_enitites = ["Canon", "Leica"]

        query_count += 1

        start = time.time()

        # expanded_entities = seisa.static_seisa(seed_enitites, entity2features, 0.5)
        # expanded_entities = seisa.static_seisa_optimized(seed_enitites, entity2features, feature2entities, 0.9)

        # expanded_entities = seisa.dynamic_seisa(seed_enitites, entity2features, 0.5)
        expanded_entities = seisa.dynamic_seisa_optimized(seed_enitites, entity2features, feature2entities, 0.9)

        end = time.time()
        print("Total time taken: %s" % (end - start))

        output_file = "./result/seisa_result_query_" + str(query_count) + ".txt"
        with open(output_file, "w", encoding="utf8") as fout:
            fout.write("Seed Entities:" + "\n")
            for entity in seed_enitites:
                fout.write(entity + "\n")

            fout.write("\nExpanded Entities:" + "\n")
            for ele in expanded_entities:
                fout.write(ele + "\n")

        fout.close()


if __name__ == "__main__":
    main()
