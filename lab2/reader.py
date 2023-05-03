from knowledgebase import *

def parse_input_files():
    facts, rules = parse_fact_file(), parse_rule_file()
    output = []
    for f in facts:
        output.append(f)
    for r in rules:
        output.append(r)
    return output

def parse_fact_file():
    with open('data/facts', 'r') as file:
        return [parse_fact_line(line) for line in file]

def parse_fact_line(fact):
    return Fact(fact.rstrip().strip().split())

def parse_rule_file():
    with open('data/rules', 'r') as file:
        lines = [line.rstrip() for line in file]
        rules = []
        for line in lines:
            r = line.split('->')
            rhs = r[1].rstrip().strip().split()
            lhs = r[0].split('&')
            lhs = map(lambda x: x.rstrip().strip().split(), lhs)
            rules.append(parse_rule(lhs, rhs))
        return rules

def parse_rule_line(line):
    r = line.split('->')
    rhs = r[1].rstrip().strip().split()
    lhs = r[0].split('&')
    lhs = map(lambda x: x.rstrip().strip().split(), lhs)
    return parse_rule(lhs, rhs)


def parse_rule(lhs, rhs):
    return Rule([[list(map(lambda x: x.strip(), c)) for c in lhs], rhs])