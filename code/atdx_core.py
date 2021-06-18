from util import *
import numpy as np
import ckwrap as ck


class AtdxCore:
    def __init__(self, projects_info):
        self.atd_x = {}
        self.normalized_updated = {}
        self.project_names = []
        self.projects_info = projects_info

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

        # initialization of the atd dimensions. We initialize them all to 0 (it can happen that sua is a dictionary of
        # projects) the same happens with the atdx
        dimensions = {}
        atd_x = 0
        for project in self.projects_info.get_analysis_projects_info():
            dimensions[project] = {}
            for dimension in atdd_tool:
                dimensions[project][dimension] = 0

        # We check all of the rules, the norm value and we do the severity calculation
        for rule in ar_tool:
            rule_dimensions = ar_tool[rule]['atd_dimension']
            # Calculation of severeness and storing adding to the dimensions
            num_clusters = min(len(np.unique(norm_t[rule])), 6)
            ar_kmeans = ck.ckmeans(norm_t[rule], k=(1, num_clusters))
            dimensions = self.get_dimensions(dimensions, rule_dimensions, ar_kmeans)

        # calculation of atdx per project in sua
        for names in dimensions:
            for dimension in dimensions[names]:
                value = dimensions[project_name][dimension] / len(atdd_tool[dimension])
                atd_x = atd_x + value

        # final step of atdx
        atd_x = atd_x / len(atdd_tool)

        return dimensions, atd_x

    def get_dimensions(self, dimensions, rule_dimensions, ar_kmeans):
        """
        get_dimensions function that returns an array with the normalized values

        :param atdd_tool: it is a dictionary containing the amount of rules per dimension. It's keys are the dimensions
        :param rule_dimensions: it contains the key of the current Dimension
        :param ar_kmeans: it's content refers to NORM^t
        """
        for rule_dimension in rule_dimensions:
            for label, project_name in zip(ar_kmeans.labels, self.projects_info.get_analysis_projects_info()):

                if max(ar_kmeans.labels) - min(ar_kmeans.labels) == 0:
                    break
                else:
                    severity = (5 * ar_kmeans.centers[label] - (min(ar_kmeans.labels))) / (
                            max(ar_kmeans.labels) - min(ar_kmeans.labels))
                    dimensions[project_name][rule_dimension] = dimensions[project_name][rule_dimension] + severity

        return dimensions

    def set_normalized_values(self, sua):
        normalized_update = {}

        for rule in self.projects_info.get_ar_rules():
            gr_level = self.projects_info.get_ar_rules()[rule]['granularity_level']
            normalized_update[rule] = []
            for project in self.projects_info.get_analysis_projects_info():
                normalized_update[rule].append(self.norm_calculator(self.projects_info.get_analysis_projects_info()[project], gr_level, rule))

            normalized_update[rule].append(self.norm_calculator(sua, gr_level, rule))

        return normalized_update

    def execute_atdx_analysis(self, sua_name):
        atdd = get_dimension_list(self.projects_info.get_triple())

        norm_t = self.set_normalized_values(self.projects_info.get_analysis_projects_info()[sua_name])

        dimensions_t, atdx = self.atdx_core(self.projects_info.get_analysis_projects_info()[sua_name], self.projects_info.get_ar_rules(), atdd, norm_t)

        save_dict_as_json('../data/test_atdx_dataset_output.json', atdx)
        save_dict_as_json('../data/test_dimensions_dataset_output.json', dimensions_t)
        save_dict_as_json('../data/test_normalized.json', norm_t)
        # print(atdx)
        # dimensions_t, atdx, norm = atdx_core(project_dataset, ar_rules, atdd, norm)
        # print(dimensions_t)
        # atdx_core print(atdx)

    @staticmethod
    def norm_calculator(project, gr_level, rule):
        """
        norm_calculator function that returns an array with the normalized values

        :param project: dictionary entry containing the values for the gr_level and rule
        :param rule: key of the rule referring a rule existing in the dataset
        :param gr_level: key for the granularity level a rule existing in the dataset
        """
        norm = int(project[rule]) / int(project[gr_level])
        return norm

    @staticmethod
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



