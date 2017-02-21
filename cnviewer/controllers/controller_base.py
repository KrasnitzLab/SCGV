'''
Created on Jan 25, 2017

@author: lubo
'''
import numpy as np


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


class HitmapControllerBase(ControllerBase):

    def __init__(self):
        super(HitmapControllerBase, self).__init__()
        self.on_add_samples_callbacks = []
        self.on_clear_samples_callbacks = []
        self.on_display_samples_callbacks = []

    def register_sample_cb(self, add_cb, clear_cb, display_cb):
        if add_cb:
            self.on_add_samples_callbacks.append(add_cb)
        if clear_cb:
            self.on_clear_samples_callbacks.append(clear_cb)
        if display_cb:
            self.on_display_samples_callbacks.append(display_cb)

    def event_loop_connect(self, fig):
        fig.canvas.mpl_connect('button_press_event', self.event_handler)
        fig.canvas.mpl_connect('key_press_event', self.event_handler)

    def event_handler(self, event):
        self.debug_event(event)
        if event.name == 'button_press_event' and event.button == 3:
            sample = self.locate_sample_click(event)
            self.add_samples([sample])

    def add_samples(self, samples):
        if not samples:
            return
        for cb in self.on_add_samples_callbacks:
            cb(samples)

    def display_samples(self, samples):
        if not samples:
            return
        for cb in self.on_display_samples_callbacks:
            cb(samples)
        #         sample_ui = SampleUi(samples_list)
        #         fig = sample_ui.build_ui()
        #         self.sample_viewer.draw_samples(fig, samples_list)
        #         sample_ui.mainloop()

    def clear_samples(self, samples):
        for cb in self.on_clear_samples_callbacks:
            cb(samples)

    def locate_sample_click(self, event):
        if event.xdata is None:
            return None
        xloc = int(event.xdata / self.model.interval_length)
        sample_name = self.model.column_labels[xloc]
        print("xloc: {}; sample name: {}".format(xloc, sample_name))
        return sample_name

    def get_profile_indices(self, profiles):
        profile_indices = []
        for i, p in enumerate(self.model.column_labels):
            if p in profiles:
                profile_indices.append(i)

        profile_indices = np.array(profile_indices)
        return profile_indices

    def highlight_profiles_labels(self, profiles):
        profile_indices = self.get_profile_indices(profiles)
        print("highlight profiles: {}".format(profile_indices))
        for index in profile_indices:
            self.ax_label.get_xticklabels()[index].set_color('red')

    def unhighlight_profile_labels(self, profiles):
        profile_indices = self.get_profile_indices(profiles)
        print("unhighlight profiles: {}".format(profile_indices))
        for index in profile_indices:
            self.ax_label.get_xticklabels()[index].set_color('black')
