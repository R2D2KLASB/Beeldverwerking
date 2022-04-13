from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
from svg_to_gcode import TOLERANCES
import re

TOLERANCES['approximation'] = 0.8

def svgToGcode(path, name):
    # try:
        gcode_compiler = Compiler(interfaces.Gcode, movement_speed=100, cutting_speed=100, pass_depth=0)

        curves = parse_file(path + "/" + name) # Parse an svg file into geometric curves

        gcode_compiler.append_curves(curves) 
        gcode_compiler.compile_to_file(path + "/" + "tmp.gcode", passes=1)
        
        with open(path + "/" + 'tmp.gcode', "r") as gcode:
            gcode = list(gcode)
            scale = get_scale(gcode, 25000)
            gcode = simplifier(gcode, scale)

        return gcode
    # except:
    #     return False

def simplifier(gcode, scale=False):
    down = False
    tmp_gcode = ''
    print(gcode)
    for line in gcode[2:]:
        if "M5" in line:
            down = True
        elif "G1" in line:
            for word in line.split(" "):
                if "G1" in word:
                    if down:
                        tmp_gcode += 'G0'
                        down = False
                    else:
                        tmp_gcode += word
                elif "F" in word:
                    continue
                elif "X" in word:
                    temp = re.compile("([a-zA-Z]+)([0-9]+)")
                    items = temp.match(word).groups()
                    tmp_gcode +=(items[0])
                    if scale:
                        tmp_gcode +=(str(int(items[1]) * scale))
                    else:
                        tmp_gcode +=(str(int(items[1])))
                elif "Y" in word:
                    temp = re.compile("([a-zA-Z]+)([0-9]+)")
                    items = temp.match(word).groups()
                    tmp_gcode +=(items[0])
                    if scale:
                        tmp_gcode +=(str(int(items[1]) * scale))
                    else:
                        tmp_gcode +=(str(int(items[1])))
                    tmp_gcode +=("")
                if "\n" not in word:
                    tmp_gcode +=(" ")
                elif "\n" in word:
                    tmp_gcode +=("\n")
    tmp_gcode += 'G28'
    return tmp_gcode

def get_scale(gcode, maxXY):
    tmp = gcode
    x = 0
    y = 0
    for line in tmp:
        if "G" in line:
            for word in line.split(" "):
                if "X" in word:
                    print('ja')
                    temp = re.compile("([a-zA-Z]+)([0-9]+)")
                    items = temp.match(word).groups()
                    if int(items[1]) > x:
                        x = int(items[1])
                elif "Y" in word:
                    temp = re.compile("([a-zA-Z]+)([0-9]+)")
                    items = temp.match(word).groups()
                    if int(items[1]) > y:
                        y = int(items[1])
    scale = maxXY / max(x, y)
    return scale