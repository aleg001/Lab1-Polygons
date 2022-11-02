# Modulo para estructura de bytes
import struct


# definiciones de estructuras bytes
def char(c):
    return struct.pack("=c", c.encode("ascii"))


def word(w):
    return struct.pack("=h", w)


def dword(d):
    return struct.pack("=l", d)


def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])


# Constates de bytes
firstW = word(1)
word24 = word(24)
headerInfo1 = 14 + 40
Dcero = dword(0)
Wcero = word(0)
w40 = dword(40)

# Valores constantes a usar de colores
color1 = "white"
color2 = "black"
color3 = "blue"


# funcion para colores a usar
def BasicColors(const):
    if const == "white":
        return color(1, 1, 1)
    if const == "black":
        return color(0, 0, 0)
    if const == "blue":
        return color(0, 1, 1)


"""
Math operations

Referencias: 
https://stackoverflow.com/questions/28253102/python-3-multiply-a-vector-by-a-matrix-without-numpy
https://stackoverflow.com/questions/10508021/matrix-multiplication-in-pure-python
https://mathinsight.org/matrix_vector_multiplication
https://www.mathsisfun.com/algebra/matrix-multiplying.html

"""


def VerifyIntegers(value):
    try:
        value = int(value)
    except:
        print("Error")


from collections import *

V2 = namedtuple("Point2", ["x", "y"])
V3 = namedtuple("Point3", ["x", "y", "z"])
V4 = namedtuple("Point4", ["x", "y", "z", "w"])


class Render(object):
    # (05 puntos) Deben crear una función glInit() que inicialice cualquier objeto interno que requiera su software renderer
    def __init__(self, width, height):
        self.glCreateWindow(width, height)
        self.clearColor = BasicColors(color2)
        self.currentColor = BasicColors(color1)
        self.glClear()

    # (05 puntos) Deben crear una función glCreateWindow(width, height) que inicialice su framebuffer con
    # un tamaño (la imagen resultante va a ser de este tamaño).
    def glCreateWindow(self, width, height):
        self.width = int(width)
        self.height = int(height)
        self.glViewPort(0, 0, self.width, self.height)

    # (10 puntos)  Deben crear una función glViewPort(x, y, width, height) que defina el área de la imagen sobre la que se va a poder dibujar
    def glViewPort(self, x, y, width, height):
        self.viewPortX = int(x)
        self.viewPortY = int(y)
        self.viewPortWidth = int(width)
        self.viewPortHeight = int(height)

    # (10 puntos) Deben crear una función glClearColor(r, g, b) con la que se pueda cambiar el color con el que funciona glClear().
    # Los parámetros deben ser números en el rango de 0 a 1.
    def glClearColor(self, r, g, b):
        self.clearColor = color(r, g, b)

    # (15 puntos) Deben crear una función glColor(r, g, b) con la que se pueda cambiar el color con el que funciona glVertex().
    # Los parámetros deben ser números en el rango de 0 a 1
    def glColor(self, r, g, b):
        self.currentColor = color(r, g, b)

    # (20 puntos) Deben crear una función glClear() que llene el mapa de bits con un solo color
    def glClear(self):
        self.pixels = [
            [self.clearColor for y in range(self.height)] for x in range(self.width)
        ]

    def glClearViewPort(self, cl=None):
        for x in range(self.viewPortX, self.viewPortX + self.viewPortWidth):
            for y in range(self.viewPortY, self.viewPortY + self.viewPortHeight):
                self.glPoint(x, y, cl)

    def glPoint(self, x, y, cl=None):
        if 0 <= x < self.width:
            if 0 <= y < self.height:
                self.pixels[x][y] = cl or self.currentColor

    def glPointViewport(self, x, y, cl=None):
        if x < -1 or x > 1 or y < -1 or y > 1:
            return
        tempX = x + 1
        tempY = y + 1
        tempVw = self.viewPortWidth / 2
        tempVh = self.viewPortHeight / 2
        finalX = tempX * tempVw + self.viewPortX
        finalY = tempY * tempVh + self.viewPortY

        finalX = int(finalX)
        finalY = int(finalY)

        self.glPoint(finalX, finalY, cl)

    def glLine(self, x0: V2, x1: V2, cl=None):
        tempX0 = int(x0.x)
        tempX1 = int(x1.x)
        tempY0 = int(x0.y)
        tempY1 = int(x1.y)

        if tempX0 == tempX1 and tempY0 == tempY1:
            self.glPoint(tempX0, tempY0, cl)
            return

        dy = tempY1 - tempY0
        dx = tempX1 - tempX0

        dy = abs(dy)
        dx = abs(dx)

        pendiente = dy > dx

        if pendiente == True:
            tempX0, tempY0 = tempY0, tempX0
            tempX1, tempY1 = tempY1, tempX1

        if pendiente == False:
            tempX0, tempY0 = tempX0, tempY0
            tempX1, tempY1 = tempX1, tempY1

        x1Bx0 = tempX1 < tempX0

        if x1Bx0 == True:
            tempX0, tempX1 = tempX1, tempX0
            tempY0, tempY1 = tempY1, tempY0

        if x1Bx0 == False:
            tempX0, tempX1 = tempX0, tempX1
            tempY0, tempY1 = tempY0, tempY1

        dx = tempX1 - tempX0
        dy = tempY1 - tempY0

        dy = abs(dy)
        dx = abs(dx)

        offset = 0
        limite = 0.5
        ecuacionRecta = dy / dx
        finalY = tempY0

        x1MasUno = tempX1 + 1

        for i in range(tempX0, x1MasUno):
            if pendiente == True:
                self.glPoint(finalY, i, cl)
            else:
                self.glPoint(i, finalY, cl)
            offset += ecuacionRecta
            if offset >= limite:
                finalY = finalY + 1 if tempY0 < tempY1 else finalY - 1
                limite += 1

    def glPolygon(self, polygon, cl=None) -> None:
        for i in range(len(polygon)):
            tempVar = i + 1
            moduleOp = tempVar % len(polygon)
            self.glLine(polygon[i], polygon[moduleOp], cl)
        self.glFillPolygon(polygon, cl, cl)

    def glFillPolygon(self, polygon, cl=None, color2=None) -> None:
        minX = min(polygon, key=lambda v: v.x).x
        maxX = max(polygon, key=lambda v: v.x).x
        minY = min(polygon, key=lambda v: v.y).y
        maxY = max(polygon, key=lambda v: v.y).y

        verifyMax = maxX > minX
        if verifyMax == True:
            minX = int(minX)
            maxX = int(maxX)
            maxMinX = maxX + minX
            maxMinY = maxY + minY
            mainX = maxMinX / 2
            mainY = maxMinY / 2
            mainX = int(mainX)
            mainY = int(mainY)

        def glColoring(x, y, cl, color2, option) -> None:
            YPlus = y + 1
            XPlus = x + 1
            XMinus = x - 1
            YMinus = y - 1
            if option == 1:
                if self.pixels[x][y] != cl:
                    self.glPoint(x, y, color2)
                    glColoring(x, YPlus, cl, color2, 1)
                    glColoring(XMinus, y, cl, color2, 1)
                    glColoring(XPlus, y, cl, color2, 1)
            if option == 2:
                if self.pixels[x][y] != cl:
                    self.glPoint(x, y, color2)
                    glColoring(x, YMinus, cl, color2, 2)
                    glColoring(XMinus, y, cl, color2, 2)
                    glColoring(XPlus, y, cl, color2, 2)

        glColoring(mainX, mainY, cl, color2, 1)
        self.glPoint(mainX, mainY, color(0, 1, 0))
        glColoring(mainX, mainY, cl, color2, 2)
        self.glPoint(mainX, mainY, color(0, 0, 0))

    def glFinish(self, filename):
        # constantes y calculos
        headerSize = headerInfo1 + (self.width * self.height * 3)
        widthD = dword(self.width)
        heightD = dword(self.height)
        whD = dword(self.width * self.height * 3)

        with open(filename, "wb") as f:
            f.write(char("B"))
            f.write(char("M"))
            f.write(dword(headerSize))
            f.write(Wcero)
            f.write(Wcero)
            f.write(dword(headerInfo1))
            f.write(w40)
            f.write(widthD)
            f.write(heightD)
            f.write(firstW)
            f.write(word24)
            f.write(Dcero)
            f.write(whD)
            f.write(Dcero)
            f.write(Dcero)
            f.write(Dcero)
            f.write(Dcero)

            for y in range(0, self.height):
                for x in range(0, self.width):
                    f.write(self.pixels[x][y])
            f.close()
