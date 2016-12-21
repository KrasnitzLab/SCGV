'''
Created on Dec 14, 2016

@author: lubo
'''


class MainController(object):

    def __init__(self, model, sample_viewer):
        self.model = model
        self.sample_viewer = sample_viewer
        self.sample_list = []

    def event_loop_connect(self, fig):
        fig.canvas.mpl_connect('button_press_event', self.event_handler)
        fig.canvas.mpl_connect('key_press_event', self.event_handler)

    def event_handler(self, event):
        print("event tester called...")
        self.debug_event(event)
        if event.name == 'button_press_event':
            sample = self.locate_sample_click(event)
            self.add_sample(sample)
        elif event.name == 'key_press_event' and event.key == 'd':
            print(self.sample_list)

            self.display_samples()
            self.sample_list = []

    def add_sample(self, sample):
        if sample is None:
            return
        if sample in self.sample_list:
            return
        self.sample_list.append(sample)

    def display_samples(self):
        self.sample_viewer.draw_samples(self.sample_list)

    def locate_sample_click(self, event):
        if event.xdata is None:
            return None
        xloc = int(event.xdata / self.model.interval_length)
        sample_name = self.model.column_labels[xloc]
        print("xloc: {}; sample name: {}".format(xloc, sample_name))
        return sample_name

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
