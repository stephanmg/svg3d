#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######################
### author: stephan
### note: for now only quadrilaterals and triangles in 1d, 2d, 3d

# import xml parsing utility
import xml.etree.ElementTree as ET

# wrappers for exporters
def ugtosvg1(fin, fout, dim):
   """ Exports a 1d grid to a svg in 3d """
   ugtosvg(fin, fout, dim)

def ugtosvg2(fin, fout, dim):
   """ Exports an surface grid in 2d to a svg in 3d """
   ugtosvg(fin, fout, dim)

def ugtosvg3(fin, fout, dim):
   """ Export an volume grid in 3d to a svg in 3d """
   ugtosvg(fin, fout, dim)

# exporter
def ugtosvg(fin, fout, dim_=-1):
   """ Export a grid either 1d, 2d, or 3d to a svg in 3d """
   # debug
   debug = True

   # string constants
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

   # read the xml tree
   tree = ET.parse(fin)
   root = tree.getroot()
   
   # preprocessing & variable setup
   digits   = []
   quads    = []
   vertices = []
   counter  = 1
   
   # setup vertices
   for atype in tree.findall('vertices'):
      digits = atype.text.split(" ")

   if ( dim_ == -1 ):
      dim = int(tree.findall('vertices')[0].get('coords'))
   else:
      dim = dim_

   if (not (dim >= 1 or dim <= 3)):
      print("Dim is enforced to be in the range [1, 3]. Aborting.")
      return

   # consistency check
   if (dim == 3):
     for vertex in range(0, len(digits)-2, dim):
         vertices.append([float(digits[vertex]), float(digits[vertex+1]), float(digits[vertex+2])])
   elif (dim == 2):
     for vertex in range(0, len(digits)-2, dim):
         vertices.append([float(digits[vertex]), float(digits[vertex+1]), 0.0])
   elif (dim == 1):
     for vertex in range(0, len(digits)-2, dim):
         vertices.append([float(digits[vertex]), 0.0, 0.0])
   else:
      pass
   
   # process quadrilaterals
   for atype in tree.findall('quadrilaterals'):
      digits = atype.text.split(" ")
   
   for quad in range(0, len(digits)-3, 4):
      quads.append([int(digits[quad]), int(digits[quad+1]), int(digits[quad+2]), int(digits[quad+3])])
   
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
   
   # process triangles
   digits   = []
   tris     = []
   counter  = 1

   for atype in tree.findall('triangles'):
      digits = atype.text.split(" ")
   
   for tri in range(0, len(digits)-2, 3):
      tris.append([int(digits[tri]), int(digits[tri+1]), int(digits[tri+2])])
   
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

   if (debug): print(prepend)

# execute when run as main 
if __name__ == "__main__":
   fin  = "unit_cube_test.ugx"
   fout = "unit_cube_test.svg"
   ugtosvg(fin, fout)
