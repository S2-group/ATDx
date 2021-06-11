from collections import defaultdict
from abc import ABC, abstractmethod

import matplotlib.pylab as plot
import numpy as np
from util import *


class ReportGen(ABC):

    def __init__(self, max_number_of_projects, max_number_of_classes, dimensions_to_print, issues_location, portfolio_info):
        self.max_number_of_projects = max_number_of_projects
        self.max_number_of_classes = max_number_of_classes
        self.dimensions = dimensions_to_print
        self.issues_location = issues_location
        self.portfolio_info = portfolio_info

    def get_categories_pair(self, my_dict):
        category_value = []
        for category in self.dimensions:
            category_value.append(my_dict[category])

        return category_value

    def generate_radarchart(self, dimension_value_pair, project_name):
        ax = plot.subplot(polar="True")

        values = self.get_categories_pair(dimension_value_pair)
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
        plot.savefig('../data/radarchart/' + project_name + '.jpg')

    def cluster_issues_per_class(self, json_path):

        json_issues = json.load(open(json_path))

        D = defaultdict(dict)
        D_with_rules = defaultdict(dict)
        for obj in json_issues:
            D[json_issues[obj]['component']] = defaultdict(int)
            D_with_rules[json_issues[obj]['component']] = defaultdict(int)

        for obj in json_issues:
            D[json_issues[obj]["component"]]['project'] = json_issues[obj]['project']
            D[json_issues[obj]["component"]]['component'] = json_issues[obj]["component"]
            D[json_issues[obj]["component"]]['issue_sum'] = 0
            D_with_rules[json_issues[obj]["component"]][json_issues[obj]['rule']] += 1
            for dimension in self.dimensions:
                D[json_issues[obj]["component"]][dimension] = 0

        for k, v in D_with_rules.items():
            for k1, v1 in v.items():
                for dimension in self.dimensions:
                    if k1 in self.dimensions[dimension]:
                        D[k][dimension] += v1
                        D[k]['issue_sum'] += v1

        return D

    def sort_by_max_sums_per_project(self, class_ATD_values):

        # remove classes with less no violations
        class_ATD_values = class_ATD_values[class_ATD_values['issue_sum'] > 0]
        # reduce to max_number_of_classes per project (files with higher value)
        class_ATD_values = class_ATD_values.sort_values(['project', 'issue_sum'], ascending=False).groupby('project').head(self.max_number_of_classes)
        # get the name of the class
        class_ATD_values['class'] = class_ATD_values['component'].str.split('/').str[-1]
        class_ATD_values = self.capitalize_table(class_ATD_values)
        class_ATD_values = class_ATD_values.groupby('Project')

        return class_ATD_values

    def capitalize_table(self, class_ATD_values):
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
    def generate_report(self, projects_data, project):
        pass

    @abstractmethod
    def generate_max_dimensions_per_project(self, json_location):
        pass

    @abstractmethod
    def get_table_for_project(self, project):
       pass

