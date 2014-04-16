#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

def ugtosvg(fin, fout):
   prepend = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11-flat-20030114.dtd">
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
xmlns:z="http://debeissat.nicolas.free.fr/svg3d/svg3d.rng" width="120%" height="120%" onload="init(this)" z:sortAlgo="allToAll">
    <script type="text/ecmascript" xlink:href="../svg3d/svg3d.js" />
    <script type="text/ecmascript" xlink:href="../svg3d/svg3d_parsing.js" />
    <script type="text/ecmascript" xlink:href="../svg3d/dom_utils.js" />
   <title>SVG animation - auto-generated (no title set!)</title>
"""
   middle = """
"""
   append = """</svg>
"""

   tree = ET.parse(fin)
   root = tree.getroot()
   digits = []
   quads = []
   for atype in tree.findall('vertices'):
      digits = atype.text.split(" ")
   
   vertices = []
   for vertex in range(0, len(digits)-2, 3):
      vertices.append([float(digits[vertex]), float(digits[vertex+1]), float(digits[vertex+2])])
   
   for atype in tree.findall('quadrilaterals'):
      digits = atype.text.split(" ")
   
   for quad in range(0, len(digits)-3, 4):
      quads.append([int(digits[quad]), int(digits[quad+1]), int(digits[quad+2]), int(digits[quad+3])])
   
   counter = 1
   for quad in quads:
      quadstr = "M"
      for q in quad:
         for coord in range(0, len(vertices[q])-1, 1):
            quadstr += str(vertices[q][coord]) + ","
         
         quadstr += str(vertices[q][len(vertices[q])-1]) + "L"
      

      final_str = ""
      final_str += '<path id="'
      final_str += str(counter)
      final_str += '" style="fill: red;" d="';
      final_str += quadstr[:-1] + 'z"' 
      final_str += ' z:threeD="true">'
      final_str += "\n"
      final_str += '<z:rotation incRotX="0.07" incRotY="0.03" incRotZ="0.02"/>'
      final_str += "\n"
      final_str += '</path>'
      final_str += "\n"
      counter = counter + 1
      middle += final_str
   
   digits = []
   tris = []
   for atype in tree.findall('triangles'):
      digits = atype.text.split(" ")
   
   for tri in range(0, len(digits)-2, 3):
      tris.append([int(digits[tri]), int(digits[quad+1]), int(digits[quad+2])])
   
   counter = 1
   for tri in tris:
      tristr = "M"
      for t in tri:
         for coord in range(0, len(vertices[q])-1, 1):
            tristr += str(vertices[q][coord]) + ","
         
         tristr += str(vertices[q][len(vertices[q])-1]) + "L"
      

      final_str = ""
      final_str += '<path id="'
      final_str += str(counter)
      final_str += '" style="fill: red;" d="';
      final_str += tristr[:-1] + 'z"' 
      final_str += ' z:threeD="true">'
      final_str += "\n"
      final_str += '<z:rotation incRotX="0.07" incRotY="0.03" incRotZ="0.02"/>'
      final_str += "\n"
      final_str += '</path>'
      final_str += "\n"
      counter = counter + 1
      middle += final_str

   prepend += middle
   prepend += append
   output = open(fout, "w")
   output.write(prepend)
   output.close()
   print(prepend)
   
if __name__ == "__main__":
   fin  = "unit_cube_test.ugx"
   fout = "unit_cube_test.svg"
   ugtosvg(fin, fout)
