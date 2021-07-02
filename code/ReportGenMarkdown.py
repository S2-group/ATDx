from ReportGen import *
import pandas as pd
from util import *

report_header_1 = """# ATDx Report Summary
Our ATDx analysis targets a portfolio of software projects and identifies the pain points of each project in terms of Architectural Technical Debt (ATD). This evaluation is based on a statistical analysis of the violations of SonarCloud rules.

## ATDx in a nutshell
![ATDx in a nutshell](https://raw.githubusercontent.com/S2-group/ATDx_reports/master/plots/atdx_in_a_nutshell.jpg)
ATDx works by comparing architectural debt metrics across the projects of a software portfolio. Intuitively, it ensures that measurements across different projects are comparable, and then evaluates the severity of Architectural Technical Debt by confronting the measurements across the projects.
The ATDx approach is by itself tool-independent, and can be customized according the analysis tools available, and the portfolio considered.
In the case of this report, we used an instance of ATDx based on the static analysis tool [SonarQube](https://www.sonarqube.org/).
The instance of ATDx used to analyze your projects provides an overview of the architectural technical debt in a project in distinct dimensions:
"""
report_header_2 = """\nFor each project, the dimensions assume a value between 0 and 5, where 0 denotes minimum architectural debt of the project in that dimension, and 5 maximum architectural debt.
In the reminder of this report, we give for the analysed project the following:
1. A radar chart for the project
2. A table showing the top-"""

report_header_3 = """ classes of the project with the highest architectural technical debt.
If you are curious about more theoretical background on ATDx, you can have a look at [this scientific publication](https://robertoverdecchia.github.io/papers/ENASE_2020.pdf).

"""


class ReportGenMarkdown(ReportGen, ABC):
    def __init__(self, max_number_of_classes, portfolio_info,report_repository, github_branch ):
        super().__init__(max_number_of_classes,report_repository,github_branch)
        self.set_dimension_list(portfolio_info.get_triple())
        self.report_header = report_header_1

        second_part = report_header_2 + str(max_number_of_classes) + report_header_3
        for dimension in portfolio_info.get_dimension_info():
            string_to_store = "* **" + dimension + "**: " + portfolio_info.get_dimension_info()[dimension]
            self.report_header = self.report_header + string_to_store + "\n"

        self.report_header = self.report_header + second_part

    def generate_report(self, project, portfolio_info):
        clustered_issues = self.cluster_issues_per_class(portfolio_info)
        clustered_issues_for_function = pd.DataFrame.from_dict(clustered_issues).transpose()
        sorted_max_issues = self.sort_by_max_sums_per_project(clustered_issues_for_function)
        self.generate_radarchart(project, portfolio_info)

        report = self.report_header + '\n'

        report = report + '# ATDx project report summary\n'
        report = report + '\n### The ATDx value for this project is: ' + str(round(portfolio_info.get_atdx()[project], 4))+ '\n\n'
        for elements in sorted_max_issues:
            if elements[0] == project:
                report = report + '<img src=\"radarchart/' + elements[0] + '.jpg\"/>' + '<p style="text-align:left">[Project on Github](' + portfolio_info.get_projects_info()[project]['repo_url'] + ') <br> [Project on SonarCloud ](https://sonarcloud.io/dashboard?id=' + elements[0] + ') <br></p>\n'
                report = report + '\n'
                report = report + self.get_table_for_project(elements)
                break

        filename = '../data/reports/' + project + '.md'

        with open(filename, 'w') as file:
            file.write(report)

    def get_table_for_project(self, project):
        project_df = project[1]
        row_count = project_df.shape[0]

        i = 0
        while i <= self.max_number_of_classes - row_count:
            project_df.loc[i + row_count] = '-'
            i += 1
        string_to_return = '### Top classes with architectural debt violations'+ '\n' + project_df.to_markdown(index=False) +'\n'

        return string_to_return

    def set_dimension_list(self, triple):
        dimensions_with_rules = get_dimension_list(triple)
        self.dimensions = dimensions_with_rules

    def get_body_comment(self, atdx_value, project_name):
        body_to_return = '# ATDx analysis results\n'

        image = '\n\n<img src="' + github_raw_content_header + self.repo_location + self.github_branch \
                + '/data/reports/radarchart/' + project_name + '.jpg"/>'

        body_to_return = body_to_return + '\n\n### The **ATDx** value is: ' + str(round(atdx_value[project_name], 3))
        report = '[' + 'here.' + '](' + github_normal_header + self.repo_location + 'blob/' + self.github_branch + '/data/reports/' \
                 + project_name + '.md)'

        body_to_return = body_to_return + image
        body_to_return = body_to_return + '\n\n### The report with the complete ATDx analysis results can be found ' + report
        return body_to_return

    @staticmethod
    def get_git_command(name, number):
        report = '../data/reports/' + name + '.md'
        radarchart = '../data/reports/radarchart/' + name + '.jpg;'

        command = 'git add ' + report + ' ' + radarchart + ' git commit -m "Analysis of the ' + name + \
                  ' repository for PR number ' + str(number) + '"; git pull; git push'

        return command