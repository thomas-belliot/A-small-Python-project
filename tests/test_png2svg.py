from a_small_python_project.png2svg import load_image, hexagon_center, hexagon_points, ray_intersects_edge, is_point_in_hexagon, sample_color, rgb_to_hex, generate_hexagon, generate_svg, convert
from math import sqrt
import pytest


def test_load_image():
    image = load_image("img/image.jpg")
    assert(image.size == (900, 506))
    assert(image.mode == "RGB")
    assert(image.getpixel((0, 0)) == (22, 199, 232))

def test_hexagon_center():
    assert(hexagon_center(0, 0, 20) == (20*sqrt(3)/2, 20) )
    assert(hexagon_center(0, 1, 20) == (20*sqrt(3)*(1/2+1), 20) )
    assert(hexagon_center(1, 0, 20) == (20*sqrt(3), 20*(1+3/2))) 
    assert(hexagon_center(10, 5, 20) == (20*sqrt(3)*(5+1/2+1/2*(10%2)), 20*(1+10*3/2)))

def test_hexagon_points():
    """ The hexagon used for this test can be seen in "img/Hexagon_test.png" """
    test = hexagon_points(4.96, 8.68, 10)
    test = [(round(test[k][0],1), round(test[k][1],1)) for k in range(len(test))]
    # I did not succeed to put the points exactly at the right place on Geogebra, this is why I need the (round)
    assert((13.6, 13.7) in test)
    assert((13.6, 3.7) in test)
    assert((14, 4) not in test)
    assert(len(test)== 6)

def test_is_point_in_hexagon():
    """ The hexagon used for this test can be seen in "img/Hexagon_test.png" """
    x_False = [-4, -2, 0, 8, 0, 14, 10]
    y_False = [4, 2, 16, 0, 0, 10, 16]
    x_True = [2, -2, 2, 3, 6, 13, 8]
    y_True = [2, 14, 16, 16, 0, 10, 8]

    for k in range(len(x_False)):
        assert(is_point_in_hexagon(x_True[k], y_True[k], 4.96, 8.68, 10) == True)
        assert(is_point_in_hexagon(x_False[k], y_False[k], 4.96, 8.68, 10) == False)


def test_rgb_to_hex():
    assert( rgb_to_hex((0,0,0)) == "#000000" )
    assert( rgb_to_hex((10,0,12)).upper() == "#0A000C" )
    assert( rgb_to_hex((124,52,12)).upper() == "#7C340C" )
    assert( rgb_to_hex((124,50,12)).upper() == "#7C320C" )

