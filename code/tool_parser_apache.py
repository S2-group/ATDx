import csv
import json


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


def save_dict_as_json(dict, path):
    out_file = open(path, 'w+')
    json.dump(dict, out_file)


def read_json(path):
    f = open(path, )

    dictionary = json.load(f)

    return dictionary


def from_csv_to_json():
    ar_rules = read_rules_csv()
    sua = read_dataset_csv()

    out_file = open('../data/ar_rules.json','w+')
    json.dump(ar_rules,out_file)

    out_file = open('../data/apache_ATDx_input.json','w+')
    json.dump(sua,out_file)