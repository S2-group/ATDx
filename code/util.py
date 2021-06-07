import re
import os
import json


# Save JSON data into the given filePath
def save(file_path, data):
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile, indent=4, default=str)


def update_dict_of_dict(dict_to_update, dict_to_add):
    final_dict = dict_to_update.copy()

    if dict_to_update:
        for key in dict_to_update:
            if key in dict_to_add:
                for key_to_update, value in dict_to_add[key].items():
                    final_dict[key][key_to_update] = value
            else:
                final_dict.pop(key)
    else:
        final_dict.update(dict_to_add)

    return final_dict


def split_missreading(string):
    split = re.split("\t ", string)
    return split


def split_dimensions(rules):
    for rule in rules:
        rules[rule]['atd_dimension'] = split_missreading(rules[rule]['atd_dimension'])
    return rules


def merge_crawled_files(directory, prefix, suffix, field, target_file, save_step):
    print('Start merging files...')

    items = list()
    counter = 1

    dir_contents = os.listdir(directory)
    total = str(len(dir_contents))

    for f in dir_contents:
        print('Merging file ' + str(counter) + '/' + total)
        counter += 1
        filename = f
        if filename.startswith(prefix) and filename.endswith(suffix):
            file_contents = json.load(open(os.path.join(directory, filename), 'r'))
            if field in file_contents:
                items_in_file = file_contents[field]
                items.extend(items_in_file)

    merged_items = {}
    for p in items:
        merged_items[p['key']] = p

    if save_step:
        save(target_file, merged_items)
    return merged_items

def get_dimension_list(triple):
    dimensions_with_rules = {}

    for rule in triple:
        dimensions_list = rule['dimensions']
        rule_name = rule['rule']

        for dimension_element in dimensions_list:
            if dimension_element not in dimensions_with_rules:
                dimensions_with_rules[dimension_element] = [rule_name]
                continue
            dimensions_with_rules[dimension_element].append(rule_name)

    return dimensions_with_rules


def read_dataset_csv():
    object_to_return = {}
    with open('../data/apache_ATDx_input.csv', mode='r') as file:
        csv_file = csv.DictReader(file)
        for rule in csv_file:
            object_to_return[rule['projectKey']] = dict(rule)
    return object_to_return


def read_rules_csv():
    object_to_return = {}
    with open('../data/ar_rules.csv', mode='r') as file:
        csv_file = csv.DictReader(file)
        for rule in csv_file:
            object_to_return[rule['id']] = dict(rule)
    return object_to_return


def save_dict_as_json(file_path, data):
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile, indent=4, default=str)


def read_json(path):
    f = open(path, )
    dictionary = json.load(f)

    return dictionary


def from_csv_to_json():
    ar_rules = read_rules_csv()
    sua = read_dataset_csv()

    out_file = open('../data/ar_rules.json','w+')
    json.dump(ar_rules, out_file, indent=4, default=str)

    out_file = open('../data/apache_ATDx_input.json','w+')
    json.dump(sua, out_file, indent=4, default=str)
