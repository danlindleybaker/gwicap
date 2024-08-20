import dearpygui.dearpygui as dpg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg


VIEWPORT_WIDTH = 1280
DRAW_HEIGHT = 850  # titlebar is approximately 40px
VIEWPORT_HEIGHT = DRAW_HEIGHT - 40
VERTICAL_WIDGET_NUMBER = 4
HEIGHT_DISCREPANCY = int(VIEWPORT_HEIGHT / VERTICAL_WIDGET_NUMBER)


class GWUI:
    def __init__(self, camera_texture, cam_width, cam_height, save_texture):
        self.camera_texture = camera_texture
        self.save_texture = save_texture
        self.cam_width = cam_width  +25
        self.cam_height = cam_height
        self.init_main_window()
        self.draw_children(VIEWPORT_WIDTH, DRAW_HEIGHT)

    def draw_children(self, width, height):
        dpg.configure_item(self.main_window, height=height, pos=[0, 0])
        dpg.configure_item(
            self.preview_window, width=width - self.cam_width, height=height, pos=[self.cam_width, 0]
        )
        dpg.configure_item(self.graph, width=-1, height=-1)
        # dpg.configure_item(self.camera_texture, width=width/5, height=height/2) 
        # dpg.configure_item(self.capture_button, texture_tag = self.camera_texture)

    def init_main_window(self):
        with dpg.window(
            no_title_bar=True, no_move=True, no_resize=True, width = self.cam_width, pos=[0,0]
        ) as self.main_window:
            self.capture_button = dpg.add_image_button(self.camera_texture, label="Capture")
            self.save_button = dpg.add_image_button(self.save_texture, label="Save")
            

        with dpg.window(
            no_title_bar=True, no_move=True, no_resize=True
        ) as self.preview_window:
            with dpg.plot(
                anti_aliased=True,
            ) as self.graph:
                self.results_time_axis = dpg.add_plot_axis(
                    dpg.mvXAxis, label="time", tag="time_axis"
                )
                self.results_V_axis = dpg.add_plot_axis(
                    dpg.mvYAxis, label="V", tag="V_axis"
                )
                # series belong to a y axis. Note the tag name is used in the update
                # function update_data

                self.results_plot = dpg.add_line_series(
                    x=[], y=[], label="Temp", parent="V_axis", tag="results_plot"
                )
                self.results_plot2 = dpg.add_line_series(
                    x=[], y=[], label="Temp", parent="V_axis", tag="results_plot2"
                )

    # def draw_graph(self, x, y):
    #     dpi = 500
    #     fig = plt.figure(figsize=(4, 3), dpi=dpi)
    #     canvas = FigureCanvasAgg(fig)
    #     ax = fig.gca()
    #     ax.plot(x, y, "ro")
    #     canvas.draw()
    #     buf = canvas.buffer_rgba()
    #     image = np.asarray(buf)
    #     image = image.astype(np.float32) / 255

    #     with dpg.texture_registry():
    #         self.graph_texture = dpg.add_raw_texture(
    #             4 * dpi, 3 * dpi, image, format=dpg.mvFormat_Float_rgba, id="texture_id"
    #         )
