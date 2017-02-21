'''
Created on Jan 25, 2017

@author: lubo
'''
from tkutils.sample_ui import SampleUi


class ControllerBase(object):

    def __init__(self):
        pass

    @staticmethod
    def debug_event(event):
        # print(event)
        if event.name == 'button_press_event':
            print("MOUSE: name={}; xy=({},{}); xydata=({},{}); "
                  "button={}; dblclick={}".format(
                      event.name,
                      event.x, event.y,
                      event.xdata, event.ydata,
                      event.button, event.dblclick
                  ))
        elif event.name == 'button_release_event':
            print("MOUSE: name={}; xy=({},{}); xydata=({},{}); "
                  "button={}; dblclick={}".format(
                      event.name,
                      event.x, event.y,
                      event.xdata, event.ydata,
                      event.button, event.dblclick
                  ))
        elif event.name == 'key_press_event':
            print("KEY: name={}; xy=({},{}); xydata=({},{}); "
                  "key={}".format(
                      event.name,
                      event.x, event.y,
                      event.xdata, event.ydata,
                      event.key
                  ))
        else:
            print("???: {}".format(event.name))

    def register_sample_cb(self, func):
        self.add_sample_cb = func

    def event_loop_connect(self, fig):
        fig.canvas.mpl_connect('button_press_event', self.event_handler)
        fig.canvas.mpl_connect('key_press_event', self.event_handler)

    def event_handler(self, event):
        self.debug_event(event)
        if event.name == 'button_press_event' and event.button == 3:
            sample = self.locate_sample_click(event)
            self.add_sample(sample)

    def add_sample(self, sample):
        if sample is None:
            return
        if self.add_sample_cb:
            self.add_sample_cb([sample])

    def display_samples(self, samples_list):
        sample_ui = SampleUi(samples_list)
        fig = sample_ui.build_ui()
        self.sample_viewer.draw_samples(fig, samples_list)
        sample_ui.mainloop()

    def locate_sample_click(self, event):
        if event.xdata is None:
            return None
        xloc = int(event.xdata / self.model.interval_length)
        sample_name = self.model.column_labels[xloc]
        print("xloc: {}; sample name: {}".format(xloc, sample_name))
        return sample_name
