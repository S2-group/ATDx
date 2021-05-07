from tool_parser_apache import *
from util import *
import numpy as np
import ckwrap as ck


def get_dimensions(sua, atdd_tool, dimensions, rule_dimensions, ar_kmeans):
    """
    get_dimensions function that returns an array with the normalized values

    :param sua: iterable with the name of the projects
    :param atdd_tool: it is a dictionary containing the amount of rules per dimension. It's keys are the dimensions
    :param dimensions: it has the current of each project ATDD value
    :param rule_dimensions: it contains the key of the current Dimension
    :param ar_kmeans: it's content refers to NORM^t
    """
    for rule_dimension in rule_dimensions:
        for label, project_name in zip(ar_kmeans.labels, sua):
            if max(ar_kmeans.labels) - min(ar_kmeans.labels) == 0:
                break
            else:
                severity = (5 * ar_kmeans.centers[label] - (min(ar_kmeans.labels))) / (max(ar_kmeans.labels) - min(ar_kmeans.labels))
                dimensions[rule_dimension][project_name] = dimensions[rule_dimension][project_name] + severity

    return dimensions, atdd_tool


def norm_calculator1(data_set, gr_level, rule):
    """
    norm_calculator1 function that returns an array with the normalized values

    :param data_set: dictionary of the
    :param rule: key of the rule referring a rule existing in the dataset
    :param gr_level: key for the granularity level a rule existing in the dataset
    """
    norm = []
    for project in data_set:
        norm.append(int(data_set[project][rule]) / int(data_set[project][gr_level]))
    return norm


def atdd_from_set_of_rules(set_of_rules):
    """
    atdd_from_set_of_rules function used to get the atdd dictionary with the key as the dimension and the number of rules
    as the content

    :param set_of_rules: it is a dictionary of a dictionary containing the keys of the 3-tuple
    :return it returns a tuple of the dimensions and the atdx given as a dictionary with the projects as key
    """
    atdd = {}
    for rule in set_of_rules:
        for key in set_of_rules[rule]['atd_dimension']:
            if key in atdd:
                atdd[key] = atdd[key] + 1
            else:
                atdd[key] = 1
    return atdd


def atdx_core(sua, ar_tool, atdd_tool, norm_t=None):
    """
    atdx_core function used to calculate the adtx of a given set of projects

    :param sua: it is a dictionary of a dictionary containing the 3-tuple for each project as first key
    :param ar_tool: it is a dictionary of a dictionary containing the keys of the 3-tuple.
    :param atdd_tool: it is a dictionary containing the amount of rules per dimension. It's keys are the dimensions
    :param norm_t: it is an array containing the normalized values of the dataset. If this variable is not added, it means it's the first atdx analysis, otherwise the functions will use this variable to calculate the adtx
    :return it returns a tuple of the dimensions and the atdx given as a dictionary with the projects as key
    """
    dimensions = {}
    atdx = {}
    normalized_updated = {}
    # initialization of the atd dimensions. We initialize them all to 0 (it can happen that sua is a dictionary of
    # projects) the same happens with the atdx
    for dimension in atdd_tool:
        dimensions[dimension] = {}
        for project_name in sua:
            atdx[project_name] = 0
            dimensions[dimension][project_name] = 0

    # We check all of the rules, the norm value and we do the severity calculation
    for rule in ar_tool:
        gr_level = ar_tool[rule]['granularity_level']
        rule_dimensions = ar_tool[rule]['atd_dimension']
        if norm_t is None:
            # norm_calculator returns an array of the norm values of the sua
            # in this case, as there is no input on nom_t (it is the first run, we would only calculate it)
            normalized_updated[rule] = norm_calculator1(sua, gr_level, rule)
        else:
            # in this case, we append the return values to the norm_t of the input to calculate it together
            normalized_updated[rule] = norm_t[rule]
            normalized_updated[rule].extend(norm_calculator1(sua, gr_level, rule))
        # Calculation of severeness and storing adding to the dimensions
        num_clusters = min(len(np.unique(normalized_updated[rule])), 6)
        ar_kmeans = ck.ckmeans(normalized_updated[rule], k=(1, num_clusters))
        dimensions, atdd_tool = get_dimensions(sua, atdd_tool, dimensions, rule_dimensions, ar_kmeans)

    # calculation of atdx per project in sua
    for dimension in dimensions:
        for project_name in sua:
            value = dimensions[dimension][project_name] / atdd_tool[dimension]
            atdx[project_name] = atdx[project_name] + value

    # final step of atdx
    for project_name in sua:
        atdx[project_name] = atdx[project_name] / len(atdd_tool)

    return dimensions, atdx, normalized_updated


ar_rules = read_json('../data/ar_rules.json')
ar_rules = split_dimensions(ar_rules)
project_dataset = read_json('../data/apache_ATDx_input.json')

atdd = atdd_from_set_of_rules(ar_rules)

dimensions_t, atdx, norm = atdx_core(project_dataset, ar_rules, atdd)

print(atdx)
dimensions_t, atdx, norm = atdx_core(project_dataset, ar_rules, atdd,norm )

print (atdx)