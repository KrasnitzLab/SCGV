'''
Created on Feb 8, 2017

@author: lubo
'''


import tkinter
from PIL import Image, ImageTk
from tkutils.heatmap_legend import HeatmapLegend
from utils.color_map import ColorMap

root = tkinter.Tk()
canvas = tkinter.Canvas(root)
canvas.grid(row=0, column=0)

cmap = ColorMap.make_qualitative12()
color = cmap.colors(0.0)
print(color)
color = cmap.colors(1.0)
print(color)
r, g, b, a = color

color = (int(255 * r), int(255 * g), int(255 * b), int(255 * a))
image = Image.new('RGBA', size=(50, 50), color=color)
tkimage = ImageTk.PhotoImage(image=image)

canvas.create_image(0, 0, image=tkimage)

# heatmap = HeatmapLegend(root)
# heatmap.build_ui()

root.mainloop()
