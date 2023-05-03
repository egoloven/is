from reader import *
from knowledgebase import *

def main():
    knowledge_base = KnowledgeBase()
    pre_knowledge = parse_input_files()

    for item in pre_knowledge:
        knowledge_base.add(item)

    while True:
        line = input()

        if line.startswith('rule '):
            process_rule_line(knowledge_base, line[5:])
        elif line.startswith('fact '):
            process_fact_line(knowledge_base, line[5:])
        elif line.startswith('query '):
            process_query_line(knowledge_base, line[6:])
        elif line.startswith('quit'):
            break
        else:
            print('Invalid input. It may be a fact, rule or query.')


def process_rule_line(knowledge_base, line):
    rule = parse_rule_line(line)
    knowledge_base.add(rule)


def process_fact_line(knowledge_base, line):
    fact = parse_fact_line(line)
    knowledge_base.add(fact)


def process_query_line(knowledge_base, line):
    fact = parse_fact_line(line)
    bindings = knowledge_base.query(fact)

    if bindings:
        for binding in bindings:
            print('True: ' + str(binding))
    else:
        print('False')


if __name__ == "__main__":
    main()