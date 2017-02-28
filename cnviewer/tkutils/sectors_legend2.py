'''
Created on Feb 1, 2017

@author: lubo
'''
from tkutils.tkimport import *  # @UnusedWildImport

from PIL import ImageTk
from tkutils.legend_base import LegendBase
from utils.color_map import ColorMap


class ShowPathologyDialog(tk.Toplevel):

    def __init__(self, image, notes, master, title=None, **kwargs):
        self.image = image
        self.notes = notes
        tk.Toplevel.__init__(self, master, **kwargs)
        # super(ShowPathologyDialog, self).__init__(master, **kwargs)

        # self.transient(master)
        if title:
            self.title(title)

        self.master = master

        body = ttk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        self.buttonbox()

        # self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (master.winfo_rootx() + 50,
                                  master.winfo_rooty() + 50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    def buttonbox(self):
        box = ttk.Frame(self)

        w = ttk.Button(
            box, text="OK", width=10, command=self.cancel, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.cancel)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.master.focus_set()
        self.destroy()

    def body(self, master):
        panel = None
        if self.image is not None:
            self.image = ImageTk.PhotoImage(self.image)
            panel = tk.Label(master, image=self.image)
            panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        text = tk.Text(master, width=80, height=20)
        scrollbar = tk.Scrollbar(master)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT, padx=10, fill=tk.Y)
        scrollbar.config(command=text.yview)
        text.config(yscrollcommand=scrollbar.set)

        if self.notes is not None:
            text.tag_configure('big', font=('Verdana', 15, 'bold'))
            text.insert(tk.END, self.notes[0], 'big')
            for line in self.notes[1:]:
                text.insert(tk.END, line)

        if panel is None:
            panel = text
        return panel


class SectorsLegend2(LegendBase):

    def __init__(self, master, controller):
        super(SectorsLegend2, self).__init__(
            master, title="Sectors Legend",
            controller=controller)

    def on_model(self, model):
        self.model = model
        self.sectors = self.model.make_sectors_legend()
        if self.sectors is None:
            return

        self.cmap = ColorMap.make_qualitative12()

        for (index, (sector, pathology)) in enumerate(self.sectors):
            color = self.cmap.colors(index)
            print(color)
            self.append_entry(
                text='{}: {}'.format(sector, pathology),
                color=color)

        self.bind_right_click(self.show_sector_pathology)
        self.bind_dbl_left_click(self.show_single_sector)

    def register_show_single_sector_callback(self, callback):
        self.show_single_sector_callback = callback

    def show_sector_pathology(self, index):
        if self.sectors is None:
            return
        print("show sector pathology with index: ", index)
        (sector, pathology) = self.sectors[index]
        print(self.sectors)
        print(sector, pathology)
        if self.controller.model.pathology is None:
            print("model.pathology is None; stopping...")
            return
        image, notes = self.controller.model.pathology.get(
            pathology, (None, None))
        if image is None and notes is None:
            return

        ShowPathologyDialog(image, notes, self.master)
        print("pathology dialog done...")

    def show_single_sector(self, index):
        if self.sectors is None:
            return
        print("show single sector viewer with index: ", index)
        (sector, _) = self.sectors[index]
        print("working with sector: ", sector)

        self.show_single_sector_callback(self.model, sector)

#
#         root = tk.Toplevel()
#         main = SectorsWindow(root)
#         controller.build_sector(main.fig)
#
#         main.connect_controller(controller)
#
#         def on_closing():
#             pass
#         main.register_on_closing_callback(on_closing)
#         root.mainloop()
