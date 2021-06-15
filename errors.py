import os
import logging
import json
import validators
import urllib


def check_name_company(name: str) -> bool:
    '''check function of name_company'''
    if len(name) == 0:
        raise Exception('Company name cannot be empty')
    if name.isdigit():
        raise Exception('Company name cannot contain only numbers')
    if validators.url(name):
        raise Exception('Comapany name cannot be URL')
    return True


def check_official_link(official_link: str) -> bool:
    '''check function of offical link company'''
    if not validators.url(official_link):
        raise Exception('Incorrect official site URL')
    return True


def check_num_results(num: str) -> bool:
    '''check function num results'''
    if not num.isdigit():
        raise Exception('The number of search results is incorrect')
    if int(num) < 0:
        raise Exception('The number of search result can\'t be than less 0')
    return True


def check_choose_searches(choose_str: str) -> bool:
    '''check function choose searches'''
    correct_numbers = ['1', '2', '3']
    choose_str = choose_str.split(' ')
    for choose in choose_str:
        if not choose.isdigit():
            raise Exception(f"{choose} is not number of search engine")
        if not choose in correct_numbers:
            raise Exception(f"{choose} is not exists number search engine")
    return True


def check_query_patterns(filepath: str) -> bool:
    '''check function query patterns'''
    with open(filepath, 'r') as file:
        try:
            query_json = json.load(file)
        except json.decoder.JSONDecodeError as json_exception:
            raise Exception("Invalid JSON") from json_exception
        else:
            if len(query_json) > 1:
                raise Exception('The number of keys in the configuration'
                                ' file cannot be more than 1 key \"queries\"')
            if len(query_json) < 1:
                raise Exception('No fields in configuration query patterns')
        queries: str = query_json['queries']
        for now_query in queries:
            if now_query.find('{}') < 0:
                raise Exception(f"Query \"{now_query}\" missing brackets " + "{}")
    return True


def check_deep(search_deep: int) -> bool:
    '''check function deep'''
    if not str(search_deep).isdigit():
        raise Exception('The deep is incorrect')
    if search_deep < 0:
        raise Exception('The deep can\'t be than less or equal 0')
    return True


def check_network() -> bool:
    '''check the internet'''

    try:
        urllib.request.urlopen('http://google.com', timeout=10)
        logging.fatal("internet on")
        return True
    except:
        logging.fatal("internet off")
        return False


def check_tor_network() -> bool:
    '''check the tor service'''
    status = os.system('systemctl is-active --quiet tor')
    logging.fatal(f"tor network status {status}")
    return status == 0
