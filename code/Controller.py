from AnalysisToolFactory import *
from ReportGenFactory import *
from PortfolioData import *
from atdx_core import *


class Controller:
    def __init__(self):
        self.tool_factory = AnalysisToolFactory()
        self.report_factory = ReportGenFactory()
        self.portfolio_data = None
        self.tool = None
        self.report_gen = None
        self.atdx = None

    def setup(self, sua_name):
        self.setup_analysis_tool_portfolio(sua_name)
        self.setup_report_gen()

    def setup_report_gen(self):
        config = read_json('../data/report_config.json')

        report_name = config["report"]
        number_class = int(config["max_number_class"])
        number_projects = int(config["max_number_projects"])
        # store = config["store"]
        self.report_gen = self.report_factory.get_report_gen(report_name, number_projects, number_class, None, self.portfolio_data)

    def init_portfolio_info(self, rules, triple, sua_info, projects_info, issues, measures,arch_issues):
        self.portfolio_data = PortfolioData(rules, triple, sua_info, projects_info, issues, measures, arch_issues)

    @staticmethod
    def get_content(config, string):
        if config[string] == "None":
            location_content = None
        else:
            location_content = read_json('../data/' + config[string])

        return location_content

    def setup_analysis_tool_portfolio(self, sua_name):
        config = read_json('../data/configuration.json')

        rules = read_json('../data/' + config["rules_location"])
        projects = read_json('../data/' + config["projects_location"])

        tool_name = config["tool"]
        store = config["store"]
        suffix = config["files_suffix"]

        issues = self.get_content(config, "issues")
        measures = self.get_content(config, "measures")

        self.init_portfolio_info(rules["rules"], rules["triple"], projects[sua_name], projects, issues, measures, None)
        self.tool = self.tool_factory.get_analysis_tool(tool_name, store, self.portfolio_data, suffix)
        self.atdx = AtdxCore(self.portfolio_data)

    def run(self, sua_name):
        self.setup(sua_name)
        self.tool.execute_analysis(sua_name)
        self.atdx.execute_atdx_analysis(sua_name)
        self.report_gen.execute_report_gen(sua_name)


if __name__ == "__main__":
    controller = Controller()
    controller.run('apache_sling-org-apache-sling-launchpad-integration-tests')

