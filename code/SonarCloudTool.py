import requests

from AnalysisTool import *
from util import *


class SonarCloudTool(AnalysisTool, ABC):

    def __init__(self, suffix):
        super().__init__()
        self.suffix = suffix

    def filter_arch_rules(self, portfolio_info, triple):
        result = {}

        for i in portfolio_info.get_arch_issues():
            if portfolio_info.get_arch_issues()[i]['rule'] in triple and portfolio_info.get_arch_issues()[i]['project'] in portfolio_info.get_projects_info():
                result[i] = portfolio_info.get_arch_issues()[i]

        portfolio_info.set_arch_issues(result)
        return result

    @staticmethod
    def pad_with_zero_projects(projects_with_issues, all_projects, ar_rules):
        to_merge = {}
        for p in all_projects:
            if not p in projects_with_issues:
                to_merge[p] = {
                    'projectKey': p,
                    'design_issues': 0
                }
                for r in ar_rules:
                    to_merge[p][r] = 0
        projects_with_issues.update(to_merge)
        return projects_with_issues

    def count_ar_issues(self, arch_issues, all_projects, ar_rules, ar_issues_path):
        counted_ar_issues = {}
        for i in arch_issues:
            if not arch_issues[i]['project'] in counted_ar_issues:
                counted_ar_issues[arch_issues[i]['project']] = {
                    'projectKey': arch_issues[i]['project'],
                    'design_issues': 1
                }
                for r in ar_rules:
                    counted_ar_issues[arch_issues[i]['project']][r] = 0
                counted_ar_issues[arch_issues[i]['project']][arch_issues[i]['rule']] = 1
            else:
                counted_ar_issues[arch_issues[i]['project']]['design_issues'] += 1
                counted_ar_issues[arch_issues[i]['project']][arch_issues[i]['rule']] += 1
        counted_ar_issues = self.pad_with_zero_projects(counted_ar_issues, all_projects, ar_rules)

        column_names = ['projectKey', 'design_issues']
        column_names.extend(ar_rules)

        return counted_ar_issues

    def filter_metadata(self, project_metadata):
        project_values = {}
        metrics = ['files', 'classes', 'functions', 'ncloc_language_distribution']
        j = 0

        for i in project_metadata:

            files = 0
            classes = 0
            functions = 0
            ncloc_java = 0

            project = i['component']
            projectKey = project['key']

            for current_measure in project['measures']:

                if current_measure['metric'] in metrics:

                    if current_measure['metric'] == 'ncloc_language_distribution':
                        try:
                            ncloc_java = int(re.search('java=([0-9]*)', current_measure['value']).group(1))

                        except AttributeError:
                            ncloc_java = 0

                    if current_measure['metric'] == 'files':
                        files = current_measure['value']

                    if current_measure['metric'] == 'classes':
                        classes = current_measure['value']

                    if current_measure['metric'] == 'functions':
                        functions = current_measure['value']

            if ncloc_java > 0:
                project_values[projectKey] = {}
                project_values[projectKey]['ncloc_java'] = ncloc_java
                project_values[projectKey]['files'] = files
                project_values[projectKey]['classes'] = classes
                project_values[projectKey]['functions'] = functions

            j += 1

        return project_values

    def get_from_tool(self, url, path, save_to_fs, field_to_check):
        response = requests.get(url)
        if response.status_code != 400:
            data = response.json()

            if field_to_check is not None and not data[field_to_check]:
                return False

            if save_to_fs:
                save(path, data)
            else:
                return data

            return True

        else:
            print(response)
            return False

    def mine_measures(self, filtered_projects, measures_path):

        url = 'https://sonarcloud.io/api/measures/component?'
        j = 0
        spec_project_list = list()

        for p in filtered_projects:
            query = {'componentKey': p,
                     'metricKeys': 'classes,files,lines,ncloc,ncloc_language_distribution,functions'}

            r = requests.get(url, params=query)
            project_specs_new = r.json()

            if 'errors' in project_specs_new:
                print('There was error when trying to obtain metrixs for: ' + p + 'the error message is: '+ project_specs_new['errors'][0]['msg'])
                continue

            spec_project_list.append(project_specs_new)

            j += 1
            print('Mined measures for project number ' + str(j))

        return spec_project_list

    def download_issues(self, project_key, sort_by, ascending_string):
        print('Start downloading issues for: ' + project_key + ' --- ' + sort_by + ' --- ' + ascending_string)

        base_url = 'https://sonarcloud.io/api/issues/search?p=PAGE_NUM&ps=10&s=SORT_BY&asc=ASCENDING&projectKeys=PROJECT_KEY'

        page_num = 1

        reached_limit = False
        while not reached_limit:
            url = base_url.replace('PAGE_NUM', str(page_num)).replace('ASCENDING', ascending_string).replace('SORT_BY',
                                                                                                             sort_by).replace(
                'PROJECT_KEY', project_key)
            reached_limit = not self.get_from_tool(url,
                                                   '../data/issues/issues_' + '_' + project_key + '_' + sort_by + '_' + ascending_string + '_' + str(
                                                       page_num) + '.json', True, 'issues')
            page_num += 1

    def mine_issues(self, project):

        print("Mining issues for: " + project['projectKey'])

        # CREATION_DATE, UPDATE_DATE, CLOSE_DATE, ASSIGNEE, SEVERITY, STATUS, FILE_LINE
        self.download_issues(project['projectKey'], 'CREATION_DATE', 'false')

    def merge_portfolio_issues(self, portfolio_info):

        for project in portfolio_info.get_projects_info():
            self.mine_issues(portfolio_info.get_projects_info()[project])

        merged_issues = merge_crawled_files('../data/issues', 'issues_', '.json', 'issues',
                                            '../data/' + self.suffix + 'non_filtered.json')
        portfolio_info.set_arch_issues(merged_issues)

        return merged_issues

    def merge_issues(self, portfolio_info, sua):

        if portfolio_info.get_ar_issues() is None:
            merged_issues = self.merge_portfolio_issues(portfolio_info)
        else:
            self.mine_issues(portfolio_info.get_projects_info()[sua])
            items_to_add = merge_crawled_files('../data/issues', 'issues_', '.json', 'issues', '../data/' + self.suffix + 'non_filtered.json')
            merged_issues = items_to_add

        portfolio_info.set_arch_issues(merged_issues)

    def prepare_ATDx_input(self, portfolio_info,  measures, ar_issues):
        metada_data = self.filter_metadata(measures)

        atdx_input = update_dict_of_dict(metada_data, ar_issues)
        portfolio_info.set_analysis_projects_info(atdx_input)

    def execute_analysis(self, portfolio_info, sua):
        triple = portfolio_info.get_triple()
        measures = portfolio_info.get_measures()
        read_ar_issues = portfolio_info.get_ar_issues()

        self.merge_issues(portfolio_info, sua)
        arch_issues = self.filter_arch_rules(portfolio_info, triple)

        ar_issues = self.count_ar_issues(arch_issues, portfolio_info.get_projects_info(), triple,
                                         '../data/ar_issues')

        if read_ar_issues is not None:
            read_ar_issues.update(ar_issues[sua])
            ar_issues = read_ar_issues

        if measures is None:
            measures = self.mine_measures(portfolio_info.get_projects_info(), '../data/measures.json')

        self.prepare_ATDx_input(portfolio_info, measures, ar_issues)

    def save(self, portfolio):

        issues = portfolio.get_ar_issues()
        measures = portfolio.get_measures()
        arch_issues = portfolio.get_arch_issues()

        save('../data/' + self.suffix + 'counted_issues,json', issues)
        save('../data/' + self.suffix + 'measures.json', measures)
        save('../data/' + self.suffix + 'arch_issues.json', arch_issues)

    def execute_portfolio_analysis(self, portfolio_info):
        triple = portfolio_info.get_triple()
        ar_issues = portfolio_info.get_ar_issues()
        measures = portfolio_info.get_measures()
        arch_issues = portfolio_info.get_arch_issues()

        if arch_issues is None:
            self.merge_portfolio_issues(portfolio_info)
            arch_issues = self.filter_arch_rules(portfolio_info, triple)
            ar_issues = self.count_ar_issues(arch_issues, portfolio_info.get_projects_info(), triple,
                                             '../data/ar_issues')
        if measures is None:
            measures = self.mine_measures(portfolio_info.get_projects_info(), '../data/measures.json')

        self.prepare_ATDx_input(portfolio_info, measures, ar_issues)