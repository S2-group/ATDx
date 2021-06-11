class PortfolioData:
    """This class is a mere information holder. It can take 4 arguments from which, arch_issues is set by default to None
    as we don't expect to have it since the beginning. The functions it contains are just getter and setters.
    """

    def __init__(self, ar_rules, sua_info, projects_info, arch_issues):
        """
        :param ar_rules: List of Architectural rules
        :param sua_info: Single project information
        :param projects_info: Dict of projects as keys holding it's information
        :param arch_issues: This attribute hols the architectural issues if already calculated.
        """
        self.arch_issues = arch_issues
        self.ar_rules = ar_rules
        self.projects_info = projects_info
        self.SUA_info = sua_info

    def set_arch_issues(self, arch_issues):
        self.arch_issues = arch_issues

    def get_arch_issues(self):
        return self.arch_issues

    def get_ar_rules(self):
        return self.ar_rules

    def get_projects_info(self):
        return self.projects_info

    def get_sua_info(self):
        return self.SUA_info
