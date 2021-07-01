from collections import defaultdict
from abc import ABC, abstractmethod

import matplotlib.pylab as plot
import numpy as np


class ReportGen(ABC):

    def __init__(self, max_number_of_projects, max_number_of_classes):
        self.max_number_of_projects = max_number_of_projects
        self.max_number_of_classes = max_number_of_classes
        self.dimensions = None

    def get_categories_pair(self, my_dict):
        """
        Function to get the get the dimensions values in the same order they are stored in the self.dimension variable
        :param my_dict: Is a dictionary containing a projects dimensions as keys and it's values as the content
        :return: Array containing the values of the different dimensions
        """
        category_value = []

        for category in self.dimensions:
            category_value.append(my_dict[category])

        return category_value

    def generate_radarchart(self, project_name, portfolio_info):
        """
        Function to generate the radarchart images, storing them into a default folder where all the radarchart will be stored
        :param portfolio_info: PorfotolioData structure containing all necessary information for the generation of the radarchar
        :param project_name: String containing the name of the project that you want to generate the radarchart for
        """
        ax = plot.subplot(polar="True")

        values = self.get_categories_pair(portfolio_info.get_analysis_projects_info()[project_name])
        N = len(self.dimensions)
        values += values[:1]

        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]

        plot.polar(angles, values)
        plot.fill(angles, values, alpha=0.3)
        plot.xticks(angles[:-1], self.dimensions)
        ax.set_rlabel_position(0)
        ax.set_title([project_name])
        plot.yticks([0, 1, 2, 3, 4, 5], color="grey", size=7)
        plot.savefig('../data/reports/radarchart/' + project_name + '.jpg')
        plot.close()

    def cluster_issues_per_class(self, portfolio_info):
        """
        This function will cluster the issues per class which are stored in the object portfolio_info
        :param portfolio_info: PorfotolioData structure containing all necessary information for the generation of the radarchar
        :return:
        """
        issues = portfolio_info.get_issues()

        D = defaultdict(dict)
        D_with_rules = defaultdict(dict)

        for obj in portfolio_info.get_issues():
            D[issues[obj]['component']] = defaultdict(int)
            D_with_rules[issues[obj]['component']] = defaultdict(int)

        for obj in issues:
            D[issues[obj]["component"]]['project'] = issues[obj]['project']
            D[issues[obj]["component"]]['component'] = issues[obj]["component"]
            D[issues[obj]["component"]]['issue_sum'] = 0
            D_with_rules[issues[obj]["component"]][issues[obj]['rule']] += 1
            for dimension in self.dimensions:
                D[issues[obj]["component"]][dimension] = 0

        for k, v in D_with_rules.items():
            for k1, v1 in v.items():
                for dimension in self.dimensions:
                    if k1 in self.dimensions[dimension]:
                        D[k][dimension] += v1
                        D[k]['issue_sum'] += v1

        return D

    def sort_by_max_sums_per_project(self, class_ATD_values):
        """
        Function that sorts the issue sum of the different projects.
        :param class_ATD_values: It should be a Dataframe containing all the cluster issues
        :return: It returns a Pandas Dataframe which is sorted by the issue_sum and grouped by the Project
        """

        # remove classes with less no violations
        class_ATD_values = class_ATD_values[class_ATD_values['issue_sum'] > 0]

        # reduce to max_number_of_classes per project (files with higher value)
        class_ATD_values = class_ATD_values.sort_values(['project', 'issue_sum'], ascending=False).groupby(
            'project').head(self.max_number_of_classes)
        # get the name of the class
        class_ATD_values['class'] = class_ATD_values['component'].str.split('/').str[-1]
        class_ATD_values = self.capitalize_table(class_ATD_values)
        class_ATD_values = class_ATD_values.groupby('Project')

        return class_ATD_values

    def capitalize_table(self, class_ATD_values):
        """
        Capitalize a table
        :param class_ATD_values:
        :return: Capitalized column names
        """
        list_of_dimensions = ['class']

        for dimension in self.dimensions:
            list_of_dimensions.append(dimension)
        list_of_dimensions.append('project')

        class_ATD_values = class_ATD_values[list_of_dimensions]
        # rename columns to prepare for the markdown export
        list_of_capitalize_dimensions = []
        for element in list_of_dimensions:
            list_of_capitalize_dimensions.append(element.capitalize())

        dict_of_rename = {}

        for capitalize, non_capitalize in zip(list_of_capitalize_dimensions, list_of_dimensions):
            dict_of_rename[non_capitalize] = capitalize

        dict_of_rename['class'] = 'Class name'
        dict_of_rename['component'] = 'Fully qualified class name'
        dict_of_rename['issue_sum'] = 'Total issues'

        class_ATD_values = class_ATD_values.rename(columns=dict_of_rename,
                                                   inplace=False)
        return class_ATD_values

    @abstractmethod
    def generate_report(self, project, portfolio_info):
        """
        This function Generates the report and stores it in a default location
        :param portfolio_info: PortfolioData object containing the already analysed data
        :param project: Name of the project to make a report for
        """
        pass

    @abstractmethod
    def get_table_for_project(self, project):
        """
        Sets a table for the report that suits the max_number_of_classes
        :param project: Name of the project we want the table for
        :return: the corresponding format for the specific ReportGen
        """
        pass
