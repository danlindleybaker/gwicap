import dearpygui.dearpygui as dpg

from gwicap.instrument import GWIns
from gwicap.ui import GWUI


def get_both_channel_data(scope: GWIns, frontend: GWUI):
    channel1, channel2 = scope.get_waveforms()
    dpg.set_value(frontend.results_plot, [[x for x in range(len(channel1))], channel1])
    dpg.set_value(frontend.results_plot2, [[x for x in range(len(channel2))], channel2])
    dpg.fit_axis_data('V_axis')
    dpg.fit_axis_data('time_axis')
