from util import *
import numpy as np
import ckwrap as ck


class AtdxCore():
    def __init__(self):
        self.atd_x = {}
        self.normalized_updated = {}
        self.project_names = []

    def atdx_core(self, sua, ar_tool, atdd_tool, norm_t):
        """
        atdx_core function used to calculate the adtx of a given set of projects

        :param sua: it is a dictionary of a dictionary containing the 3-tuple for each project as first key
        :param ar_tool: it is a dictionary of a dictionary containing the keys of the 3-tuple.
        :param atdd_tool: it is a dictionary containing the dimensions as keys and the array of rules as the content
        :param norm_t: it is an array containing the normalized values of the dataset. If this variable is not added, it means it's the first atdx analysis, otherwise the functions will use this variable to calculate the adtx
        :return it returns a tuple of the dimensions and the atdx given as a dictionary with the projects as key
        """

        project_name = sua['projectKey']
        self.project_names.append(project_name)
        # initialization of the atd dimensions. We initialize them all to 0 (it can happen that sua is a dictionary of
        # projects) the same happens with the atdx
        dimensions = {}

        for projects in self.project_names:
            dimensions[projects] = {}
            for dimension in atdd_tool:
                self.atd_x[projects] = 0
                dimensions[projects][dimension] = 0

        # We check all of the rules, the norm value and we do the severity calculation
        for rule in ar_tool:
            gr_level = ar_tool[rule]['granularity_level']
            rule_dimensions = ar_tool[rule]['atd_dimension']
            # norma_t update with the new element to add
            if rule in norm_t:
                self.normalized_updated[rule] = norm_t[rule]
            else:
                self.normalized_updated[rule] = []
            self.normalized_updated[rule].append(norm_calculator(sua, gr_level, rule))
            # Calculation of severeness and storing adding to the dimensions
            num_clusters = min(len(np.unique(self.normalized_updated[rule])), 6)
            ar_kmeans = ck.ckmeans(self.normalized_updated[rule], k=(1, num_clusters))
            dimensions, atdd_tool = self.get_dimensions(dimensions, atdd_tool, rule_dimensions, ar_kmeans)
            # number_cluster check (1-5) (better 0-6)

        # calculation of atdx per project in sua
        for names in dimensions:
            for dimension in dimensions[names]:
                value = dimensions[project_name][dimension] / len(atdd_tool[dimension])
            self.atd_x[project_name] = self.atd_x[project_name] + value

        # final step of atdx
        self.atd_x[project_name] = self.atd_x[project_name] / len(atdd_tool)

        return dimensions, self.atd_x, self.normalized_updated

    def get_dimensions(self, dimensions, atdd_tool, rule_dimensions, ar_kmeans):
        """
        get_dimensions function that returns an array with the normalized values

        :param atdd_tool: it is a dictionary containing the amount of rules per dimension. It's keys are the dimensions
        :param rule_dimensions: it contains the key of the current Dimension
        :param ar_kmeans: it's content refers to NORM^t
        """
        for rule_dimension in rule_dimensions:
            for label, project_name in zip(ar_kmeans.labels, self.project_names):
                if max(ar_kmeans.labels) - min(ar_kmeans.labels) == 0:
                    break
                else:
                    severity = (5 * ar_kmeans.centers[label] - (min(ar_kmeans.labels))) / (
                            max(ar_kmeans.labels) - min(ar_kmeans.labels))
                    dimensions[project_name][rule_dimension] = dimensions[project_name][rule_dimension] + severity

        return dimensions, atdd_tool


def norm_calculator(project, gr_level, rule):
    """
    norm_calculator function that returns an array with the normalized values

    :param data_set: dictionary of the
    :param rule: key of the rule referring a rule existing in the dataset
    :param gr_level: key for the granularity level a rule existing in the dataset
    """
    norm = int(project[rule]) / int(project[gr_level])
    return norm


def atdd_from_set_of_rules(set_of_rules):
    """
    atdd_from_set_of_rules function used to get the atdd dictionary with the key as the dimension and the number of rules
    as the content

    :param set_of_rules: it is a dictionary of a dictionary containing the keys of the 3-tuple
    :return it returns a tuple of the dimensions and the atdx given as a dictionary with the projects as key
    """
    atdd = {}
    for rule in set_of_rules:
        for key in set_of_rules[rule]['atd_dimension']:
            if key in atdd:
                atdd[key] = atdd[key] + 1
            else:
                atdd[key] = 1
    return atdd


def get_dimension_list(triple):
    dimensions_with_rules = {}

    for rule in triple:
        dimensions_list = rule['dimensions']
        rule_name = rule['rule']

        for dimension_element in dimensions_list:
            if dimension_element not in dimensions_with_rules:
                dimensions_with_rules[dimension_element] = [rule_name]
                continue
            dimensions_with_rules[dimension_element].append(rule_name)

    return dimensions_with_rules


if __name__ == "__main__":
    rules_triple = read_json('../data/ar_rules.json')
    ar_rules = split_dimensions(rules_triple['rules'])
    project_dataset = read_json('../data/ATDx_input.json')

    atdd = get_dimension_list(rules_triple['triple'])
    print(atdd)

    norm_t = {}
    atdx_calculator = AtdxCore()

    for sua in project_dataset:
        dimensions_t, atdx, norm_t = atdx_calculator.atdx_core(project_dataset[sua], ar_rules, atdd, norm_t)
    dimensions_t, atdx, norm_t = atdx_calculator.atdx_core(project_dataset['apache_sling-org-apache-sling-commons-html'], ar_rules, atdd, norm_t)

    save_dict_as_json('../data/test_atdx_dataset_output.json', atdx)
    save_dict_as_json('../data/test_dimensions_dataset_output.json', dimensions_t)
    save_dict_as_json('../data/test_normalized.json', norm_t)

    # print(atdx)

    # dimensions_t, atdx, norm = atdx_core(project_dataset, ar_rules, atdd, norm)
    # print(dimensions_t)
    # atdx_core print(atdx)
