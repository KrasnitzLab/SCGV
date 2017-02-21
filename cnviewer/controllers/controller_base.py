'''
Created on Jan 25, 2017

@author: lubo
'''


class ControllerBase(object):

    def __init__(self, model):
        self.model = model

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
