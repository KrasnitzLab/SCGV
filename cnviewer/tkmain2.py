'''
Created on Jan 16, 2017

@author: lubo
'''
import sys  # @UnusedImport


from tkutils.profiles_ui import ProfilesUi
from tkutils.open_ui import OpenUi
from tkutils.canvas_ui import CanvasWindow


if sys.version_info[0] < 3:
    import Tkinter as tk  # @UnusedImport @UnresolvedImport
    import ttk  # @UnusedImport @UnresolvedImport
    from tkFileDialog import askopenfilename  # @UnusedImport @UnresolvedImport
    import tkMessageBox as messagebox  # @UnusedImport @UnresolvedImport
else:
    import tkinter as tk  # @Reimport @UnresolvedImport
    from tkinter import ttk  # @UnresolvedImport @UnusedImport @Reimport
    from tkinter.filedialog \
        import askopenfilename  # @UnresolvedImport @Reimport@UnusedImport
    from tkinter.filedialog \
        import askdirectory  # @UnresolvedImport @Reimport@UnusedImport

    from tkinter import messagebox  # @UnresolvedImport @Reimport @UnusedImport


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("cnviewer")

    main = CanvasWindow(root)

    profiles = ProfilesUi(main.button_ext)
    profiles.build_ui()
    main.register_on_controller_callback(profiles.connect_controller)

    open_buttons = OpenUi(main, main.toolbar_ext, main.fig)
    open_buttons.build_ui()

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.mainloop()
