from AnalysisToolFactory import *
from ReportGenFactory import *
from PortfolioData import *
from ATDxCore import *


class Controller:
    def __init__(self):
        self.tool = None
        self.report_gen = None
        self.atdx = None
        self.portfolio_data = None

    def setup(self, main_config_location, report_config_location):
        """
        This function executes calls the different setup for the the analysis tool and report generation

        :param main_config_location: string containing the name of the main configuration file
        :param report_config_location:  string containing the name of the report configuration file
        """
        self.setup_analysis_tool_portfolio(main_config_location)
        self.setup_report_gen(report_config_location)

    def setup_report_gen(self, report_config_location):
        """
        This function sets up the report generation object inside the Controller Class
        """
        report_factory = ReportGenFactory()
        config = read_json(report_config_location)

        report_name = config["report"]
        number_class = int(config["max_number_class"])
        report_repository = config["github_repository_location"]
        github_branch = config['github_branch']
        self.report_gen = report_factory.get_report_gen(report_name, number_class, self.portfolio_data, report_repository, github_branch)

    @staticmethod
    def get_content(config, key):
        """
        This function gets the content of a given location returns it's content
        :param config: Dict we want to get the location from
        :param key: Key of the dict
        :return: The content of the location or None if there was no such a content
        """
        if config[key] == "None":
            location_content = None
        else:
            location_content = read_json('../data/' + config[key])

        return location_content

    def setup_analysis_tool_portfolio(self, config_location):
        """
        This function reads the config json and sets up the content of the porftolio_info as well as the analysis tool
        :param config_location: string containing the name of the configuration filey
        """
        tool_factory = AnalysisToolFactory()
        config = read_json(config_location)

        rules = read_json('../data/' + config["rules_location"])
        projects = read_json('../data/' + config["projects_location"])

        tool_name = config["tool"]
        suffix = config["files_suffix"]

        counted_issues = self.get_content(config, "counted_issues")
        arch_issues = self.get_content(config, "arch_issues")

        measures = self.get_content(config, "measures")

        self.portfolio_data = PortfolioData(rules["triple"], rules['dimensions'], projects, counted_issues, arch_issues, measures)
        self.tool = tool_factory.get_analysis_tool(tool_name, suffix)
        self.atdx = ATDxCore()

    def run_sua(self, sua_name):
        """
        This functions runs all the steps from setup to generate the report
        :param sua_name: string containing the name of the project to analyze
        """

        self.setup( '../data/configuration.json', '../data/report_config.json')
        self.tool.execute_analysis(self.portfolio_data, sua_name)
        self.atdx.execute_ATDx_analysis(self.portfolio_data)

        self.report_gen.generate_report(sua_name, self.portfolio_data)
        self.save_dataset()

    def run_portfolio(self, main_config_location, report_config_location):

        self.setup(main_config_location, report_config_location)
        self.tool.execute_portfolio_analysis(self.portfolio_data)
        self.atdx.execute_ATDx_analysis(self.portfolio_data)

        for projects in self.portfolio_data.get_projects_info():
            self.report_gen.generate_report(projects, self.portfolio_data)

        self.save_dataset()

    def publish_report(self, name, pr_number):
        command = self.report_gen.get_git_command(name, pr_number)
        # Pushing the report and radarchart to the specfied github location in the config file
        os.system(command)

    def get_body_comment(self, project_name):
        return self.report_gen.get_body_comment(self.portfolio_data.get_atdx(), project_name)

    def save_dataset(self):
        self.tool.save(self.portfolio_data)


if __name__ == "__main__":
    controller = Controller()
    valid_input = False

    while not valid_input:
        single_or_portfolio = input('Please input 1 for single project analysis or 2 for portfolio analysis\n')

        if single_or_portfolio == '1':
            SUA = input("Please input the name of the Sistem Under Analysis.\n")
            controller.run_sua(SUA)
            valid_input = True

        if single_or_portfolio == '2':
            main_config_location = input("Please input the main configuration file location.\n")
            report_config = input("Please input the report configuration file location.\n")
            controller.run_portfolio(main_config_location, report_config)
            valid_input = True

