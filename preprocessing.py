from collections import defaultdict
from math import log


def calculate_TFIDF_strength(inputFileName, outputFileName):
    entity_w_feature2count = defaultdict()  # mapping between (entity, feature) -> count
    feature2entitycount = defaultdict(int)  # number of distinct entities that match this feature
    feature2entitycountsum = defaultdict(int)  # total occurrence of entities matched this feature

    entity_set = set()
    with open(inputFileName, "r", encoding="utf8") as fin:
        print("[INFO] Read in %s" % inputFileName)
        cnt = 0
        for line in fin:
            if cnt % 1000000 == 0 and cnt != 0:
                print("Processed %s of lines" % cnt)
            cnt += 1
            seg = line.strip().split("\t")

            if len(seg) == 3:
                entity = seg[0]
                feature = seg[1]
                count = int(seg[2])

            entity_set.add(entity)
            entity_w_feature2count[(entity, feature)] = count
            feature2entitycount[feature] += 1
            feature2entitycountsum[feature] += count

    ## Please refer to eq. (1) in http://mickeystroller.github.io/resources/ECMLPKDD2017.pdf
    print("[INFO] Start calculating TF-IDF strength")
    E = len(entity_set)  # vocabulary size
    with open(outputFileName, "w", encoding="utf8") as fout:
        cnt = 0
        for key in entity_w_feature2count.keys():
            cnt += 1
            if cnt % 1000000 == 0:
                print("Processed %s of (entity, feature) pairs" % cnt)
            X_e_c = entity_w_feature2count[key]
            feature = key[1]
            f_e_c_count = log(1 + X_e_c) * (log(E) - log(feature2entitycount[feature]))
            f_e_c_strength = log(1 + X_e_c) * (log(E) - log(feature2entitycountsum[feature]))  # the one used in SetExpan

            fout.write(key[0] + "\t" + key[1] + "\t" + str(f_e_c_count) + "\t" + str(f_e_c_strength) + "\n")


def main():
    # data_folder = "../../SetExpan_data/weblist/"
    data_folder = "./dataset/weblist/"

    data_file_name = data_folder + "data.txt"
    entity_feature_count_file = data_folder + "EntityFeatureCount.txt"

    entity_feature_mapping = {}
    with open(data_file_name, 'r', encoding="utf8") as fin:
        for line in fin:

            seg = line.strip().split('\t\t')
            if len(seg) == 2:
                feature = seg[0]
                entities = seg[1].split('\t')

                for entity in entities:
                    if entity in entity_feature_mapping:
                        entity_feature_mapping[entity].append(feature)
                    else:
                        entity_feature_mapping[entity] = [feature]

    fin.close()

    with open(entity_feature_count_file, 'w', encoding="utf8") as fout:
        for entity in entity_feature_mapping:
            feature_list = entity_feature_mapping[entity]

            for feature in feature_list:
                fout.write(entity + '\t' + feature + '\t' + '1' + '\n')

    fout.close()

    tfidf_strength_file = data_folder + "EntityFeature2TFIDFStrength.txt"
    calculate_TFIDF_strength(entity_feature_count_file, tfidf_strength_file)


if __name__ == "__main__":
    main()
