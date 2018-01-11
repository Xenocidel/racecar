import tkinter

class Track():

    def __init__(self):
        middle = Square(150,450,150,650)
        middle1 = Square(150,450,150,340)
        middle2 = Square(150,450,460,650)
        left_wall = Square(0,600,0,20)
        right_wall = Square(0,600,780,800)
        top_wall = Square(0,20,0,800)
        bottom_wall = Square(580,600,0,800)
        obstacle = Square(65,115,350,450)
        obstacle2 = Square(80,150,220,270)
        obstacle3 = Square(290,320,700,730)
        obstacle1 = Square(60,90,230,280)
        obstacle4 = Square(100,130,360,410)
        obstacle5 = Square(50,80,480,530)
        obstacle6 = Square(80,110,600,650)
        block = Square(450,600,350,450)
        self.obstacles = [middle1, middle2, left_wall, right_wall, top_wall, bottom_wall, obstacle1,
                          obstacle4, obstacle5, obstacle3, obstacle6]
        #self.obstacles = [middle1, middle2, left_wall, right_wall, top_wall, bottom_wall, obstacle3]

    def draw(self, screen:"tkinter.Canvas"):
        color = "#FF0000"
        for item in self.obstacles:
            screen.create_line(item.left, item.top, item.left, item.bottom, fill = color)
            screen.create_line(item.left, item.bottom, item.right, item.bottom, fill = color)
            screen.create_line(item.right, item.bottom, item.right, item.top, fill = color)
            screen.create_line(item.right, item.top, item.left, item.top, fill = color)

    def check_collision(self, point:"touple"):
        for item in self.obstacles:
            if(item.intersect(point)):
                return True
        return False


class Square():

    def __init__(self, top:float, bottom:float, left:float, right:float):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def intersect(self, point:"touple"):
        if(point[0] <= self.right+5 and point[0] >= self.left-5 and point[1] >= self.top-5 and point[1] <= self.bottom+5):
            return True
        else:
            return False
