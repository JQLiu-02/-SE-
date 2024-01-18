import turtle
import math
from semantics import Semantic_analysis

class DRAW:
    def __init__(self,semantics_results):
        self.scale_x = semantics_results[0]
        self.scale_y = semantics_results[1]
        self.rot = semantics_results[2]#弧度
        self.origin_x = semantics_results[3]
        self.origin_y = semantics_results[4]
        self.color = semantics_results[11]#颜色
        # self.for_T = semantics_results[5]
        # self.for_from = semantics_results[6]
        # self.for_to = semantics_results[7]
        # self.for_step = semantics_results[8]
        # self.for_x = semantics_results[9]
        # self.for_y = semantics_results[10]
        self.for_all = []
        #将for中的参数的格式修改一下
        tmp_int = 0
        while tmp_int<len(semantics_results[5]):
            tmp_array = []
            tmp_int2 = 5
            while tmp_int2<11:
                tmp_array.append(semantics_results[tmp_int2][tmp_int])
                tmp_int2 += 1
            tmp_int += 1
            self.for_all.append(tmp_array)


    def ROT(self):
        #将语义分析得到的弧度值通过math的degrees函数转为turtle识别的角度
        angle = math.degrees(self.rot)
        turtle.left(angle)

    def Init(self):
        #turtle.setworldcoordinates(-960, 540, 960, -540)#设置画布的大小长为2560像素,宽为1600像素,并设置向下为y轴正方向
        turtle.pencolor(self.color)
        turtle.width(5)
        turtle.speed(0)  # 设置为最大速度
        turtle.tracer(0, 0)  # 关闭自动刷新
        # turtle.hideturtle()


    def draw(self):
        turtle.dot(6,self.color)#最初的原点
        for tmp_for in self.for_all:
            t = tmp_for[1]
            max_t = tmp_for[2]
            step = tmp_for[3]
            while t<=max_t:
                expression_x = tmp_for[4].replace('T',str(t))
                result_x = eval(expression_x)
                expression_y = tmp_for[5].replace('T',str(t))
                result_y = eval(expression_y)
                #scale缩放
                scale_x = result_x * self.scale_x
                scale_y = result_y * self.scale_y
                #rot旋转
                rot_x = scale_x * math.cos(self.rot) + scale_y * math.sin(self.rot)
                rot_y = scale_y * math.cos(self.rot) - scale_x * math.sin(self.rot)
                #origin平移
                origin_x = rot_x + self.origin_x
                origin_y = rot_y + self.origin_y

                turtle.penup()
                turtle.goto(origin_x,-origin_y)#负号代表y轴正方向朝下
                turtle.pendown()
                turtle.dot(3,self.color)
                t += step
                turtle.update()  # 手动刷新


# semantics_results = Semantic_analysis()
# draw = DRAW(semantics_results)
# #semantics_results =(100.0, 1000000.0, 1.5707963, 0.9589157234143065, 240.0, ['T', 'T'], [0.0, 0.0], [6.2831852, 6.2831852], [0.06283185200000001, 0.06283185200000001], ['COS(2.0*T+7.0)+10.0', 'LN(T+1.0)'], ['SIN(T)', 'EXP(T-1.0)'])
# draw.Init()
# draw.draw()
# turtle.mainloop()
def Draw(semantics_results):
    draw = DRAW(semantics_results)
    draw.Init()
    draw.draw()
    turtle.mainloop()

