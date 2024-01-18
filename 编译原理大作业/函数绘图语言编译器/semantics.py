from scanner import Token,Scanner_analys,Token_Type
import sys
import math

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
    
    def get_expr_value(self):
        if self.type == "value":
            return self.value
        elif self.type == "operator":
            left_value = self.children[0].get_expr_value()
            right_value = self.children[1].get_expr_value()

            if self.operator == "+":
                return left_value + right_value
            elif self.operator == "-":
                return left_value - right_value
            elif self.operator == "*":
                return left_value * right_value
            elif self.operator == "/":
                return left_value / right_value
            elif self.operator == "**":
                return left_value ** right_value
            # 添加其他运算符的处理

        elif self.type == "func":
            # 在这里处理函数的计算
            child_value = self.children[0].get_expr_value()
            if self.func_name == "SIN":
                return math.sin(child_value)
            if self.func_name == "COS":
                return math.cos(child_value)
            if self.func_name == "TAN":
                return math.tan(child_value)
            if self.func_name == "LN":
                return math.log(child_value)
            if self.func_name == "EXP":
                return math.exp(child_value)
            if self.func_name == "SQRT":
                return math.sqrt(child_value)

    def get_func_label(self):
        #由于在处理for的后两个带T的参数时不可能求出值,不能使用get_expr_value,而又由于我们需要这两个参数的最初字符串形式,所以通过get_func_label深度中序遍历来得到最初的字符串
        #也有其他得到最初字符串的方法,如重新遍历源程序,得到对应位置的参数,或重新遍历tokens将token拼接成对应参数
        label = ""

        if len(self.children) == 1 and self.type == "func":
            label += self.func_name
            label += "("
            label += self.children[0].get_func_label()
            label += ")"
            
        elif len(self.children) == 2 and self.type == "operator":
            label += self.children[0].get_func_label()
            label += self.operator
            label += self.children[1].get_func_label()

        else:
            label += str(self.value)


        return label

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = -1
        self.root = None
        #下方是语义分析需要返回的值,因为origin,rot,scale总是后出现的有效,所以,他其中的数值用一个常量来表示
        self.origin1 = 0.0
        self.origin2 = 0.0
        self.rot = 0.0
        self.scale1 = 1.0
        self.scale2 = 1.0
        #而for语句可以画多个图,所以采用列表来存储多个for语句的语义
        self.for1 = []
        self.for2 = []
        self.for3 = []
        self.for4 = []
        self.for5 = []
        self.for6 = []
        self.color = 'black'

    def func_to_math_func(self):
        #将输入中的函数名转换为可执行的函数格式
        # tmp_int = 0
        # while tmp_int<len(self.for5):
        #     self.for5[tmp_int] = self.for5[tmp_int].replace('SIN','math.sin')
        #     self.for5[tmp_int] = self.for5[tmp_int].replace('COS','math.cos')
        #     self.for5[tmp_int] = self.for5[tmp_int].replace('TAN','math.tan')
        #     self.for5[tmp_int] = self.for5[tmp_int].replace('LN','math.log')
        #     self.for5[tmp_int] = self.for5[tmp_int].replace('EXP','math.exp')
        #     self.for5[tmp_int] = self.for5[tmp_int].replace('SQRT','math.sqrt')

        #     self.for6[tmp_int] = self.for5[tmp_int].replace('SIN','math.sin')
        #     self.for6[tmp_int] = self.for5[tmp_int].replace('COS','math.cos')
        #     self.for6[tmp_int] = self.for5[tmp_int].replace('TAN','math.tan')
        #     self.for6[tmp_int] = self.for5[tmp_int].replace('LN','math.log')
        #     self.for6[tmp_int] = self.for5[tmp_int].replace('EXP','math.exp')
        #     self.for6[tmp_int] = self.for5[tmp_int].replace('SQRT','math.sqrt')

        #     tmp_int += 1
        math_functions = {
            'SIN': 'math.sin',
            'COS': 'math.cos',
            'TAN': 'math.tan',
            'LN': 'math.log',
            'EXP': 'math.exp',
            'SQRT': 'math.sqrt'
        }

        for i in range(len(self.for5)):
            for key, value in math_functions.items():
                self.for5[i] = self.for5[i].replace(key, value)
                self.for6[i] = self.for6[i].replace(key, value)

    def output_semantics(self):
        #先执行func_to_math_func函数
        self.func_to_math_func()
        #返回语义分析结果,先比例,再旋转,再平移

        return self.scale1,self.scale2,self.rot,self.origin1,self.origin2,self.for1,self.for2,self.for3,self.for4,self.for5,self.for6,self.color

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
        #匹配statement语句Statement →  OriginStatment | ScaleStatment|  RotStatment    | ForStatment

        print("enter in  statement")
        if self.current_token.type.name == "ORIGIN":
            self.origin_statement()
        elif self.current_token.type.name == "SCALE":
            self.scale_statement()
        elif self.current_token.type.name == "ROT":
            self.rot_statement()
        elif self.current_token.type.name == "FOR":
            self.for_statement()
        elif self.current_token.type.name == "COLOR":
            self.color_statement()
        else:
            raise SyntaxError(f"current_token_index: {self.index} Unexpected token: {self.current_token.type.name}")
        print("exit from  statement")

    def origin_statement(self):
        #匹配origin语句OriginStatment → ORIGIN IS L_BRACKET Expression COMMA Expression R_BRACKET

        print("enter in origin_statement")
        self.match("ORIGIN")
        self.match("IS")
        self.match("L_BRACKET")
        tmp_node = self.expression()
        self.origin1 = tmp_node.get_expr_value()
        self.match("COMMA")
        tmp_node = self.expression()
        self.origin2 = tmp_node.get_expr_value()
        self.match("R_BRACKET")
        print("exit from origin_statement")



    def scale_statement(self):
        #匹配scale语句ScaleStatment  → SCALE IS L_BRACKET Expression COMMA Expression R_BRACKET

        print("enter in scale_statement")
        self.match("SCALE")
        self.match("IS")
        self.match("L_BRACKET")
        tmp_node = self.expression()
        self.scale1 = tmp_node.get_expr_value()
        self.match("COMMA")
        tmp_node = self.expression()
        self.scale2 = tmp_node.get_expr_value()
        self.match("R_BRACKET")
        print("exit from scale_statement")


    def rot_statement(self):
        #匹配rot语句RotStatment → ROT IS Expression
        print("enter in rot_statement")
        self.match("ROT")
        self.match("IS")
        tmp_node = self.expression()
        self.rot = tmp_node.get_expr_value()
        print("exit from rot_statement")


    def for_statement(self):
        #匹配for语句 for_statement -> FOR T FROM expression TO expression STEP expression DRAW L_BRACKET Expression COMMA Expression R_BRACKET
        print("enter in for_statement")
        self.match("FOR")
        self.match("T")
        self.for1.append("T")
        self.match("FROM")
        tmp_node = self.expression()
        self.for2.append(tmp_node.get_expr_value())
        self.match("TO")
        tmp_node = self.expression()
        self.for3.append(tmp_node.get_expr_value())
        self.match("STEP")
        tmp_node = self.expression()
        self.for4.append(tmp_node.get_expr_value())
        self.match("DRAW")
        self.match("L_BRACKET")
        tmp_node = self.expression()
        self.for5.append(tmp_node.get_func_label())
        self.match("COMMA")
        tmp_node = self.expression()
        self.for6.append(tmp_node.get_func_label())
        self.match("R_BRACKET")
        print("exit from for_statement")

    def color_statement(self):
        #匹配color语句color_Statment → COLOR IS __
        print("enter in color_statement")
        self.match("COLOR")
        self.match("IS")
        if(self.current_token.type.name == "RED"):
            self.match("RED")
            self.color = "RED"
        elif(self.current_token.type.name == "GREEN"):
            self.match("GREEN")
            self.color = "GREEN"
        elif(self.current_token.type.name == "BLUE"):
            self.match("BLUE")
            self.color = "BLUE"
        elif(self.current_token.type.name == "BLACK"):
            self.match("BLACK")
            self.color = "BLACK"
        else:
            raise SyntaxError(f"current_token_index: {self.index} Unexpected token: {self.current_token.type}")
        print("exit from for_statement")
        
    def expression(self,flag = 0):
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
        if flag == 0:
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
            
            expression_node = self.expression(1)#由于这个expression是嵌套在expression内的,如果这个输出树求值的话会导致混乱,所以当带有参数1时,表示这个expression不输出树,也不求值

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
            
            expression_node = self.expression(1)#由于这个expression是嵌套在expression内的,如果这个输出树求值的话会导致混乱,所以当带有参数1时,表示这个expression不输出树,也不求值

            if self.current_token.type.name == "R_BRACKET":
                self.get_next_token()
            else:
                raise SyntaxError(f"current_token_index: {self.index} Unexpected token: {self.current_token.type}")
            atom_node = expression_node
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token.type}")

        return atom_node


def Semantic_analysis(tokens):
    try:
        tmp = sys.stdout
        with open('../test/stdout1.txt', 'a') as f:
            sys.stdout = f  # 标准输出重定向到stdout1.txt文件,此时重定向到文件不会覆盖掉原本的内容,跟着词法分析的结果追加
            parser = Parser(tokens)
            parser.parse()
            semantics_result = parser.output_semantics()
            print("语义分析结果:")
            print(semantics_result)
            sys.stdout = tmp
            return semantics_result
    except Exception as e:
            sys.stdout = tmp
            print(f"出错了!!!{e}")

#tokens = Scanner_analys("test1.txt")
#Semantic_analysis(tokens)