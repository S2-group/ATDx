from abc import ABC, abstractmethod


class AnalysisTool(ABC):

    @abstractmethod
    def __init__(self, n):
        self.save_intermediate_steps = n

    @abstractmethod
    def get_from_tool(self, url, path, save_to_fs, field_to_check):
        pass

    @abstractmethod
    def mine_measures(self, projects_path, measures_path):
        pass

    @abstractmethod
    def download_issues(self,  org, project_key, sort_by, ascending_string):
        pass

    @abstractmethod
    def mine_issues(self, project_path):
        pass

    @abstractmethod
    def filter_metadata(self, project_metadata):
        pass

    @abstractmethod
    def count_ar_issues(self, arch_issues, all_projects_path, ar_rules, ar_issues_path):
        pass

    @abstractmethod
    def filter_rules(self, issues_path, ar_rules):
        pass

