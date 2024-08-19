import dearpygui.dearpygui as dpg
import matplotlib.pyplot as plt
import numpy as np
import dearpygui.dearpygui as dpg
from matplotlib.backends.backend_agg import FigureCanvasAgg


class GWUI:
    def __init__(self):
        self.init_main_window()
        self.draw_children(800, 600)

    def draw_children(self, width, height):
        dpg.configure_item(self.main_window, width=width/5, height=height, pos=[0, 0])
        dpg.configure_item(self.preview_window, width=4*width/5, height=height, pos=[width/5, 0])
        dpg.configure_item(self.graph, width=4*width/5 - 20, height=height - 20)

    def init_main_window(self):
        with dpg.window(no_title_bar=True, no_move=True, no_resize=True) as self.main_window:
            self.capture_button = dpg.add_button(label="Capture")
            self.save_button = dpg.add_button(label="Save")
            self.draw_graph([1,2,3,4,5], [1,2,3,4,5])
        with dpg.window(no_title_bar=True, no_move=True, no_resize=True) as self.preview_window:
            self.graph = dpg.add_image(self.graph_texture)

    def draw_graph(self, x, y):
        dpi = 500
        fig = plt.figure(figsize=(4, 3), dpi=dpi)
        canvas = FigureCanvasAgg(fig)
        ax = fig.gca()
        ax.plot(x, y, "ro")
        canvas.draw()
        buf = canvas.buffer_rgba()
        image = np.asarray(buf)
        image = image.astype(np.float32) / 255

        with dpg.texture_registry():
            self.graph_texture = dpg.add_raw_texture(
                4*dpi, 3*dpi, image, format=dpg.mvFormat_Float_rgba, id="texture_id"
            )

       
