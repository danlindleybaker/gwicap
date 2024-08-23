import dearpygui.dearpygui as dpg
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")
import tkinter as tk
from tkinter import filedialog
import xlsxwriter

from gwicap.instrument import GWIns
from gwicap.ui import GWUI


def get_both_channel_data(scope: GWIns, frontend: GWUI):
    time, channel1, channel2 = scope.get_waveforms()
    dpg.set_value(frontend.results_plot, [time, channel1])
    dpg.set_value(frontend.results_plot2, [time, channel2])
    dpg.fit_axis_data("V_axis")
    dpg.fit_axis_data("time_axis")


def open_tkinter_saveas_file_picker(type = "png"):
    root = tk.Tk()
    root.withdraw()

    if type == "png":
        filename = filedialog.asksaveasfilename(
            initialfile="scope_screenshot",
            defaultextension=".png",
            filetypes=(("Screenshots", "*.png"), ("All files", "*.*")),
        )
    elif type == "xlsx":
        filename = filedialog.asksaveasfilename(
            initialfile="scope_data",
            defaultextension=".xlsx",
            filetypes=(("Scope data", "*.xlsx"), ("All files", "*.*")),
        )
    root.destroy()
    return filename


# no mechanism to save dearpygui plot, so recreate in matplotlib and save that...


def save_screenshot(sender, app_data, user_data: GWUI):
    # get filename dialog - Tkinter (because it's native and doesn't look completely rubbish)

    filename = open_tkinter_saveas_file_picker()
    

    # make graph
    plt.rc("font", size=16)
    fig, ax = plt.subplots()
    fig.set_size_inches([12, 7])
    fig.set_facecolor((200 / 255, 200 / 255, 200 / 255))
    fig.set_dpi(500)
    channel1_x, channel1_y = dpg.get_value(user_data.results_plot)
    channel2_x, channel2_y = dpg.get_value(user_data.results_plot2)

    (h1,) = ax.plot(channel1_x, channel1_y, "r-")
    (h2,) = ax.plot(channel2_x, channel2_y, "b-")

    x_min, x_max = dpg.get_axis_limits(user_data.results_time_axis)

    # Get y-axis limits
    y_min, y_max = dpg.get_axis_limits(user_data.results_V_axis)

    plt.grid(True)

    plt.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.7)

    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])

    plt.xlabel("time (s)")
    plt.ylabel("voltage (V)")
    legend = plt.legend([h1, h2], ["Channel 1", "Channel 2"], loc="upper right")
    legend.get_frame().set_alpha(1)
    legend.get_frame().set_facecolor((200 / 255, 200 / 255, 200 / 255))

    # save graph to filename
    plt.savefig(filename)
    plt.close(fig)

def make_excel(sender, app_data, user_data: GWUI):

    channel1_x, channel1_y = dpg.get_value(user_data.results_plot)
    _, channel2_y = dpg.get_value(user_data.results_plot2)

    filename = open_tkinter_saveas_file_picker("xlsx")
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet(name = "Scope Data")
    worksheet.write(0, 0, 'time (s)')
    worksheet.write(0, 1, 'Channel 1 (V)')
    worksheet.write(0, 2, 'Channel 2 (V)')

    worksheet.write_column(1, 0, channel1_x) 
    worksheet.write_column(1, 1, channel1_y) 
    worksheet.write_column(1, 2, channel2_y) 
    worksheet.autofit()
    workbook.close()





