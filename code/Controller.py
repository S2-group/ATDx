from AnalysisToolFactory import *
from ReportGenFactory import *
from PortfolioData import *
from atdx_core import *


class Controller:
    def __init__(self):
        self.tool = None
        self.report_gen = None
        self.atdx = None

    def setup(self, sua_name):
        """
        This function executes calls the different setup for the the analysis tool and report generation

        :param sua_name: the name of the project to execute the analysis for
        """
        self.setup_analysis_tool_portfolio(sua_name)
        self.setup_report_gen()

    def setup_report_gen(self):
        """
        This function sets up the report generation object inside the Controller Class
        """
        report_factory = ReportGenFactory()
        config = read_json('../data/report_config.json')

        report_name = config["report"]
        number_class = int(config["max_number_class"])
        number_projects = int(config["max_number_projects"])
        # store = config["store"]
        self.report_gen = report_factory.get_report_gen(report_name, number_projects, number_class, self.portfolio_data)

    def init_portfolio_info(self, rules, triple, dimensions,sua_info, projects_info, issues, measures,arch_issues):
        self.portfolio_data = PortfolioData(rules, triple,dimensions, sua_info, projects_info, issues, measures, arch_issues)

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

    def setup_analysis_tool_portfolio(self, sua_name):
        """
        This function reads the config json and sets up the content of the porftolio_info as well as the analysis tool
        :param sua_name: Name of the project to analysed
        """
        tool_factory = AnalysisToolFactory()
        config = read_json('../data/configuration.json')

        rules = read_json('../data/' + config["rules_location"])
        projects = read_json('../data/' + config["projects_location"])

        tool_name = config["tool"]
        save_intermediate_steps = config["save_intermediate_steps"]
        suffix = config["files_suffix"]

        issues = self.get_content(config, "issues")
        measures = self.get_content(config, "measures")

        self.init_portfolio_info(rules["rules"], rules["triple"], rules['dimensions'], projects[sua_name], projects, issues, measures, None)
        self.tool = tool_factory.get_analysis_tool(tool_name, save_intermediate_steps, suffix)
        self.atdx = AtdxCore()

    def run(self, sua_name):
        """
        This functions runs all the steps from setup to generate the report
        :param sua_name: string containing the name of the project to analyze
        """
        self.setup(sua_name)
        self.tool.execute_analysis(self.portfolio_data, sua_name)
        self.atdx.execute_atdx_analysis(self.portfolio_data, sua_name)
        self.report_gen.generate_report(sua_name, self.portfolio_data)

    def get_atdx_value(self):
        return self.portfolio_data.get_atdx()


if __name__ == "__main__":
    controller = Controller()
    controller.run('apache_sling-org-apache-sling-commons-html')

