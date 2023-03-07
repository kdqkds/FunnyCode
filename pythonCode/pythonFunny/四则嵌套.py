from typing import Set
import operator as op
vairables = {}

class code:
    index = 0
    def __hash__(self) -> int:
        self.index += 1
        return self.index
    
    def do(self) -> None:
        ...

class setValue(code):
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    def do(self):
        vairables[self.name] = self.value

class getValue(code):
    def __init__(self, name) -> None:
        self.name = name
    def do(self):
        return vairables[self.name]

class changeValue(code):
    # 实现 x+=1
    def __init__(self, name, dv, op) -> None:
        self.name = name
        self.dv = dv
        self.op = op
    def do(self):
        vairables[self.name] = self.op(vairables[self.name], self.dv)

class Op(code):
    def __init__(self, left, operator, value) -> None:
        self.left = left
        self.operator = operator
        self.value = value
    def do(self):
        if isinstance(self.left, str):
            return self.operator(vairables[self.left], self.value)
        elif isinstance(self.left, code):
            return self.operator(self.left.do(), self.value)
        else:
            return self.operator(self.left, self.value)

class If(code):
    # if(){}else(){}
    def __init__(self, *args) -> None:
        if len(args) == 4:
            self.condition = args[0]
            self.doCode: Set[code] = args[1]
            self.elsedo: Set[code] = args[3]
        elif len(args) == 2:
            self.condition = args[0]
            self.doCode: Set[code] = args[1]
            self.elsedo: Set[code] = set()
    def do(self) -> None:
        if self.condition.do():
            for coding in self.doCode:
                coding.do()
        elif self.elsedo:
            for coding in self.elsedo:
                coding.do()
class For(code):
    def __init__(self, init, judge, loopContent, loopcode) -> None:
        super().__init__()
        self.init = init
        self.judge = judge
        self.loopContent = loopContent
        self.loopcode = loopcode
    def do(self):
        self.init.do()
        while self.judge.do():
            for coding in self.loopContent:
                coding.do()
            self.loopcode.do()

class Print(code):
    def __init__(self, string) -> None:
        self.string = string
    def do(self) -> None:
        print(self.string.do())

class namespace:
    def __init__(self, *args) -> None:
        self.arr = args
    def run(self):
        for coding in self.arr:
            coding.do()

ns = namespace(
    For(    setValue("i", 0),
        
            Op(getValue("i"), op.lt, 1000),

        [If(Op(Op("i", op.mod, 2), op.eq, 0),
                [Print(getValue("i"))]
            )],

            changeValue("i", 1, op.add)

        )#for
)

ns.run()