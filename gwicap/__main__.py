import dearpygui.dearpygui as dpg
from pathlib import Path
import ctypes
import importlib.resources

from gwicap.ui import GWUI, VIEWPORT_WIDTH, DRAW_HEIGHT
from gwicap.instrument import GWIns
from gwicap.utils import get_both_channel_data, save_screenshot, make_excel


import matplotlib.pyplot as plt
import matplotlib.font_manager as fm



def main():

    

    dpg.create_context()
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    MODULE_PATH = importlib.resources.files(__package__)
    dpg.create_viewport(
        title="GW Instek Capture", width=VIEWPORT_WIDTH, height=DRAW_HEIGHT,
    )

    dpg.set_viewport_large_icon(MODULE_PATH / "assets/gwicap_icon.ico")
    dpg.set_viewport_small_icon(MODULE_PATH / "assets/gwicap_icon.ico")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    font_path = Path(MODULE_PATH / "assets/GeistVF.ttf")


    # set Geist as the font for the saved matplotlib figure
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = font_name


    with dpg.font_registry():
        default_font = dpg.add_font(font_path, 18 * screensize[1] / 1080)
        title_font = dpg.add_font(font_path, 20 * screensize[1] / 1080)
        status_font = dpg.add_font(font_path, 36 * screensize[1] / 1080)

    dpg.bind_font(default_font)

    
    with dpg.theme() as graph_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0 ,0), category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvPlotCol_PlotBg, (255, 255, 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_FrameBg, (200, 200, 200), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBg, (200, 200, 200), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_InlayText, (0, 0, 0), category=dpg.mvThemeCat_Plots)

    with dpg.theme() as general_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [200, 200, 200])

    dpg.bind_theme(general_theme)

    cam_width, cam_height, channels, data = dpg.load_image(str(Path(MODULE_PATH / "assets/camera.png")))
    save_width, save_height, channels, save_data = dpg.load_image(str(Path(MODULE_PATH / "assets/save.png")))
    excel_width, excel_height, channels, excel_data = dpg.load_image(str(Path(MODULE_PATH / "assets/excel.png")))

    with dpg.texture_registry():
        camera_texture = dpg.add_static_texture(width=cam_width, height=cam_height, default_value=data, tag="camera_texture")
        save_texture = dpg.add_static_texture(width=save_width, height=save_height, default_value=save_data, tag="save_texture")
        excel_texture = dpg.add_static_texture(width=excel_width, height=excel_height, default_value=excel_data, tag="excel_texture")
        

    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    scope = GWIns("COM3")

    if not scope.initiased:
        with dpg.window():
            dpg.add_text("Could not initialise the oscilloscope. Please close the software and check connections.")
        frontend = GWUI(camera_texture, cam_width, cam_height, save_texture, excel_texture, False)
    else: 
        frontend = GWUI(camera_texture, cam_width, cam_height, save_texture, excel_texture)
        
        dpg.configure_item(
            frontend.capture_button, callback=lambda: get_both_channel_data(scope, frontend)
        )

        dpg.configure_item(
            frontend.save_button, callback = save_screenshot, user_data = frontend
        )
        dpg.configure_item(
            frontend.excel_button, callback = make_excel, user_data = frontend
        )

        dpg.bind_item_theme(frontend.graph,graph_theme)
    while dpg.is_dearpygui_running():
        # check if hotstage is connected. If it is, start thread to poll temperature.
        if (
            viewport_width != dpg.get_viewport_client_width()
            or viewport_height != dpg.get_viewport_client_height()
        ):
            # redraw_windows.
            viewport_width = dpg.get_viewport_client_width()
            viewport_height = dpg.get_viewport_client_height()
            if frontend.draw:
                frontend.draw_children(viewport_width, viewport_height)

        dpg.render_dearpygui_frame()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
