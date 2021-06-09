
class PortfolioData:
    def __init__(self, ar_rules, projects_info):
        self.arch_issues = None
        self.ar_rules = ar_rules
        self.project_info = projects_info

    def set_arch_issues(self, arch_issues):
        self.arch_issues = arch_issues
