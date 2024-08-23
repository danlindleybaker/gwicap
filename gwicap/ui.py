import dearpygui.dearpygui as dpg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg


VIEWPORT_WIDTH = 1280
DRAW_HEIGHT = 667  # titlebar is approximately 40px
VIEWPORT_HEIGHT = DRAW_HEIGHT - 40
VERTICAL_WIDGET_NUMBER = 4
HEIGHT_DISCREPANCY = int(VIEWPORT_HEIGHT / VERTICAL_WIDGET_NUMBER)


class GWUI:
    def __init__(self, camera_texture, cam_width, cam_height, save_texture, excel_texture, draw = True):
        self.camera_texture = camera_texture
        self.save_texture = save_texture
        self.excel_texture = excel_texture
        self.cam_width = cam_width  +25
        self.cam_height = cam_height
        self.draw = draw

        if draw: 
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
            self.excel_button = dpg.add_image_button(self.excel_texture, label="excel")
            

        with dpg.window(
            no_title_bar=True, no_move=True, no_resize=True
        ) as self.preview_window:
            with dpg.plot(
                anti_aliased=True,
            ) as self.graph:
                
                dpg.add_plot_legend(location = 9)
                self.results_time_axis = dpg.add_plot_axis(
                    dpg.mvXAxis, label="time (s)", tag="time_axis"
                )
                self.results_V_axis = dpg.add_plot_axis(
                    dpg.mvYAxis, label="voltage (V)", tag="V_axis"
                )

                with dpg.theme() as self.channel1_theme:
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (255,0,0), category=dpg.mvThemeCat_Plots)
                        dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 3, category=dpg.mvThemeCat_Plots)

                with dpg.theme() as self.channel2_theme:
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (0,0,255), category=dpg.mvThemeCat_Plots)
                        dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 3, category=dpg.mvThemeCat_Plots)

                
                # series belong to a y axis. Note the tag name is used in the update
                # function update_data

                self.results_plot = dpg.add_line_series(
                    x=[], y=[], label="Channel 1", parent="V_axis", tag="results_plot"
                )

                self.results_plot2 = dpg.add_line_series(
                    x=[], y=[], label="Channel 2", parent="V_axis", tag="results_plot2"
                )
                dpg.bind_item_theme(self.results_plot, self.channel1_theme)
                dpg.bind_item_theme(self.results_plot2, self.channel2_theme)


                dpg.output_frame_buffer
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
