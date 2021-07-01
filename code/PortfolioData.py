class PortfolioData:
    """This class is a mere information holder. Storing all the information that we want to use to analyse.
    """

    def __init__(self,  triple_rules, dimensions, sua_info, projects_info, ar_issues, measures, arch_issues):
        """
        :param dimensions: Dict containing the dimensions and their definitions
        :param triple_rules: 3-tuples containing the ATDD and the granularity of the architectural rules
        :param sua_info: Single project information
        :param projects_info: Dict of projects as keys holding it's information
        :param issues: Dict containing all the mined issues from the analysis tool
        :param measures: Dict containing all the projects as key and measures as content
        :param arch_issues: This attribute holds the architectural issues if already calculated.
        """
        self.dimensions = dimensions
        self.meaures = measures
        self.ar_issues = ar_issues
        self.triple = triple_rules
        self.arch_issues = arch_issues
        self.projects_info = projects_info
        self.SUA_info = sua_info
        self.analysis_projects_info = None
        self.atdx = None
        self.project_issues = None

    def set_arch_issues(self, arch_issues):
        self.arch_issues = arch_issues

    def set_atdx(self, atdx):
        self.atdx = atdx

    def set_issues(self, issues):
        self.project_issues = issues

    def set_analysis_projects_info(self, info):
        self.analysis_projects_info = info

    def get_arch_issues(self):
        return self.arch_issues

    def get_projects_info(self):
        return self.projects_info

    def get_sua_info(self):
        return self.SUA_info

    def get_issues(self):
        return self.project_issues

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

    def get_dimension_info(self):
        return self.dimensions

    def get_ar_issues(self):
        return self.ar_issues