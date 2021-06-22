class PortfolioData:
    """This class is a mere information holder. Storing all the information that we want to use to analyse.
    """

    def __init__(self, ar_rules, triple_rules, sua_info, projects_info, issues, measures, arch_issues):
        """

        :param ar_rules: List of Architectural rules
        :param triple_rules:
        :param sua_info: Single project information
        :param projects_info: Dict of projects as keys holding it's information
        :param issues:
        :param measures:
        :param arch_issues: This attribute hols the architectural issues if already calculated.
        """
        self.meaures = measures
        self.issues = issues
        self.triple = triple_rules
        self.arch_issues = arch_issues
        self.ar_rules = ar_rules
        self.projects_info = projects_info
        self.SUA_info = sua_info
        self.analysis_projects_info = None
        self.atdx = None

    def set_arch_issues(self, arch_issues):
        self.arch_issues = arch_issues

    def set_atdx(self, atdx):
        self.atdx = atdx

    def set_issues(self, issues):
        self.issues = issues

    def set_analysis_projects_info(self, info):
        self.analysis_projects_info = info

    def get_arch_issues(self):
        return self.arch_issues

    def get_ar_rules(self):
        return self.ar_rules

    def get_projects_info(self):
        return self.projects_info

    def get_sua_info(self):
        return self.SUA_info

    def get_issues(self):
        return self.issues

    def get_triple(self):
        return self.triple

    def get_measures(self):
        return self.meaures

    def get_analysis_projects_info(self):
        return self.analysis_projects_info

    def get_atdx(self):
        return self.atdx

    def get_project_key(self, sua):
        for projects in self.get_projects_info():
            if projects == sua:
                return self.get_projects_info()[projects]['projectKey']

        print("The selected project was not found")
