import requests
from util import *
from AnalysisTool import *


class SonarCloudTool(AnalysisTool, ABC):
    def __init__(self, n, suffix):
        self.save_intermediate_steps = n
        self.suffix = suffix

    def filter_rules(self, issues, ar_rules):
        result = {}
        for i in issues:
            if issues[i]['rule'] in ar_rules:
                result[i] = issues[i]
        if self.save_intermediate_steps == 1:
            save('../data/arch_issues' + self.suffix + '.json', result)
        return result

    def pad_with_zero_projects(self, projects_with_issues, all_projects_path, ar_rules):
        to_merge = {}
        all_projects = json.load(open(all_projects_path, 'r'))
        for p in all_projects:
            if not p['key'] in projects_with_issues:
                to_merge[p['key']] = {
                    'projectKey': p['key'],
                    'design_issues': 0
                }
                for r in ar_rules:
                    to_merge[p['key']][r] = 0
        projects_with_issues.update(to_merge)
        return projects_with_issues

    def count_ar_issues(self, arch_issues, all_projects_path, ar_rules, ar_issues_path):
        counted_ar_issues = {}
        for i in arch_issues:
            if not arch_issues[i]['project'] in counted_ar_issues:
                counted_ar_issues[arch_issues[i]['project']] = {
                    'projectKey': arch_issues[i]['project'],
                    'design_issues': 1
                    # 'total_issues': 0
                }
                for r in ar_rules:
                    counted_ar_issues[arch_issues[i]['project']][r] = 0
                counted_ar_issues[arch_issues[i]['project']][arch_issues[i]['rule']] = 1
            else:
                counted_ar_issues[arch_issues[i]['project']]['design_issues'] += 1
                # result[arch_issues[i]['project']]['total_issues'] = 0
                counted_ar_issues[arch_issues[i]['project']][arch_issues[i]['rule']] += 1
        counted_ar_issues = self.pad_with_zero_projects(counted_ar_issues, all_projects_path, ar_rules)

        column_names = ['projectKey', 'design_issues']
        column_names.extend(ar_rules)

        if self.save_intermediate_steps == 1:
            save(ar_issues_path + self.suffix + '.json', counted_ar_issues)
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
            print (i)
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
        if self.save_intermediate_steps == 1:
            save('../data/meta_data' + self.suffix + '.json', project_values)

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

    def mine_measures(self, projects_path, measures_path):
        with open(projects_path) as json_data:
            projects_dict = json.load(json_data, )

            filtered_projects = projects_dict

            url = 'https://sonarcloud.io/api/measures/component?'

            j = 0

            spec_project_list = list()

            for p in filtered_projects:
                p_key = p['key']

                query = {'componentKey': p_key,
                         'metricKeys': 'duplicated_blocks,duplicated_lines,duplicated_lines_density,violations,false_positive_issues,open_issues,confirmed_issues,reopened_issues,code_smells,sqale_rating,sqale_index,sqale_debt_ratio,bugs,reliability_rating,reliability_remediation_effort,vulnerabilities,security_rating,classes,comment_lines,comment_lines_density,directories,files,lines,ncloc,ncloc_language_distribution,functions'}

                r = requests.get(url, params=query)
                project_specs_new = r.json()
                if 'errors' in project_specs_new:
                    continue
                spec_project_list.append(project_specs_new)

                j += 1
                print('Mined measures for project number ' + str(j))

        if self.save_intermediate_steps == 1:
            save(measures_path, spec_project_list)

        return spec_project_list

    def download_issues(self, org, project_key, sort_by, ascending_string):
        print('Start downloading issues for: ' + project_key + ' --- ' + sort_by + ' --- ' + ascending_string)

        base_url = 'https://sonarcloud.io/api/issues/search?p=PAGE_NUM&ps=10&s=SORT_BY&asc=ASCENDING&projectKeys=PROJECT_KEY'

        page_num = 1

        reached_limit = False
        while not reached_limit:
            url = base_url.replace('PAGE_NUM', str(page_num)).replace('ASCENDING', ascending_string).replace('SORT_BY',
                                                                                                             sort_by).replace(
                'PROJECT_KEY', project_key)
            reached_limit = not self.get_from_tool(url,
                                                   '../data/issues/issues_' + org + '_' + project_key + '_' + sort_by + '_' + ascending_string + '_' + str(
                                                       page_num) + '.json', True, 'issues')
            page_num += 1

    def mine_issues(self, project_path):
        projects = json.load(open(project_path, 'r'))
        counter = 1

        for p in projects:
            print(p['key'] + ' --- ' + str(counter) + '/' + str(len(projects)))
            counter += 1
            # CREATION_DATE, UPDATE_DATE, CLOSE_DATE, ASSIGNEE, SEVERITY, STATUS, FILE_LINE
            # self.download_issues(p['organization'], p['key'], 'CREATION_DATE', 'false')
            # self.download_issues(p['organization'], p['key'], 'UPDATE_DATE', 'false')
            # self.download_issues(p['organization'], p['key'], 'CLOSE_DATE', 'false')
            # issues = download_issues(org, p['key'], 'ASSIGNEE', 'false')
            self.download_issues(p['organization'], p['key'], 'SEVERITY', 'false')
            self.download_issues(p['organization'], p['key'], 'STATUS', 'false')
            self.download_issues(p['organization'], p['key'], 'FILE_LINE', 'false')

            # self.download_issues(p['organization'], p['key'], 'CREATION_DATE', 'true')
            # self.download_issues(p['organization'], p['key'], 'UPDATE_DATE', 'true')
            # self.download_issues(p['organization'], p['key'], 'CLOSE_DATE', 'true')
            # issues = download_issues(org, p['key'], 'ASSIGNEE', 'true')
            self.download_issues(p['organization'], p['key'], 'SEVERITY', 'true')
            self.download_issues(p['organization'], p['key'], 'STATUS', 'true')
            self.download_issues(p['organization'], p['key'], 'FILE_LINE', 'true')

        location = '../data/merged_issues' + self.suffix + '.json'
        merged_issues = merge_crawled_files('../data/issues', 'issues_', '.json', 'issues', location,
                                            self.save_intermediate_steps)
        return merged_issues


def sonarcloud():
    tool = SonarCloudTool(1, 'apache')
    ar_rules = read_json('../data/ar_rules.json')['rules']
    # merged_issues = tool.mine_issues('../data/filtered_projects.json')
    merged_issues = read_json('../data/merged_issues.json')
    # Merge_crawled_files need a refactoring
    arch_issues = tool.filter_rules(merged_issues, ar_rules)

    ar_issues = tool.count_ar_issues(arch_issues, '../data/filtered_projects.json', ar_rules, '../data/ar_issues.json')
    measures = tool.mine_measures('../data/filtered_projects.json', '../data/measures.json')

    metada_data = tool.filter_metadata(measures)

    atdx_input = update_dict_of_dict(ar_issues, metada_data)
    save('../data/ATDx_input.json', atdx_input)
