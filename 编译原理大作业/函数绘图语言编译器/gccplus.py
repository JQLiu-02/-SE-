import sys
from scanner import Scanner_analys
from semantics import Semantic_analysis
from draw import Draw


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        tokens = Scanner_analys(file_name)
        semantics_results = Semantic_analysis(tokens)
        Draw(semantics_results)
    else:
        print("在命令行参数中只能输入一个文件名,如果没有文件名默认编译test1.txt文件")
        file_name = "test1.txt"
        tokens = Scanner_analys(file_name)
        semantics_results = Semantic_analysis(tokens)
        Draw(semantics_results)