import util


def main():
    # Loading Corpus
    data_folder = "../../setExpan_data/weblist/"
    # data_folder = "./dataset/weblist/"

    print('loading Entity and feature maps')
    entity2features, feature2entities = util.loadFeaturesAndEntityMap(
        data_folder + 'EntityFeatureCount.txt')  # EnitityFeatureCount.txt

    truth_lists = [
        ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
         "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
         "Meghalaya", "Mizoram", "Nagaland", "Orissa", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Tripura",
         "Uttar Pradesh", "Uttarakhand", "West Bengal", "Jammu and Kashmir"],

        ["Airdrie", "Beaumont", "Brooks", "Calgary", "Camrose", "Chestermere", "Cold Lake", "Edmonton",
         "Fort Saskatchewan", "Grande Prairie", "Lacombe", "Leduc", "Lethbridge", "Lloydminster", "Medicine Hat",
         "Red Deer", "Spruce Grove", "St. Albert", "Wetaskiwin"],

        ["Algoma University", "Brock University", "Carleton University", "Lakehead University", "Laurentian University",
         "McMaster University", "Nipissing University", "Queen\\'s University", "Ryerson University",
         "Trent University", "University of Guelph", "University of Ottawa", "University of Toronto",
         "University of Waterloo", "University of Western Ontario", "University of Windsor",
         "Wilfrid Laurier University", "York University", "OCAD University"],

        ["Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominica",
         "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico",
         "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia", "Trinidad and Tobago", "United States"],

        ["John A. Macdonald", "Alexander Mackenzie", "John Abbott", "John Thompson", "Mackenzie Bowell",
         "Charles Tupper", "Wilfrid Laurier", "Robert Borden", "Arthur Meighen", "William Lyon Mackenzie King",
         "R. B. Bennett", "Louis St. Laurent", "John Diefenbaker", "Lester B. Pearson", "Pierre Trudeau", "Joe Clark",
         "John Turner", "Brian Mulroney", "Kim Campbell", "Jean Chrétien", "Paul Martin", "Stephen Harper",
         "Justin Trudeau"]
    ]

    for truth_list in truth_lists:
        entity_feature_count = {}

        unique_features = set()

        for entity in truth_list:
            feature_count = len(entity2features[entity])
            entity_feature_count[entity] = feature_count

            unique_features = unique_features.union(set(entity2features[entity]))


        sorted_entity_feature_count = sorted(entity_feature_count.items(), key=lambda item: item[1], reverse=True)



        print(sorted_entity_feature_count)
        print("\n")
        print("number of lists: %s" % len(unique_features))
        print("\n\n")


if __name__ == "__main__":
    main()
