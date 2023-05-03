class KnowledgeBase:
    def __init__(self):
        self.facts = []
        self.rules = []

    def add(self, item):
        if isinstance(item, Fact):
            self._add_logical_fact(item)
        elif isinstance(item, Rule):
            self._add_logical_rule(item)

    def _add_logical_fact(self, fact):
        if fact not in self.facts:
            self.facts.append(fact)
            self._derive_facts_from_rules(fact)
        else:
            self._update_fact_dependencies(fact)

    def _add_logical_rule(self, rule):
        if rule not in self.rules:
            self.rules.append(rule)
            self._derive_facts_from_rule(rule)
        else:
            self._update_rule_dependencies(rule)

    def _derive_facts_from_rules(self, fact):
        for rule in self.rules:
            self.derive(fact, rule)

    def _update_fact_dependencies(self, fact):
        index = self.facts.index(fact)
        if fact.relies_on:
            for f in fact.relies_on:
                self.facts[index].relies_on.append(f)
        else:
            self.facts[index].asserted = True

    def _derive_facts_from_rule(self, rule):
        for fact in self.facts:
            self.derive(fact, rule)

    def _update_rule_dependencies(self, rule):
        index = self.rules.index(rule)
        if rule.relies_on:
            for f in rule.relies_on:
                self.rules[index].relies_on.append(f)
        else:
            self.rules[index].asserted = True

    def query(self, fact):
        if isinstance(fact, Fact):
            f = Fact(fact.predicate)
            bindings_lst = []
            for fact in self.facts:
                binding = match(f.predicate, fact.predicate)
                if binding:
                    bindings_lst.append(binding)

            return bindings_lst

        else:
            print("Invalid question:", fact.predicate)
            return []

    def derive(self, fact, rule):
        bindings = match(rule.lhs[0], fact.predicate)
        if not bindings:
            return None

        if len(rule.lhs) == 1:
            new_fact = Fact(instantiate(rule.rhs, bindings), [[rule, fact]])
            rule.relied_facts.append(new_fact)
            fact.relied_facts.append(new_fact)
            self.add(new_fact)
        else:
            local_lhs = [instantiate(rule.lhs[i], bindings) for i in range(1, len(rule.lhs))]
            local_rhs = instantiate(rule.rhs, bindings)
            new_rule = Rule([local_lhs, local_rhs], [[rule, fact]])
            rule.relied_rules.append(new_rule)
            fact.relied_rules.append(new_rule)
            self.add(new_rule)

class Rule:
    def __init__(self, rule, relies_on=None):
        super(Rule, self).__init__()

        if relies_on is None:
            relies_on = []

        # The rule is provided in the form of a list of predicates, separated by an `&` operation
        self.lhs = [p if isinstance(p, Predicate) else Predicate(p) for p in rule[0]]

        # The right side is the predicate that is derived from the rule
        self.rhs = rule[1] if isinstance(rule[1], Predicate) else Predicate(rule[1])
        self.asserted = not relies_on
        self.relies_on = []
        self.relied_facts = []
        self.relied_rules = []
        for pair in relies_on:
            self.relies_on.append(pair)

class Fact:
    def __init__(self, predicate, relies_on=None):
        self.predicate = self._ensure_predicate_instance(predicate)
        self.asserted = not relies_on
        self.relies_on = relies_on or []
        self.relied_facts = []
        self.relied_rules = []

    def __eq__(self, other):
        return isinstance(other, Fact) and self.predicate == other.predicate

    @staticmethod
    def _ensure_predicate_instance(predicate):
        return predicate if isinstance(predicate, Predicate) else Predicate(predicate)


class Predicate:
    def __init__(self, predicates_list=None):
        self.predicate = ""
        self.terms = []

        if predicates_list:
            self._initialize_terms_and_predicate(predicates_list)

    def __eq__(self, other):
        return (self.predicate == other.predicate
                and all(st == ot for st, ot in zip(self.terms, other.terms)))

    def _initialize_terms_and_predicate(self, predicates_list):
        self.predicate = predicates_list[0]
        self.terms = [self._ensure_term_instance(t) for t in predicates_list[1:]]

    @staticmethod
    def _ensure_term_instance(term):
        return term if isinstance(term, Term) else Term(term)

class Term:
    def __init__(self, term):
        super(Term, self).__init__()
        # Term is either a variable or a constant
        is_var_or_value = isinstance(term, Variable) or isinstance(term, Constant)
        self.term = term if is_var_or_value else (Variable(term) if Variable.is_variable(term) else Constant(term))

    def __eq__(self, other):
        return (self is other
                or isinstance(other, Term) and self.term.element == other.term.element
                or ((isinstance(other, Variable) or isinstance(other, Constant))
                    and self.term.element == other.element))


class Variable:
    def __init__(self, element):
        self.term = None
        self.element = element

    def __eq__(self, other):
        return (self is other
                or isinstance(other, Term) and self.term.element == other.term.element
                or ((isinstance(other, Variable) or isinstance(other, Constant))
                    and self.term.element == other.element))

    @staticmethod
    def is_variable(var):
        if type(var) == str:
            return var[0] == '?'
        if isinstance(var, Term):
            return isinstance(var.term, Variable)

        return isinstance(var, Variable)


class Constant:
    def __init__(self, element):
        self.term = None
        self.element = element

    def __eq__(self, other):
        return (self is other
                or isinstance(other, Term) and self.term.element == other.term.element
                or ((isinstance(other, Variable) or isinstance(other, Constant))
                    and self.term.element == other.element))


# Struct used to build assignments for quering the knowledge base
class Assignment:
    def __init__(self, variable, value):
        super(Assignment, self).__init__()
        self.variable = variable
        self.value = value

    def __str__(self):
        return self.variable.element + " : " + self.value.element


class Assignments:
    def __init__(self):
        self.assignments = []
        self.mapping = {}

    def __str__(self):
        if not self.assignments:
            return ''
        return ", ".join((str(binding) for binding in self.assignments))

    def __getitem__(self, key):
        return self.mapping[key] if (self.mapping and key in self.mapping) else None

    def assign(self, variable, value):
        self.mapping[variable.element] = value.element
        self.assignments.append(Assignment(variable, value))

    def is_assigned_to(self, variable):
        if variable.element in self.mapping.keys():
            value = self.mapping[variable.element]
            if value:
                return Variable(value) if Variable.is_variable(value) else Constant(value)
        return False

    def test_and_bind(self, variable_term, value_term):
        bound = self.is_assigned_to(variable_term.term)
        if bound:
            return value_term.term == bound

        self.assign(variable_term.term, value_term.term)
        return True


def match(state1, state2, bindings=None):
    if len(state1.terms) != len(state2.terms) or state1.predicate != state2.predicate:
        return False
    if not bindings:
        bindings = Assignments()
    return match_recursive(state1.terms, state2.terms, bindings)


def match_recursive(terms1, terms2, bindings):
    if len(terms1) == 0:
        return bindings
    if Variable.is_variable(terms1[0]):
        if not bindings.test_and_bind(terms1[0], terms2[0]):
            return False
    elif Variable.is_variable(terms2[0]):
        if not bindings.test_and_bind(terms2[0], terms1[0]):
            return False
    elif terms1[0] != terms2[0]:
        return False
    return match_recursive(terms1[1:], terms2[1:], bindings)


def instantiate(statement, bindings):
    def handle_term(term):
        if Variable.is_variable(term):
            bound_value = bindings.is_assigned_to(term.term)
            return Term(bound_value) if bound_value else term
        else:
            return term

    new_terms = [handle_term(t) for t in statement.terms]
    return Predicate([statement.predicate] + new_terms)