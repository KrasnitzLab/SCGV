'''
Created on Feb 8, 2017

@author: lubo
'''


import tkinter
from PIL import Image, ImageTk
from tkutils.heatmap_legend import HeatmapLegend

root = tkinter.Tk()
# canvas = tkinter.Canvas(root)
# canvas.grid(row=0, column=0)
#
# image = Image.new('RGB', size=(50, 50), color=(255, 0, 0))
# tkimage = ImageTk.PhotoImage(image=image)
#
# canvas.create_image(0, 0, image=tkimage)

heatmap = HeatmapLegend(root)
heatmap.build_ui()

root.mainloop()


