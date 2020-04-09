def main():
    # truth_list = ["Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Orissa","Punjab","Rajasthan","Sikkim","Tamil Nadu","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Jammu and Kashmir"]
    # truth_list = ["Airdrie","Beaumont","Brooks","Calgary","Camrose","Chestermere","Cold Lake","Edmonton","Fort Saskatchewan","Grande Prairie","Lacombe","Leduc","Lethbridge","Lloydminster","Medicine Hat","Red Deer","Spruce Grove","St. Albert","Wetaskiwin"]
    # truth_list = ["Algoma University","Brock University","Carleton University","Lakehead University","Laurentian University","McMaster University","Nipissing University","Queen\\'s University","Ryerson University","Trent University","University of Guelph","University of Ottawa","University of Toronto","University of Waterloo","University of Western Ontario","University of Windsor","Wilfrid Laurier University","York University","OCAD University"]
    truth_list = ["Antigua and Barbuda","Bahamas","Barbados","Belize","Canada","Costa Rica","Cuba","Dominica","Dominican Republic","El Salvador","Grenada","Guatemala","Haiti","Honduras","Jamaica","Mexico","Nicaragua","Panama","Saint Kitts and Nevis","Saint Lucia","Trinidad and Tobago","United States"]
    # truth_list = ["John A. Macdonald","Alexander Mackenzie","John Abbott","John Thompson","Mackenzie Bowell","Charles Tupper","Wilfrid Laurier","Robert Borden","Arthur Meighen","William Lyon Mackenzie King","R. B. Bennett","Louis St. Laurent","John Diefenbaker","Lester B. Pearson","Pierre Trudeau","Joe Clark","John Turner","Brian Mulroney","Kim Campbell","Jean Chrétien","Paul Martin","Stephen Harper","Justin Trudeau"]

    output_list = ['Canada', 'United States', 'Mexico', 'Cuba', 'Jamaica', 'Brazil', 'France', 'Germany', 'Colombia', 'Argentina', 'Italy', 'Australia', 'Venezuela', 'Russia', 'Chile', 'Spain', 'Sweden', 'Dominican Republic', 'Japan', 'Costa Rica', 'Guatemala', 'Trinidad and Tobago']

    print("Truth set length: %s, output length: %s" % (len(truth_list), len(output_list)))

    common_entities = set(output_list).intersection(set(truth_list))

    incorrect_entities = set(output_list).difference(set(truth_list))
    missing_entities = set(truth_list).difference(set(output_list))

    print("Incorrect entiites: %s" % incorrect_entities)
    print("Missing entiites: %s" % missing_entities)

    r_precision = len(common_entities) / len(truth_list)

    print("R-precision: %s" % r_precision)

    count = 0
    correct_count = 0
    sum_precision = 0
    for entity in output_list:
        count += 1
        if entity in truth_list:
            correct_count += 1
            sum_precision += correct_count / count

    average_precision = sum_precision / correct_count

    print("Average Precision: %s" % average_precision)


if __name__ == "__main__":
    main()
