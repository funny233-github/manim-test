from manim import *
import math
class VectorExample(Scene):
    def construct(self):
        plane = NumberPlane()
        circle = Circle().scale(0.25)
        vector_1 = Vector().shift(RIGHT + UP)  # 创建向量
        t = ValueTracker(0)
        self.add(plane, vector_1, circle)

        def updater(vec):
            center = circle.get_center()  # 获取坐标
            vec_center = vec.get_center()
            vx = vec_center[0]
            vy = vec_center[1]
            x = center[0]
            y = center[1]
            # if vx == x and vy > y:
            #     angle = -0.5 * PI
            # else:
            angle = math.atan2(vy - y, vx - x)  # 通过正切求角度
            vec.set_angle(angle)

        def update_path(cir):
            p = t.get_value()
            y = 2*math.sin(p)  # 圆的参数方程
            x = 2*math.cos(p)
            cir.move_to(x * RIGHT + y * UP)

        vector_1.add_updater(updater)
        self.wait()
        self.play(circle.animate.move_to(5 * RIGHT), run_time=3)
        self.wait()
        self.play(circle.animate.move_to(RIGHT), run_time=10)
        circle.add_updater(update_path)
        self.play(t.animate.set_value(2 * PI))
        self.wait()

class main(Scene):
    def construct(self):
        tick = ValueTracker(0)
        def update_path(point):
            t = tick.get_value()
            x = t
            y = 0
            point.move_to(x*RIGHT + y * UP)
        def homotopy_func(x,y,z,t):
            return [x*t**PI,y*t**PI,z]
        def complexhomotopy_func(z: complex,t:float) -> complex:
            return interpolate(z,z**3,t)
        plane = NumberPlane()
        point = Dot()
        point.add_updater(update_path)
        self.play(SpinInFromNothing(plane),Create(point))
        self.play(ComplexHomotopy(complexhomotopy_func,plane))
        self.play(tick.animate.set_value(1))
        self.play(Uncreate(plane),Uncreate(point))
