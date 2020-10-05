import numpy as np
import matplotlib.pyplot as plt


def plot_group_bar():
    # seisa = [0.5461, 0.4447, 0.6039, 0.7459, 0.6547, 0.5770, 0.8505, 0.7591]
    # setexpan = [0.6131, 0.6009, 0.8818, 0.7445, 0.7975, 0.6387, 0.9343, 0.7883]
    # query = [1, 2, 3, 4, 5, 6, 7, 8]
    # algorithms = ['M-SEISA', 'SetExpan']
    # pos = np.arange(len(query))
    # bar_width = 0.3
    #
    # plt.bar(pos, seisa, bar_width, color='teal', edgecolor='black')
    # plt.bar(pos + bar_width, setexpan, bar_width, color='firebrick', edgecolor='black')
    # plt.xticks(pos + bar_width / 2, query)
    # plt.xlabel('Query No.', fontsize=10)
    # plt.ylabel('Average R-Precision', fontsize=10)
    # # plt.title('Average R-Precision of queries over concept classes', fontsize=12)
    # plt.legend(algorithms, loc="best", fontsize=8)
    # plt.show()

    # seisa = [0.9075, 0.9424, 0.8734, 0.8712, 0.8912, 0.9897, 0.9498, 0.9061]
    # setexpan = [0.9664, 0.9549, 0.9493, 0.9203, 0.9138, 0.9509, 0.9915, 0.9170]
    # query = [1, 2, 3, 4, 5, 6, 7, 8]
    # algorithms = ['M-SEISA', 'SetExpan']
    # pos = np.arange(len(query))
    # bar_width = 0.3
    #
    # plt.bar(pos, seisa, bar_width, color='teal', edgecolor='black')
    # plt.bar(pos + bar_width, setexpan, bar_width, color='firebrick', edgecolor='black')
    # plt.xticks(pos + bar_width / 2, query)
    # plt.xlabel('Query No.', fontsize=10)
    # plt.ylabel('Mean Average Precision', fontsize=10)
    # plt.legend(algorithms, loc="best", fontsize=8)
    # plt.show()

    # seisa = [1.0, 0.3553, 0.8860, 0.7138, 0.5455]
    # setexpan = [0.9642, 0.5438, 0.8903, 0.8551, 0.6818]
    # classes = ["States of India", "Cities of Alberta", "Public Universities in Ontario", "Prime Ministers of Canada", "Countries of North America"]
    # algorithms = ['M-SEISA', 'SetExpan']
    # pos = np.arange(len(classes))
    # bar_width = 0.3
    #
    # plt.bar(pos, seisa, bar_width, color='teal', edgecolor='black')
    # plt.bar(pos + bar_width, setexpan, bar_width, color='firebrick', edgecolor='black')
    # plt.xticks(pos + bar_width / 2, classes, rotation=10, fontsize=8)
    # plt.xlabel('Concept Class', fontsize=10)
    # plt.ylabel('Average R-Precision', fontsize=10)
    # plt.legend(algorithms, loc="best", fontsize=8)
    # plt.show()

    # seisa = [1.0, 0.7590, 0.9941, 0.9889, 0.8596]
    # setexpan = [0.9989, 0.9142, 0.9592, 0.9434, 0.9264]
    # classes = ["States of India", "Cities of Alberta", "Public Universities in Ontario", "Prime Ministers of Canada",
    #            "Countries of North America"]
    # algorithms = ['M-SEISA', 'SetExpan']
    # pos = np.arange(len(classes))
    # bar_width = 0.3
    #
    # plt.bar(pos, seisa, bar_width, color='teal', edgecolor='black')
    # plt.bar(pos + bar_width, setexpan, bar_width, color='firebrick', edgecolor='black')
    # plt.xticks(pos + bar_width / 2, classes, rotation=10, fontsize=8)
    # plt.xlabel('Concept Class', fontsize=10)
    # plt.ylabel('Mean Average Precision', fontsize=10)
    # plt.legend(algorithms, loc="best", fontsize=8)
    # plt.show()

    seisa = [0.5316, 0.6592, 0.8505, 0.7591]
    setexpan = [0.6986, 0.7269, 0.9343, 0.7883]
    sizes = [2, 3, 4, 5]
    algorithms = ['M-SEISA', 'SetExpan']
    pos = np.arange(len(sizes))
    bar_width = 0.3

    plt.bar(pos, seisa, bar_width, color='teal', edgecolor='black')
    plt.bar(pos + bar_width, setexpan, bar_width, color='firebrick', edgecolor='black')
    plt.xticks(pos + bar_width / 2, sizes)
    plt.xlabel('Seed Size', fontsize=10)
    plt.ylabel('Average R-Precision', fontsize=10)
    plt.legend(algorithms, loc="best", fontsize=8)
    plt.show()


    # seisa = [0.9078, 0.9174, 0.9498, 0.9061]
    # setexpan = [0.9569, 0.9283, 0.9915, 0.9170]
    # sizes = [2, 3, 4, 5]
    # algorithms = ['M-SEISA', 'SetExpan']
    # pos = np.arange(len(sizes))
    # bar_width = 0.3
    #
    # plt.bar(pos, seisa, bar_width, color='teal', edgecolor='black')
    # plt.bar(pos + bar_width, setexpan, bar_width, color='firebrick', edgecolor='black')
    # plt.xticks(pos + bar_width / 2, sizes)
    # plt.xlabel('Seed Size', fontsize=10)
    # plt.ylabel('Mean Average Precision', fontsize=10)
    # plt.legend(algorithms, loc="best", fontsize=8)
    # plt.show()


def main():
    plot_group_bar()
    # plot_multi_line()


if __name__ == "__main__":
    main()
