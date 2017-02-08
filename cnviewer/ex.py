'''
Created on Feb 8, 2017

@author: lubo
'''


import tkinter
from PIL import Image, ImageTk
from tkutils.heatmap_legend import HeatmapLegend
from utils.color_map import ColorMap
from tkutils.legend_base import LegendEntry

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

images = []
for i in range(12):
    color = cmap.colors(i)
    tkcolor = LegendEntry.tkcolor(color)
    image = Image.new('RGBA', size=(20, 20), color=tkcolor)
    tkimage = ImageTk.PhotoImage(image=image)
    images.append(tkimage)

    canvas.create_image(i*21+20, 20, image=tkimage)

# heatmap = HeatmapLegend(root)
# heatmap.build_ui()

root.mainloop()
