from ReportGenMarkdown import *


class ReportGenFactory:
    def __init__(self):
        self.report_to_gen = {
            "Markdown": ReportGenMarkdown,
        }

    def get_report_gen(self, report_gen, max_number_of_projects, max_number_of_classes, dimensions_to_print, issues_location):
        if report_gen in self.report_to_gen:
            tool_to_return = self.report_to_gen[report_gen]
            return tool_to_return( max_number_of_projects, max_number_of_classes, dimensions_to_print, issues_location)
        else:
            print("The analysis tool doesn't exist. The available ones are:")
            for keys in self.report_to_gen:
                print(keys)
