from enum import Enum, auto
import math,re,sys

class Token_Type(Enum):
    #在原本语言的基础上新增改变函数图像的颜色的语句(只支持红绿蓝黑,默认为黑)
    COLOR = auto()
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    BLACK = auto()
    CONST_ID = auto()
    COMMENT = auto()
    ORIGIN = auto()
    SCALE = auto()
    ROT = auto()
    IS = auto()
    TO = auto()
    STEP = auto()
    DRAW = auto()
    FOR = auto()
    FROM = auto()
    #以上为保留字
    T = auto()
    #T为唯一的参数
    SEMICO = auto()
    L_BRACKET = auto()
    R_BRACKET = auto()
    COMMA = auto()
    #以上四个为分隔符:分号,左括号,右括号,逗号
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    POWER = auto()
    #以上为五个运算符
    FUNC = auto()
    #函数
    WHITE_SPACE = auto()
    #空格,制表符,回车,换行等
    NONTOKEN = auto()
    #空记号,源程序结束


class Token:
    def __init__(self, token_type, lexeme=None, value=0.0, func_ptr=None):
        self.type = token_type
        self.lexeme = lexeme
        self.value = value
        self.func_ptr = func_ptr

    def display(self):
        print(f"Type: {self.type}, Lexeme: {self.lexeme}, Value: {self.value}, FuncPtr: {self.func_ptr}")

# 正则表达式
patterns = [
    #与ppt上不同,取消了ID,将ID包含的各个种类的re分开写
    (Token_Type.FUNC, r'COS|SIN|TAN|LN|EXP|SQRT'),
    #函数的正则表达式的遍历位次一定要在T和E上边,防止将TAN和EXP匹配成T和E
    (Token_Type.CONST_ID, r'(\d+(\.\d*)?)|PI|E'),  # 匹配常数
    (Token_Type.COMMENT, r'//|--'),  # 匹配注释
    (Token_Type.COLOR,r'COLOR'),
    (Token_Type.RED,r'RED'),
    (Token_Type.GREEN,r'GREEN'),
    (Token_Type.BLUE,r'BLUE'),
    (Token_Type.ORIGIN, r'ORIGIN'),
    (Token_Type.SCALE, r'SCALE'),
    (Token_Type.ROT, r'ROT'),
    (Token_Type.IS, r'IS'),
    (Token_Type.TO, r'TO'),
    (Token_Type.STEP, r'STEP'),
    (Token_Type.DRAW, r'DRAW'),
    (Token_Type.FOR, r'FOR'),
    (Token_Type.FROM, r'FROM'),
    (Token_Type.T, r'T'),
    (Token_Type.SEMICO, r';'),
    (Token_Type.L_BRACKET, r'\('),
    (Token_Type.R_BRACKET, r'\)'),
    (Token_Type.COMMA, r','),
    (Token_Type.POWER, r'\*\*'),#乘方一定要在乘前,防止匹配的是两个*而不是一个**
    (Token_Type.PLUS, r'\+'),
    (Token_Type.MINUS, r'-'),
    (Token_Type.MUL, r'\*'),
    (Token_Type.DIV, r'/'),
    (Token_Type.WHITE_SPACE, r'\s+'),
]

def content_to_token(content):
    tokens = []
    pos = 0
    lexeme = None

    while pos < len(content):
        matched = False
        for token_type, pattern in patterns:
            match = re.match(pattern, content[pos:])
            if match:
                lexeme = match.group(0)
                
                if token_type == Token_Type.COMMENT:
                    # 注释类型，跳过注释内容直到换行符
                    pos += len(lexeme)
                    while pos < len(content) and content[pos] != '\n':
                        pos += 1
                
                elif token_type == Token_Type.WHITE_SPACE:
                    pos += len(lexeme) #当识别的下一类型为WHITE_SPACE时,pos+1
                elif token_type == Token_Type.CONST_ID:
                    #常数型自变量时分类处理
                    if(lexeme == "PI"):
                        tokens.append(Token(token_type,lexeme,3.1415926))
                        pos += 2
                    elif(lexeme == "E"):
                        tokens.append(Token(token_type,lexeme,2.71828))
                        pos +=1
                    else:
                        tokens.append(Token(token_type,lexeme,value=float(lexeme)))
                        pos += len(lexeme)
                elif token_type in {Token_Type.ORIGIN, Token_Type.SCALE, Token_Type.ROT, Token_Type.IS,Token_Type.TO, Token_Type.STEP, Token_Type.DRAW, Token_Type.FOR, Token_Type.FROM, Token_Type.COLOR, Token_Type.RED, Token_Type.GREEN, Token_Type.BLUE, Token_Type.BLACK}:
                    # 保留字类型时,加入tokens列表,新加入COLOR,RED,GREEN,BLUE,BLACK
                    tokens.append(Token(token_type,lexeme)) #value默认为0,函数指针默认为none(缺省参数)
                    pos += len(lexeme)

                elif token_type == Token_Type.T:
                    tokens.append(Token(token_type,lexeme)) #T时同保留字
                    pos += 1

                elif token_type in { Token_Type.SEMICO, Token_Type.L_BRACKET, Token_Type.R_BRACKET, Token_Type.COMMA}:
                    tokens.append(Token(token_type,lexeme)) #分隔符时也同保留字
                    pos += len(lexeme)

                elif token_type in {Token_Type.PLUS, Token_Type.MINUS, Token_Type.MUL, Token_Type.DIV, Token_Type.POWER}:
                    tokens.append(Token(token_type,lexeme)) #加减乘除乘方也同上
                    pos += len(lexeme)
                    
                elif token_type == Token_Type.FUNC:
                    if lexeme == "SIN":
                        tokens.append(Token(token_type,lexeme,0.0,func_ptr=math.sin))
                    elif lexeme == "COS":
                        tokens.append(Token(token_type,lexeme,0.0,func_ptr=math.cos))
                    elif lexeme == "TAN":
                        tokens.append(Token(token_type,lexeme,0.0,func_ptr=math.tan))
                    elif lexeme == "LN":
                        tokens.append(Token(token_type,lexeme,0.0,func_ptr=math.log))
                    elif lexeme == "EXP":
                        tokens.append(Token(token_type,lexeme,0.0,func_ptr=math.exp))
                    elif lexeme == "SQRT":
                        tokens.append(Token(token_type,lexeme,0.0,func_ptr=math.sqrt))
                    pos += len(lexeme)

                # elif token_type == Token_Type.NONTOKEN:
                #     print("能运行到这吗")
                #     return tokens
                    
                else:
                    print(f"Position: {pos}, Lexeme: {lexeme}")
                    print("出问题了,为什么会匹配失败呢")
                matched = True
                break

        if not matched:
            print(f"scanner:error!!!出错位置:Position: {pos}, 上一次匹配到的Lexeme: {lexeme}")
            print("scanner:error!!!无法识别的字符:", content[pos])
            pos += 1
    tokens.append(Token(Token_Type.NONTOKEN))
    return tokens #当整个content完全被扫描完后(即while结束后)将收集到的tokens返回

def Scanner_analys(file_name):
    try:
        with open(f'../test/{file_name}', 'r', encoding='utf-8') as file:
        # 读取文件内容
            content = file.read().upper()
            # print(content)
            tokens = content_to_token(content)
            with open('../test/stdout1.txt', 'w') as f:
                tmp = sys.stdout
                sys.stdout = f  # 标准输出重定向到stdout1.txt文件,此时重定向到文件会覆盖掉原本的内容
                print("词法分析开始!!!")
                for token in tokens:
                    token.display()
                print("词法分析结束!!!")
                sys.stdout = tmp # 将标准输出从文件返回为正常输出
            return tokens

    except FileNotFoundError:
        print("文件未找到，请检查文件路径是否正确。注意在当前路径下直接输入test内的文件名即可")
    except Exception as e:
        print(f"发生未知错误: {e}")

#Scanner_analys("test1.txt")
