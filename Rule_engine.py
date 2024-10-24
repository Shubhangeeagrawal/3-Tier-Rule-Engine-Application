#!/usr/bin/env python
# coding: utf-8

# In[22]:


import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY,
                rule_text TEXT NOT NULL
            );
        """)
        self.conn.commit()

    def save_rule(self, rule_text):
        self.cursor.execute("INSERT INTO rules (rule_text) VALUES (?)", (rule_text,))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_rule(self, rule_id):
        self.cursor.execute("SELECT rule_text FROM rules WHERE id = ?", (rule_id,))
        return self.cursor.fetchone()


# In[23]:


def create_rule(self, rule_string: str) -> int:
    ast = self.parse(rule_string)
    rule_id = self.database.save_rule(rule_string)
    return rule_id


# In[24]:


def combine_rules(self, rules: List[str]) -> int:
    combined_ast = None
    for rule in rules:
        ast = self.create_rule(rule)
        if combined_ast is None:
            combined_ast = ast
        else:
            combined_ast = Node(NodeType.OPERATOR, Operator.AND, left=combined_ast, right=ast)
    combined_rule_text = str(combined_ast)
    combined_rule_id = self.database.save_rule(combined_rule_text)
    return combined_rule_id


# In[26]:


def evaluate_rule(self, rule_id: int, data: Dict[str, Union[str, int]]) -> bool:
    rule_text = self.database.get_rule(rule_id)
    ast = self.create_rule(rule_text)
    return self.evaluate_ast(ast, data)

def evaluate_ast(self, ast: Node, data: Dict[str, Union[str, int]]) -> bool:
    if ast.type == NodeType.OPERAND:
        attribute, operator, value = self.parse_operand(ast.value)
        if operator == Operator.EQ:
            return str(data.get(attribute)) == value
        elif operator == Operator.LT:
            return float(data.get(attribute)) < float(value)
        elif operator == Operator.GT:
            return float(data.get(attribute)) > float(value)
    elif ast.type == NodeType.OPERATOR:
        left_result = self.evaluate_rule(ast.left, data)
        right_result = self.evaluate_rule(ast.right, data)
        if ast.operator == Operator.AND:
            return left_result and right_result
        elif ast.operator == Operator.OR:
            return left_result or right_result


# In[30]:


from enum import Enum
from typing import Optional, Dict, List, Union
import re
import sqlite3

class NodeType(Enum):
    OPERATOR = 'operator'
    OPERAND = 'operand'

class Operator(Enum):
    AND = 'AND'
    OR = 'OR'
    EQ = '=='
    LT = '<'
    GT = '>'

class Node:
    def __init__(self, node_type: NodeType, operator: Optional[Operator] = None, value: Optional[str] = None, left: Optional['Node'] = None, right: Optional['Node'] = None):
        self.type = node_type
        self.operator = operator
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        if self.type == NodeType.OPERAND:
            return f"{self.value}"
        elif self.type == NodeType.OPERATOR:
            return f"({self.left} {self.operator.value} {self.right})"

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY,
                rule_text TEXT NOT NULL
            );
        """)
        self.conn.commit()

    def save_rule(self, rule_text):
        self.cursor.execute("INSERT INTO rules (rule_text) VALUES (?)", (rule_text,))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_rule(self, rule_id):
        self.cursor.execute("SELECT rule_text FROM rules WHERE id = ?", (rule_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None  # Return the rule text or None if not found
    
class RuleEngine:
    def __init__(self):
        self.database = Database('rules.db')

    def create_rule(self, rule_string: str) -> int:
        tokens = self.tokenize(rule_string)
        parser = self.Parser(tokens)
        ast = parser.parse_expression()
        rule_id = self.database.save_rule(rule_string)
        return rule_id

    def combine_rules(self, rules: List[str]) -> int:
        combined_rule_text = " AND ".join(rules)
        combined_rule_text = f"({combined_rule_text})"
        combined_rule_id = self.create_rule(combined_rule_text)
        return combined_rule_id 
    
    def evaluate_rule(self, rule_id: int, data: Dict[str, Union[str, int]]) -> bool:
        rule_text = self.database.get_rule(rule_id)
        if rule_text is None:
            raise ValueError(f"No rule found with id {rule_id}")
        tokens = self.tokenize(rule_text)
        parser = self.Parser(tokens)
        ast = parser.parse_expression()
        return self.evaluate_ast(ast, data)
    
    def evaluate_ast(self, ast: Node, data: Dict[str, Union[str, int]]) -> bool:
        if ast.type == NodeType.OPERAND:
            attribute, operator, value = self.parse_operand(ast.value)
            if operator == Operator.EQ:
                return str(data.get(attribute)) == value
            elif operator == Operator.LT:
                return float(data.get(attribute)) < float(value)
            elif operator == Operator.GT:
                return float(data.get(attribute)) > float(value)
        elif ast.type == NodeType.OPERATOR:
            left_result = self.evaluate_ast(ast.left, data)
            right_result = self.evaluate_ast(ast.right, data)
            if ast.operator == Operator.AND:
                return left_result and right_result
            elif ast.operator == Operator.OR:
                return left_result or right_result

    def tokenize(self, rule_string: str) -> List[str]:
        tokens = re.findall(r'$$|$$|AND|OR|>=|<=|>|<|==|[^\s()]+', rule_string)
        return tokens

    class Parser:
        def __init__(self, tokens):
            self.tokens = tokens
            self.current = 0

        def parse_expression(self):
            left = self.parse_term()
            while self.current < len(self.tokens) and self.tokens[self.current] in ['AND', 'OR']:
                operator = Operator[self.tokens[self.current]]
                self.current += 1
                right = self.parse_term()
                left = Node(NodeType.OPERATOR, operator, left=left, right=right)
            return left

        def parse_term(self):
            if self.tokens[self.current] == '(':
                self.current += 1
                node = self.parse_expression()
                if self.current < len(self.tokens) and self.tokens[self.current] == ')':
                    self.current += 1
                    return node
                else:
                    raise Exception("Unmatched opening parenthesis")
            else:
                operand = []
                while self.current < len(self.tokens) and self.tokens[self.current] not in ['AND', 'OR', ')', '(']:
                    operand.append(self.tokens[self.current])
                    self.current += 1
                return Node(NodeType.OPERAND, value=' '.join(operand))

    def parse_operand(self, operand: str) -> (str, Operator, str):
        match = re.match(r'(\w+)\s*(==|<|>)\s*(.+)', operand)
        if match:
            attribute = match.group(1)
            operator = Operator(match.group(2))
            value = match.group(3).strip()
            return attribute, operator, value
        else:
            raise Exception("Invalid operand syntax")

# Example usage
rule_engine = RuleEngine()

# Create individual rules
rule1 = "(age > 30 AND department == Sales) OR (age < 25 AND department == Marketing)"
rule2 = "(age > 30 AND department == Marketing)"

# Combine rules
combined_rule_id = rule_engine.combine_rules([rule1, rule2])

# Test data
data1 = {"age": 35, "department": "Sales"}
data2 = {"age": 28, "department": "Marketing"}

# Evaluate combined rule
result1 = rule_engine.evaluate_rule(combined_rule_id, data1)
result2 = rule_engine.evaluate_rule(combined_rule_id, data2)

print(f"Result for data1: {result1}")  # Should print: Result for data1: True
print(f"Result for data2: {result2}")  # Should print: Result for data2: False


# In[ ]:


from flask import Flask, request, jsonify

app = Flask(__name__)

rule_engine = RuleEngine()

@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_string = request.json['rule']
    rule_id = rule_engine.create_rule(rule_string)
    return jsonify({'rule_id': rule_id})

@app.route('/combine_rules', methods=['POST'])
def combine_rules():
    rules = request.json['rules']
    combined_rule_id = rule_engine.combine_rules(rules)
    return jsonify({'combined_rule_id': combined_rule_id})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    rule_id = request.json['rule_id']
    data = request.json['data']
    result = rule_engine.evaluate_rule(rule_id, data)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)

