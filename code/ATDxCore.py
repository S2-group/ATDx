from util import *
import numpy as np
import ckwrap as ck


class ATDxCore:
    def __init__(self):
        pass

    @staticmethod
    def calculate_ATDx_sua(dimensions_sua, atdd_tool):
        ATDx = 0

        for dimension in dimensions_sua:
            value = dimensions_sua[dimension] / len(atdd_tool[dimension])
            ATDx = ATDx + value

        # final step of atdx
        ATDx = ATDx / len(atdd_tool)

        return ATDx

    @staticmethod
    def init_dimensions(projects_info, atdd_tool):
        dimensions = {}
        for project in projects_info.get_analysis_projects_info():
            dimensions[project] = {}
            for dimension in atdd_tool:
                dimensions[project][dimension] = 0
        return dimensions

    @staticmethod
    def get_ar_kmeans(norm_t, rule):
        num_clusters = min(len(np.unique(norm_t[rule])), 6)
        ar_kmeans = ck.ckmeans(norm_t[rule], k=(1, num_clusters))
        return ar_kmeans

    def ATDx_core(self, projects_info, ar_tool, atdd_tool, norm_t):
        """
        atdx_core function used to calculate the adtx of a given set of projects

        :param sua: it is a dictionary of a dictionary containing the 3-tuple for each project as first key
        :param ar_tool: it is a dictionary of a dictionary containing the keys of the 3-tuple.
        :param atdd_tool: it is a dictionary containing the dimensions as keys and the array of rules as the content
        :param norm_t: it is an array containing the normalized values of the dataset. If this variable is not added, it means it's the first atdx analysis, otherwise the functions will use this variable to calculate the adtx
        :return it returns a tuple of the dimensions and the atdx given as a dictionary with the projects as key
        """
        # initialization of the atd dimensions. We initialize them all to 0 (it can happen that sua is a dictionary of
        # projects) the same happens with the atdx
        ATDx = {}
        dimensions = self.init_dimensions(projects_info, atdd_tool)

        # We check all of the rules, the norm value and we do the severity calculation
        for rule in ar_tool:
            rule_dimensions = ar_tool[rule]['atd_dimension']
            # Calculation of severeness and storing adding to the dimensions
            ar_kmeans = self.get_ar_kmeans(norm_t, rule)
            dimensions = self.get_dimensions(projects_info, dimensions, rule_dimensions, ar_kmeans)

        # calculation of atdx of a sua
        for projects in projects_info.get_analysis_projects_info():
            ATDx[projects] = self.calculate_ATDx_sua(dimensions[projects], atdd_tool)

        return dimensions, ATDx

    @staticmethod
    def get_dimensions(projects_info, dimensions, rule_dimensions, ar_kmeans):
        """
        get_dimensions function that returns an array with the normalized values

        :param dimensions:
        :param projects_info:
        :param atdd_tool: it is a dictionary containing the amount of rules per dimension. It's keys are the dimensions
        :param rule_dimensions: it contains the key of the current Dimension
        :param ar_kmeans: it's content refers to NORM^t
        """
        for rule_dimension in rule_dimensions:
            for label, project_name in zip(ar_kmeans.labels, projects_info.get_analysis_projects_info()):

                if max(ar_kmeans.labels) - min(ar_kmeans.labels) == 0:
                    break
                else:
                    severity = (5 * ar_kmeans.centers[label] - (min(ar_kmeans.labels))) / (
                            max(ar_kmeans.labels) - min(ar_kmeans.labels))
                    dimensions[project_name][rule_dimension] = dimensions[project_name][rule_dimension] + severity

        return dimensions

    def set_normalized_values(self, projects_info):
        normalized_update = {}
        for rule in projects_info.get_triple():
            gr_level = projects_info.get_triple()[rule]['granularity_level']
            normalized_update[rule] = []

            for project in projects_info.get_analysis_projects_info():
                normalized_update[rule].append(self.norm_calculator(projects_info.get_analysis_projects_info()[project], gr_level, rule))

        return normalized_update

    def execute_ATDx_analysis(self, projects_info):
        atdd = get_dimension_list(projects_info.get_triple())

        norm_t = self.set_normalized_values(projects_info)

        dimensions_t, atdx = self.ATDx_core(projects_info, projects_info.get_triple(), atdd, norm_t)

        projects_info.set_analysis_projects_info(dimensions_t)
        projects_info.set_atdx(atdx)


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





