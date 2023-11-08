from manimlib import *

class SurroundBox(Rectangle):
    def __init__(self,mobject:Mobject,color:str = YELLOW,**kwargs):
        super().__init__(
                mobject.get_width()+MED_SMALL_BUFF,
                mobject.get_height()+MED_SMALL_BUFF,
                )
        self.move_to(mobject.get_center())
        self.set_color(color)

class TextScene(Scene):
    def construct(self):
        text = Tex("x=a^2+b",isolate = ["a","b","="]).set_submobject_colors_by_gradient(BLUE,RED)
        text1 = Tex("x-a^2=b",isolate = ["a","b","="]).set_submobject_colors_by_gradient(BLUE,RED)
        text2 = Tex("(\\sqrt{x}+a)(\\sqrt{x}-a)=b",isolate = ["a","b","="]).set_submobject_colors_by_gradient(BLUE,RED)
        result1 = Tex("\\sqrt{x}=a+\\frac{b}{a+\\sqrt{x}}",isolate = ["\\sqrt{x}","="]).set_submobject_colors_by_gradient(BLUE,RED)
        group:Mobject = VGroup(text,text1,text2,result1)
        group2:Mobject = VGroup(text,text1,text2)
        group.arrange(DOWN)
        self.play(ShowCreation(text))
        self.play(ReplacementTransform(text.copy(),text1)) 
        self.play(ReplacementTransform(text1.copy(),text2))
        self.play(ReplacementTransform(text2.copy(),result1))
        self.play(FadeOut(group2))
        self.play(result1.animate.move_to(ORIGIN))
        result2 = Tex("\\sqrt{x}=a+\\frac{b}{2a+\\frac{b}{a+\\sqrt{x}}}",isolate = ["\\sqrt{x}","+"]).set_submobject_colors_by_gradient(BLUE,RED)
        self.play(ReplacementTransform(result1,result2))
        result3 = Tex("\\sqrt{x}=a+\\frac{b}{2a+\\frac{b}{2a+\\frac{b}{2a+\\frac{b}{2a+\\dots}}}}",isolate = ["\\sqrt{x}","+"]).set_submobject_colors_by_gradient(BLUE,RED)
        self.play(ReplacementTransform(result2,result3))
        surround = SurroundBox(result3)
        self.play(ShowCreation(surround))
        self.wait()
class SquareScene(Scene):
    def construct(self):
        square = Square().set_stroke(BLUE_E).set_fill(BLUE,0.7).scale(np.pi/2)
        self.play(ShowCreation(square))
        self.play(square.animate.apply_complex_function(np.exp))

class Tree(Scene):
    treeResult:list[Mobject] = []
    def facingLine(self,mobject:Mobject,width:float,facing:float):
        x = UP * width/2 * np.sin(facing) 
        y = RIGHT * width/2 * np.cos(facing)
        line = Line(mobject.get_center(),mobject.get_center()+x+y)
        self.add(line)
    def createBranch(self,base:Mobject,baseFacing:float,width:float,theta:float=PI/2/2): 
        center = base.get_center()
        baseUP = UP * np.cos(baseFacing) - RIGHT * np.sin(baseFacing)
        baseRIGHT = UP * np.sin(baseFacing) + RIGHT * np.cos(baseFacing)
        leftWidth = np.cos(theta/2)*width
        leftCenter = center + baseUP*((leftWidth*np.sin(theta/2+PI/4))/np.sqrt(2)+width/2) + baseRIGHT*(-width/2+leftWidth*np.cos(theta/2+PI/4)/np.sqrt(2))
        leftBranch = base.deepcopy().rotate(theta/2).scale(leftWidth/width).move_to(leftCenter).set_color(BLUE)

        rightWidth = np.sin(theta/2)*width
        rightCenter = center + baseUP*(rightWidth*np.sin(3*PI/4-theta/2)/np.sqrt(2)+width/2) + baseRIGHT*(width/2-rightWidth*np.cos(3*PI/4-theta/2)/np.sqrt(2))
        rightBranch = base.deepcopy().rotate((theta-PI)/2).scale(rightWidth/width).move_to(rightCenter).set_color(RED)
        return leftBranch,rightBranch
    def grownBase(self,base:Mobject,baseFacing:float,baseWidth:float,theta:float=PI/2/2,step:int=1):
        leftBranch,rightBranch = self.createBranch(base,baseFacing,baseWidth,theta)
        self.treeResult.append(leftBranch)
        self.treeResult.append(rightBranch)
        if step <= 0:
            return
        self.grownBase(leftBranch,theta/2+baseFacing,np.cos(theta/2)*baseWidth,theta,step-1)
        self.grownBase(rightBranch,(theta-PI)/2+baseFacing,np.sin(theta/2)*baseWidth,theta,step-1)
        
    def construct(self):
        rotate_angle = 0
        base = Square().shift(DOWN*3).scale(1).rotate(rotate_angle)
        group = Group(base)
        self.play(ShowCreation(group))
        for i in range(10):
            self.treeResult.append(base)
            self.grownBase(base,rotate_angle,Square().get_width(),PI/2,i)
            newgroup = Group(*self.treeResult)
            self.play(Transform(group,newgroup))
            self.wait()
            self.treeResult = []
class TreeBox(VMobject):
    def facingLine(self,mobject:Mobject,width:float,facing:float):
        x = UP * width/2 * np.sin(facing) 
        y = RIGHT * width/2 * np.cos(facing)
        line = Line(mobject.get_center(),mobject.get_center()+x+y)
        self.add(line)
    def createBranch(self,base:Mobject,baseFacing:float,width:float,theta:float=PI/2/2): 
        center = base.get_center()
        baseUP = UP * np.cos(baseFacing) - RIGHT * np.sin(baseFacing)
        baseRIGHT = UP * np.sin(baseFacing) + RIGHT * np.cos(baseFacing)
        leftWidth = np.cos(theta/2)*width
        leftCenter = center + baseUP*((leftWidth*np.sin(theta/2+PI/4))/np.sqrt(2)+width/2) + baseRIGHT*(-width/2+leftWidth*np.cos(theta/2+PI/4)/np.sqrt(2))
        leftBranch = base.deepcopy().rotate(theta/2).scale(leftWidth/width).move_to(leftCenter).set_color(BLUE)

        rightWidth = np.sin(theta/2)*width
        rightCenter = center + baseUP*(rightWidth*np.sin(3*PI/4-theta/2)/np.sqrt(2)+width/2) + baseRIGHT*(width/2-rightWidth*np.cos(3*PI/4-theta/2)/np.sqrt(2))
        rightBranch = base.deepcopy().rotate((theta-PI)/2).scale(rightWidth/width).move_to(rightCenter).set_color(RED)
        return leftBranch,rightBranch
    def grownBase(self,base:Mobject,baseFacing:float,baseWidth:float,theta:float=PI/2/2,step:int=1):
        leftBranch,rightBranch = self.createBranch(base,baseFacing,baseWidth,theta)
        self.add(leftBranch)
        self.add(rightBranch)
        if step <= 1:
            return
        self.grownBase(leftBranch,theta/2+baseFacing,np.cos(theta/2)*baseWidth,theta,step-1)
        self.grownBase(rightBranch,(theta-PI)/2+baseFacing,np.sin(theta/2)*baseWidth,theta,step-1)
    def set_theta(self,theta:float=PI/2/2):
        self.__init__(self.base,self.baseWidth,self.baseFacing,theta,self.step) 
        return self
        
    def __init__(self,base:Mobject,baseWidth:float|None=None,baseFacing:float=0,theta:float=PI/2/2,step:int=1):
        if baseWidth is None:
            baseWidth = base.get_width()
        self.base = base
        self.baseWidth = baseWidth
        self.baseFacing = baseFacing
        self.theta = theta
        self.step = step
        super().__init__()
        self.add(base)
        self.grownBase(base,baseFacing,baseWidth,theta,step)
class TestScene(Scene):
    def construct(self):
        DT = 1/60
        tree = TreeBox(Square().shift(DOWN*2),step=7,theta=0)
        self.add(tree)
        for i in range(314):
            tree.set_theta(i/100)
            self.wait(DT)
            print(i)
class TestNumberScene(Scene):
    def construct(self):
        DT = 1/60
        tree = TreeBox(Square().shift(DOWN*2),step=2,theta=0)
        num = DecimalNumber(number=0).shift(DOWN*2)
        self.add(tree,num)
        for i in range(314):
            tree.set_theta(i/100)
            num.set_value(i/100) 
            self.wait(DT)
            print(i)
