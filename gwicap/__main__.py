import dearpygui.dearpygui as dpg
from pathlib import Path
import ctypes
import importlib.resources

VIEWPORT_WIDTH = 800
DRAW_HEIGHT = 600
 

def main():
    dpg.create_context()
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    MODULE_PATH = importlib.resources.files(__package__)
    dpg.create_viewport(
        title="SMPontaneous Polarisation", width=VIEWPORT_WIDTH, height=DRAW_HEIGHT
    )

    dpg.set_viewport_large_icon(MODULE_PATH / "assets/LCD_icon.ico")
    dpg.set_viewport_small_icon(MODULE_PATH / "assets/LCD_icon.ico")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    font_path = Path(MODULE_PATH / "assets/GeistVF.ttf")

    with dpg.font_registry():
        default_font = dpg.add_font(font_path, 18 * screensize[1] / 1080)
        title_font = dpg.add_font(font_path, 20 * screensize[1] / 1080)
        status_font = dpg.add_font(font_path, 36 * screensize[1] / 1080)

    dpg.bind_font(default_font)

    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    while dpg.is_dearpygui_running():
        # check if hotstage is connected. If it is, start thread to poll temperature.
        if (
            viewport_width != dpg.get_viewport_client_width()
            or viewport_height != dpg.get_viewport_client_height()
        ):
            # redraw_windows.
            viewport_width = dpg.get_viewport_client_width()
            viewport_height = dpg.get_viewport_client_height()
            # frontend.draw_children(viewport_width, viewport_height)

        dpg.render_dearpygui_frame()

    dpg.destroy_context()

if __name__ == "__main__":
    main()