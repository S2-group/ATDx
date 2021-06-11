from AnalysisToolFactory import *
from ReportGenFactory import *
from PortfolioData import *


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
        number_class = read_json(config["max_number_class"])
        number_projects = read_json(config["max_number_projects"])
        store = config["store"]
        self.report_gen = self.report_factory.get_report_gen(report_name, number_projects, number_class, None)

    def init_portfolio_info(self, rules, sua_info, projects_info, issues, arch_issues):
        self.portfolio_data = PortfolioData(rules, sua_info, projects_info, issues, arch_issues)

    def setup_analysis_tool_portfolio(self, sua_name):
        config = read_json('../data/configuration.json')

        tool_name = config["tool"]
        rules = read_json(config["rules_location"])
        projects = read_json(config["projects_location"])
        issues = read_json(config["issues_location"])
        store = config["store"]
        suffix = config["files_suffix"]

        report_name = config["report_gen"]

        if issues == "None":
            issues = None

        self.init_portfolio_info(rules["rules"], projects[sua_name], projects, issues, None)
        self.tool = self.tool_factory.get_analysis_tool(tool_name, store, self.portfolio_data, suffix)

    def run(self, sua_name):
        self.setup(sua_name)

