from gl import *

# Desplegar resultado
# Referencia: https://www.geeksforgeeks.org/python-pil-image-show-method/
from PIL import Image

# Colores
wh = color(1, 1, 1)


def Lab1(filename):
    r = Render(1920, 1080)
    figure1 = [
        V2(165, 380),
        V2(185, 360),
        V2(180, 330),
        V2(207, 345),
        V2(233, 330),
        V2(230, 360),
        V2(250, 380),
        V2(220, 385),
        V2(205, 410),
        V2(193, 383),
    ]
    figure2 = [V2(321, 335), V2(288, 286), V2(339, 251), V2(374, 302)]
    figure3 = [V2(377, 249), V2(411, 197), V2(436, 249)]
    figure4 = [
        V2(413, 177),
        V2(448, 159),
        V2(502, 88),
        V2(553, 53),
        V2(535, 36),
        V2(676, 37),
        V2(660, 52),
        V2(750, 145),
        V2(761, 179),
        V2(672, 192),
        V2(659, 214),
        V2(615, 214),
        V2(632, 230),
        V2(580, 230),
        V2(597, 215),
        V2(552, 214),
        V2(517, 144),
        V2(466, 180),
    ]

    r.glPolygon(figure1, wh)
    r.glPolygon(figure2, wh)
    r.glPolygon(figure3, wh)
    r.glPolygon(figure4, wh)

    r.glFinish(filename)
    im = Image.open(filename)
    im.show()
