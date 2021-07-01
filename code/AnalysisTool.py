from abc import ABC, abstractmethod


class AnalysisTool(ABC):
    """This super class is the skeleton for the different analysis tools that could be implemented."""

    @abstractmethod
    def __init__(self, save_intermediate_steps):
        self.save_intermediate_steps = save_intermediate_steps

    @abstractmethod
    def get_from_tool(self, url, path, save_to_fs, field_to_check):
        """ Function to get all the field_to_check of each project individually. And would store this if indicated.

        :param url: the url address of the tool you want to interact with
        :param path: path to save issues to
        :param save_to_fs: Boolean which indicates if the program should store the issues received
        :param field_to_check: Contains the name of the field which represent the measures we get from tool
        """
        pass

    @abstractmethod
    def mine_measures(self, projects_path, measures_path):
        """Function to get all the metadata of the projects and to store them

        :param projects_path: Path to the projects list
        :param measures_path: Path where to store the measures
        """
        pass

    @abstractmethod
    def download_issues(self, project_key, sort_by, ascending_string):
        """Function to download all the issues of a project. Typically used to call get_from_tool

       :param project_key: Key of the project we want to request from the tool Analysis
       :param sort_by: The name of the metric we want it to be sorted by
       :param ascending_string: Boolean to refer the sort
       """
        pass

    @abstractmethod
    def mine_issues(self, projects_path):
        """Function to download all the issues of a project. Typically used to call get_from_tool

       :param project_path: Path to the projects list
       """
        pass

    @abstractmethod
    def filter_metadata(self, projects_metadata):
        """Function to filter the metadata we need for the analysis

       :param projects_metadata: List of raw metadata information of all the projects
       """
        pass

    @abstractmethod
    def count_ar_issues(self, arch_issues, all_projects_path, ar_rules, ar_issues_path):
        """Function to count all the Architectural issues occurrences

        :param arch_issues: The array containing all the architectural issues
        :param all_projects_path: the path to find all the projects
        :param ar_rules: List of all the architectural rules
        :param ar_issues_path: Location where to store the counted of Architectural issues
        """
        pass

    @abstractmethod
    def filter_arch_rules(self, portfolio_data, ar_rules):
        """Function to filter the architectural issues that are contained within the architectural rules given

        :param portfolio_data: PorfolioData object from which we can get the issues of it
        :param ar_rules: List of all the architectural rules
        :return result: Dict with the the filtered issues
        """
        pass

