from scanner import Token,Scanner_analys,Token_Type
import sys

class ExprNode:
    def __init__(self, type, value=None, operator=None, func_name=None,children=None):
        self.type = type    #值,运算符号,函数名
        self.value = value
        self.operator = operator
        self.func_name = func_name
        self.children = children if children is not None else [] #如果children为空的话children将初始化为空列表

    def add_child(self, child):
        self.children.append(child)

    def display(self, level=0):
        indent = "  " * level
        print(f"{indent}{self.type}", end="")

        if self.type == "value":
            print(f": {self.value}")
        elif self.type == "operator":
            print(f": {self.operator}")
        elif self.type == "func":
            print(f": {self.func_name}")

        if len(self.children) == 1:
            print(f"{indent} -> Child:")
            self.children[0].display(level + 1)
        elif len(self.children) == 2:
            print(f"{indent} -> Left Child:")
            self.children[0].display(level + 1)
            print(f"{indent} -> Right Child:")
            self.children[1].display(level + 1)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = -1
        self.root = None

    def parse(self):
        self.current_token = self.get_next_token()
        print("语法分析开始!!!")
        print("enter in  program")
        while self.current_token.type != Token_Type.NONTOKEN:
            self.statement()
            #匹配statement文法
            self.match("SEMICO")
        print("exit from program")
        print("语法分析结束!!!")
        
    def get_next_token(self):
        #经过词法分析后tokens的最后一个token类型固定为NONTOKEN
        self.index += 1
        self.current_token = self.tokens[self.index]
        return self.current_token



    def match(self, expected_type):
        if self.current_token.type.name == expected_type:
            print(f"matchtoken  {expected_type}")
            self.get_next_token()
        else:
            raise SyntaxError(f"current_token_index: {self.index} Unexpected token: {self.current_token.type.name}")


    def statement(self):
        print("enter in  statement")
        if self.current_token.type.name == "ORIGIN":
            self.origin_statement()
        elif self.current_token.type.name == "SCALE":
            self.scale_statement()
        elif self.current_token.type.name == "ROT":
            self.rot_statement()
        elif self.current_token.type.name == "FOR":
            self.for_statement()
        else:
            raise SyntaxError(f"current_token_index: {self.index} Unexpected token: {self.current_token.type.name}")
        print("exit from  statement")

    def origin_statement(self):
        print("enter in origin_statement")
        self.match("ORIGIN")
        self.match("IS")
        self.match("L_BRACKET")
        self.expression()
        self.match("COMMA")
        self.expression()
        self.match("R_BRACKET")
        print("exit from origin_statement")



    def scale_statement(self):
        print("enter in scale_statement")
        self.match("SCALE")
        self.match("IS")
        self.match("L_BRACKET")
        self.expression()
        self.match("COMMA")
        self.expression()
        self.match("R_BRACKET")
        print("exit from scale_statement")


    def rot_statement(self):
        self.match("ROT")
        self.match("IS")
        self.expression()


    def for_statement(self):
        self.match("FOR")
        self.match("T")
        self.match("FROM")
        self.expression()
        self.match("TO")
        self.expression()
        self.match("STEP")
        self.expression()
        self.match("DRAW")
        self.match("L_BRACKET")
        self.expression()
        self.match("COMMA")
        self.expression()
        self.match("R_BRACKET")


    def expression(self):
        # Expression → Term { ( PLUS | MINUS ) Term }
        print("enter in  expression")
        expr_node = self.term()

        while self.current_token.type.name in ["PLUS", "MINUS"]:
            if self.current_token.type.name == "PLUS":
                operator = "+"
            else:
                operator = "-"
            self.get_next_token()
            term_node = self.term()

            expr_node = ExprNode(type="operator", operator=operator, children=[expr_node, term_node])

        expr_node.display()
        print("exit from  expression")
        return expr_node


    def term(self):
        # Term → Factor { ( MUL | DIV ) Factor }
        term_node = self.factor()

        while self.current_token.type.name in ["MUL", "DIV"]:
            if self.current_token.type.name == "MUL":
                operator = "*"
            else:
                operator = "/"
            self.get_next_token()
            factor_node = self.factor()

            term_node = ExprNode(type="operator", operator=operator, children=[term_node, factor_node])

        return term_node


    def factor(self):
        # Factor → ( PLUS | MINUS ) Factor | Component
        if self.current_token.type.name == "PLUS":
            self.get_next_token()# 遇到一元运算符+时,直接跳过+号
            factor_node = self.factor()
        elif self.current_token.type.name == "MINUS":
            # 遇到减号时将'-'建成factor节点,然后get_next_token(),后将0.0放入第一个节点,后边的value放入第二个节点
            factor_node = ExprNode(type="operator",operator="-")
            self.get_next_token()
            tmp_node1 = ExprNode(type="value",value=0.0)
            tmp_node2 = self.factor()
            factor_node.add_child(tmp_node1)
            factor_node.add_child(tmp_node2)

        else:
            factor_node = self.component()

        return factor_node

    def component(self):
        # Component → Atom [ POWER Component ]
        atom_node = self.atom()

        if self.current_token.type.name == "POWER":
            component_node = ExprNode("operator", operator="**")
            self.get_next_token()
            next_component_node = self.component()
            component_node.add_child(atom_node)
            component_node.add_child(next_component_node)
        else:
            component_node = atom_node
        return component_node

    def atom(self):
        # Atom → CONST_ID | T | FUNC L_BRACKET Expression R_BRACKET | L_BRACKET Expression R_BRACKET

        if self.current_token.type.name == "CONST_ID":
            atom_node = ExprNode(type="value",value=self.current_token.value)
            self.get_next_token()

        elif self.current_token.type.name == "T":
            atom_node = ExprNode(type="value",value=self.current_token.lexeme)
            self.get_next_token()

        elif self.current_token.type.name == "FUNC":
            atom_node = ExprNode(type="func", func_name=self.current_token.lexeme)
            self.get_next_token()

            if self.current_token.type.name == "L_BRACKET":
                self.get_next_token()
            else:
                raise SyntaxError(f"current_token_index: {self.index} Unexpected token: {self.current_token.type}")
            
            expression_node = self.expression()

            if self.current_token.type.name == "R_BRACKET":
                self.get_next_token()
            else:
                raise SyntaxError(f"current_token_index: {self.index} Unexpected token: {self.current_token.type}")
            
            atom_node.add_child(expression_node)

        elif self.current_token.type.name == "L_BRACKET":
            if self.current_token.type.name == "L_BRACKET":
                self.get_next_token()
            else:
                raise SyntaxError(f"current_token_index: {self.index} Unexpected token: {self.current_token.type}")
            
            expression_node = self.expression()

            if self.current_token.type.name == "R_BRACKET":
                self.get_next_token()
            else:
                raise SyntaxError(f"current_token_index: {self.index} Unexpected token: {self.current_token.type}")
            atom_node = expression_node
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token.type}")

        return atom_node



tokens = Scanner_analys("test1.txt")



def InitParser():
    try:
        tmp = sys.stdout
        with open('../test/stdout1.txt', 'a') as f:
            sys.stdout = f  # 标准输出重定向到stdout1.txt文件,此时重定向到文件不会覆盖掉原本的内容,跟着词法分析的结果追加
            parser = Parser(tokens)
            parser.parse()
            sys.stdout = tmp
    except Exception as e:
            sys.stdout = tmp
            print(f"出错了!!!{e}")


InitParser()