import re


def update_dict_of_dict(dict_to_update, dict_to_add):
    if dict_to_update:
        for key in dict_to_add:
            for key_to_update, value in dict_to_add[key].items():
                dict_to_update[key][key_to_update] = value
    else:
        dict_to_update.update(dict_to_add)
    pass


def split_missreading(string):
    split = re.split("\t ", string)
    return split


def split_dimensions(rules):
    for rule in rules:
        rules[rule]['atd_dimension'] = split_missreading(rules[rule]['atd_dimension'])
    return rules
