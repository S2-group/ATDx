from ReportGen import *
from util import *
import pandas as pd


class ReportGenMarkdown(ReportGen, ABC):
    def __init__(self, max_number_of_projects, max_number_of_classes, dimensions_to_print, issues_location):
        super().__init__(max_number_of_projects, max_number_of_classes, dimensions_to_print, issues_location)
        self.report_header = """# ATDx Report Summary
    Our ATDx analysis targets a portfolio of software projects and identifies the pain points of each project in terms of Architectural Technical Debt (ATD). This evaluation is based on a statistical analysis of the violations of SonarCloud rules.
    ## ATDx in a nutshell
    ![ATDx in a nutshell](https://raw.githubusercontent.com/S2-group/ATDx_reports/master/plots/atdx_in_a_nutshell.jpg)
    ATDx works by comparing architectural debt metrics across the projects of a software portfolio. Intuitively, it ensures that measurements across different projects are comparable, and then evaluates the severity of Architectural Technical Debt by confronting the measurements across the projects.
    The ATDx approach is by itself tool-independent, and can be customized according the analysis tools available, and the portfolio considered.
    In the case of this report, we used an instance of ATDx based on the static analysis tool [SonarQube](https://www.sonarqube.org/).
    The instance of ATDx used to analyze your projects provides an overview of the architectural technical debt in a project in 6 distinct dimensions:
    * **Inheritance**: flaws concerning inheritance mechanisms between classes, such as overrides and inheritance of methods or fields
    * **Exception**: flaws regarding the management of Java exceptions and the subclassing of the “Exception” Java class.
    * **JVMS**: potential misuses of the Java Virtual Machine, e.g., the incorrect usage of the specific Java class “Serializable”
    * **Threading**: flaws arising from the implementation of multiple execution threads, which could potentially lead to concurrency problems
    * **Interface**: flaws related to the usage of Java interfaces
    * **Complexity**: flaws derived from prominent complexity measures, such as McCabe’s cyclomatic complexity
    For each project, the dimensions assume a value between 0 and 5, where 0 denotes minimum architectural debt of the project in that dimension, and 5 maximum architectural debt.
    In the reminder of this report, we firstly provide a set of radar charts (one for each project). Then for each project we give:
    1. The same radar chart as shown at the beginning
    2. A table showing the top-10 classes of the project with the highest architectural technical debt.
    Note that if numerous classes with 1 violation are reported, this might point to a widespread problem (only a maximum of 10 classes are provided per project for the sake of readability). Similarly, empty rows indicate that only a few classes are affected by ATDx violations.
    If you are curious about more theoretical background on ATDx, you can have a look at [this scientific publication](https://robertoverdecchia.github.io/papers/ENASE_2020.pdf).
    ## ATDx radar charts of your projects
    """

    def generate_report(self, project):
        table = ''
        i = 0
        report = self.report_header
        clustered_issues = self.cluster_issues_per_class(self.issues_location)
        clustered_issues_for_function = pd.DataFrame.from_dict(clustered_issues).transpose()
        sorted_max_issues = self.sort_by_max_sums_per_project(clustered_issues_for_function)
        print(sorted_max_issues.get_group('apache_sling-org-apache-sling-commons-html'))
        for elements in sorted_max_issues:
            blocks = []
            block = '<p align="center">Analysed project ' + str(i+1) +'</p><img src=\"radarchart/' + elements[0] + '.jpg\"/> <p style="text-align:left">[Project on Github](https://github.com/' + elements[0]+ ') <br> [Project on SonarCloud ](https://sonarcloud.io/dashboard?id=' + elements[0] + ') <br></p>'

            blocks.append(block)

            # if 9 projects included
            if i == self.max_number_of_projects:
                break

            # create table with overview of the projects
            if len(blocks) == 2:
                table = '|||\n|-|-|\n'
                table = table + '|' + blocks[0]
                table = table + '|' + blocks[1]

            else:
                #table = '||||\n|-|-|-|\n'
                table = '\n'
                for i in range(0, len(blocks)):
                    table = table + '|' + blocks[i]

                    if (i + 1) % 3 == 0:
                        if i == self.max_number_of_projects:
                            table = table + '\n'
                            break
                        else:
                            table = table + '\n | |\n'

            report = report + table + '\n'
            i += 1

        i = 0
        report = report + '# ATDx project report summaries\n'
        for elements in sorted_max_issues:
            report = report + '## Project ' + str(i + 1) + ': _' + elements[0] + '_' + '\n'
            report = report + '|<img src=\"radarchart/' + elements[0] + '.jpg\"/>|' + '<p style="text-align:left">[Project on Github](https://github.com/' + elements[0] + ') <br> [Project on SonarCloud ](https://sonarcloud.io/dashboard?id=' + elements[0] + ') <br></p>\n'
            report = report + '|-|-|\n'
            report = report + '\n'
            report = report + self.get_table_for_project(elements)
            # if max_number_of_projects included
            if i == self.max_number_of_projects:
                break
            i += 1

        filename = '../data/reports/test_report.md'

        with open(filename, 'w') as file:

            file.write(report)

    def generate_max_dimensions_per_project(self, json_location):
        class_ATD_values = pd.read_json(json_location).transpose()
        max_all_dimensions = pd.DataFrame()
        array_of_dimensions= []
        for dimension in self.dimensions:
            max_class_sum = class_ATD_values.sort_values(dimension, ascending=False).drop_duplicates(['project'])
            max_class_sum.insert(2, 'max_type', dimension)
            max_all_dimensions = pd.concat([max_all_dimensions, max_class_sum])
            array_of_dimensions.append(dimension)

        max_all_dimensions['max_type'] = pd.Categorical(max_all_dimensions['max_type'], array_of_dimensions)

        grouped = max_all_dimensions.groupby('project')

        for project in grouped:
            project_df = project[1]
            # project_df = project_df.drop('project', axis=1)
            f = open('../data/reports/{0}.md'.format('test_report'), 'w')
            f.write('### Top classes with architectural debt' + '\n' + project_df.to_markdown(index=False) + '\n')
            f.close()


    def get_table_for_project(self, project):
        # number_of_projects = 0
        # for project in class_ATD_values:
        #    if number_of_projects >= self.max_number_of_projects:
        #        break
        project_df = project[1]
        # project_name = project[0]

        # project_df = project_df.drop('Project', axis=1)

        row_count = project_df.shape[0]

        i = 0

        while i <= self.max_number_of_classes - row_count:
            project_df.loc[i + row_count] = '-'
            i += 1
        string_to_return = '### Top classes with architectural debt violations'+ '\n' +project_df.to_markdown(index=False) +'\n'
        return string_to_return
        # number_of_projects += 1


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

    # This part is just a fix for the ATDx implementation. it will be changed
    dimensions = read_json('../data/dimensions_dataset_output.json')
    my_projects = read_json('../data/filtered_projects.json')
    rules = read_json('../data/ar_rules.json')
    new_dict = {}

    dimensions_to_store = get_dimension_list(rules['triple'])

    for dimension in dimensions:
        for projects in dimensions[dimension]:
            if projects not in new_dict:
                new_dict[projects] = {}
            new_dict[projects][dimension] = dimensions[dimension][projects]

    # print(dimensions_to_store)
    rep_gen = ReportGenMarkdown(1, 5, dimensions_to_store, '../data/arch_issues.json')

    # for project in new_dict:
    #    rep_gen.generate_radarchart(new_dict[project], project)

    rep_gen.generate_report(my_projects)
