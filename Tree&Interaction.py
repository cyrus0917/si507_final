import json
import copy
import tabulate
import pandas as pd
import numpy as np
import seaborn as sns

lego_file = open('result_Lego.json', 'r')
cache_lego_contents = lego_file.read()
lego_cache = json.loads(cache_lego_contents)

Tree_Age = ('Are you looking for the products designed for the 1.5+ years old?',
            ('Are you looking for the products designed for the 4+ years old?',
             ('Are you looking for the products designed for the 6+ years old?',
              ('Are you looking for the products designed for the 9+ years old?',
               ('Are you looking for the products designed for the 13+ years old?',
                ('Are you looking for the products designed for the 18+ years old?',
                '',(lego_cache['age-18-plus-years'], None, None)),
                (lego_cache['age-13-plus-years'], None, None)),
               (lego_cache['age-9-plus-years'], None, None)),
              (lego_cache['age-6-plus-years'], None, None)),
             (lego_cache['age-4-plus-years'], None, None)),
            (lego_cache['age-1-plus-years'], None, None))

def notAnswer(tree):
    if type(tree[0]) is str and tree[1] is not None and tree[2] is not None:
        return True
    else:
        return False

def isAnswer(tree):
    try:
        if type(tree[0]) is list and tree[1] is None and tree[2] is None:
            return True
        else:
            return False
    except:
        return True


def yes(prompt):
    proper_answer = ['y', 'yes', 'yeah', 'yup', 'sure']
    answer_input = input(prompt)
    if answer_input.lower() in proper_answer:
        return True
    else:
        return False

def playAnswer(tree):
    return yes(tree[0])

def play_age_tree(tree):
    if notAnswer(tree):
        if playAnswer(tree):
            print('Please tell me more about your prefernece!')
            return play_age_tree(tree[2])

        else:
            try:
                return play_age_tree(tree[1])
            except:
                print('There is no appropriate products options for you!')

    else:
        return tree[0]


def saveTree(tree, lego_tree_File):
    if isAnswer(tree):
        print('Leaf', file=lego_tree_File)
        try:
            print(tree[0], file=lego_tree_File)
        except:
            print(tree, file=lego_tree_File)

    else:
            print('Internal Node', file=lego_tree_File)
            print(tree[0], file=lego_tree_File)
            try:
                saveTree(tree[1], lego_tree_File)
            except:
                pass
            saveTree(tree[2], lego_tree_File)
        

write_document = open('lego_tree.json', 'w')
saveTree(Tree_Age, write_document)

def loadTree(treeFile):
    first_line = treeFile.readline()
    second_line = treeFile.readline()
    if first_line.strip() == "Internal node":
        return (second_line.strip(), loadTree(treeFile), loadTree(treeFile))

    elif first_line.strip() == "Leaf":
        return (second_line.strip(), None, None)


def expectation_rating():
    while True:
        expected_rating = input('Please enter the lowest rating you can accept and all products above this rating will be filtered out. The maximum rating is 5 points.')
        try:
            expected_rating = float(expected_rating)
            return expected_rating
        except:
            continue

def expectation_price():
    while True:
        expected_price_min = input("Please input the lowest price you'd like to set, please keep two decimals")
        expected_price_max = input('Please input the highest price you can accept for the toy, please keep two decimals')
        try:
            expected_price_min = float(expected_price_min)
            expected_price_max = float(expected_price_max)
            return (expected_price_min, expected_price_max)
        except:
            continue

def expectation_pieces():
    while True:
        expected_pieces = input('How many pieces of toys would you like to have, the suitable toys would be recommended to you, please input integer')
        try:
            expected_pieces = int(expected_pieces)
            return expected_pieces
        except:
            continue

def expectation_status():
    expected_status = input('Would you like to only focus on the products availble now?')
    return expected_status 

def filter_out(objective, objective_rating, objective_price, objective_pieces, expected_rating, expected_price_min, expected_price_max, expected_pieces, expected_status):
    if objective_rating >= expected_rating:
        if expected_price_min <= objective_price <= expected_price_max:
            if expected_pieces-200 <= objective_pieces <= expected_pieces+200:
                if expected_status in ['y', 'yes', 'yeah', 'yup', 'sure']:
                    if objective['Status'] == 'Available now':
                        return True
                else:
                    return True

def tabulate_list(list):
    list1 = copy.deepcopy(list)
    list2 = copy.deepcopy(list)
    for items in list1:
        del items['URL']
        if items['Name'].isalpha():
            items['Name'] = items['Name'].strip()
        else:
            items_name = ''
            for word in items['Name']:
                if word.isalpha() or word == ' ':
                    items_name += word
            items['Name'] = items_name
                
    dataset = list1
    header = dataset[0].keys()
    rows = [x.values() for x in dataset]
    print('Wish the following results would help you sort out the perfect Lego toys!')
    print(tabulate.tabulate(rows, header, tablefmt='grid'))
    guide_answer = input('Would you like to see the url, which guides you to the page of products?')
    if guide_answer in ['y', 'yes', 'yeah', 'yup', 'sure']:
        for item in list2:
            del item['Rating']
            del item['Status']
            del item['Pieces']
            if item['Name'].isalpha():
                item['Name'] = item['Name'].strip()
            else:
                item_name = ''
                for word in item['Name']:
                    if word.isalpha() or word == ' ':
                        item_name += word
                item['Name'] = item_name
        dataset1 = list2
        header1 = dataset1[0].keys()
        rows1 = [x.values() for x in dataset1]
        print('The URLs are as follows:')
        print(tabulate.tabulate(rows1, header1, tablefmt='grid'))
    else:
        print('Thank you for supporting Lego!')


def main():

    recommendation = []
    product_under_age = play_age_tree(Tree_Age)
    expected_rating = expectation_rating()
    expected_price_min, expected_price_max = expectation_price()
    expected_pieces = expectation_pieces()
    expected_status = expectation_status()
    # print(product_under_age)#A big list full of dictionary
    for items in product_under_age:
        rating = items['Rating'][:-2]
        try:
            if len(rating)>1:
                rating = float(rating)
            else:
                rating = int(rating)
        except:
            rating = 0

        try:
            price = float(items['Price'][1:])
        except:
            price = 0

        try:
            pieces = int(items['Pieces'])
        except:
            pieces = 0

        if filter_out(items, rating, price, pieces, expected_rating, expected_price_min, expected_price_max, expected_pieces, expected_status) == True:
            recommendation.append(items)
    if recommendation == []:
        print('There is no appropriate products options for you!')
    else:
        tabulate_list(recommendation)


if __name__ == '__main__':
    main()
