import csv
import json


# Save JSON data into the given filePath
def save(file_path, data):
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile, indent=4, default=str)


def read_ar_rules(csv_path):
    result = {}

    with open(csv_path, 'r') as ar_rules_csv:
        # we load the data
        csv_reader = csv.DictReader(ar_rules_csv, delimiter=',')
        for line in csv_reader:
            result[line['id']] = line
    return result


def filter_rules(issues_path, ar_rules):
    issues = json.load(open(issues_path, 'r'))
    result = {}
    for i in issues:
        if issues[i]['rule'] in ar_rules:
            result[i] = issues[i]
    return result


def pad_with_zero_projects(projects_with_issues, all_projects_path, ar_rules):
    to_merge = {}
    all_projects = json.load(open(all_projects_path, 'r'))
    for p in all_projects:
        if ((not p['key'] in projects_with_issues)):
            to_merge[p['key']] = {
                'projectKey': p['key'],
                'design_issues': 0
            }
            for r in ar_rules:
                to_merge[p['key']][r] = 0
    projects_with_issues.update(to_merge)
    return projects_with_issues


def count_ar_issues(arch_issues, all_projects_path, ar_rules, ar_issues_path):
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
    counted_ar_issues = pad_with_zero_projects(counted_ar_issues, all_projects_path, ar_rules)

    column_names = ['projectKey', 'design_issues']
    column_names.extend(ar_rules)

    with open(ar_issues_path, 'w') as ar_issues_file:
        writer = csv.DictWriter(ar_issues_file, fieldnames=column_names)
        writer.writeheader()
        for data in counted_ar_issues.values():
            writer.writerow(data)


if __name__ == "__main__":
    ar_rules = read_ar_rules('../data/ar_rules.csv')
    arch_issues = filter_rules('../data/merged_issues.json', ar_rules)
    save('../data/arch_issues.json', arch_issues)

# arch_issues = json.load(open('./data/arch_issues.json', 'r'))
# count_ar_issues(arch_issues, './data/merged_projects.json', ar_rules, './data/onap_ar_issues.csv')
# count_ar_issues(arch_issues, 'apache', './data/merged_projects.json', ar_rules, './data/apache_ar_issues.csv')
