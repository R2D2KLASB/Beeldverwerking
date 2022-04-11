from svg_to_gcode import TOLERANCES
import re

TOLERANCES['approximation'] = 0.8

def simplifier(gcode):
    tmp_gcode = ''
    for line in gcode[2:]:
        if "M5" in line:
            tmp_gcode += line
        elif "M3" in line:
            tmp_gcode +=("M3;\n")
        elif "G1" in line:
            for word in line.split(" "):
                if "G1" in word:
                    tmp_gcode +=(word)
                elif "F" in word:
                    continue
                elif "X" in word:
                    temp = re.compile("([a-zA-Z]+)([0-9]+)")
                    items = temp.match(word).groups()
                    tmp_gcode +=(items[0])
                    tmp_gcode +=(str(float(items[1]) * 40))
                elif "Y" in word:
                    temp = re.compile("([a-zA-Z]+)([0-9]+)")
                    items = temp.match(word).groups()
                    tmp_gcode +=(items[0])
                    tmp_gcode +=(str(float(items[1]) * 40))
                    tmp_gcode +=(";")
                if "\n" not in word:
                    tmp_gcode +=(" ")
                elif "\n" in word:
                    tmp_gcode +=("\n")
    return tmp_gcode