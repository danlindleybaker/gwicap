import serial
from serial.serialutil import SerialException
import matplotlib.pyplot as plt


class GWIns:
    def __init__(self, address):

        try: 
            self.scope = serial.Serial(
                address,
                baudrate=9600,
                bytesize=8,
                parity="N",
                stopbits=1,
                xonxoff=False,
                dsrdtr=False,
                timeout=5,
            )
            self.initiased = True
        except SerialException:
            self.initiased = False

        if self.initiased:
            print(f"Time scale: {self.get_t_scale()}")

    def write(self, msg):
        self.scope.write(bytes(msg + "\n", encoding="ascii"))

    def get_v_scale(self, channel):
        self.write(f"CHAN{channel}:SCAL?")
        return float(self.scope.readline())
    
    def get_t_scale(self):
        # returns seconds per division and there are 10 divisions on the scope. So 800 bytes per div? 
        self.write(":TIMebase:SCALe?")
        return float(self.scope.readline())
    
    def get_waveforms(self):
        time, channel1 = self.get_waveform(1)
        _, channel2 = self.get_waveform(2)

        return time, channel1, channel2

    def get_waveform(self, channel):
        v_scale = self.get_v_scale(channel)
        t_scale = self.get_t_scale()
        self.write(f":ACQ{channel}:MEM?")
        header = self.scope.read(6)
        data_length_bytes = int(header[2:6])

        data = self.scope.read(data_length_bytes)

        integers = []
        # if there are 10 divs, and each div is t_scale, then increment = t_scale / (int(header[2:6])/(2*10))
        t_increment = t_scale / ((data_length_bytes - 8)/20)
        
        time = [i*t_increment for i in range(int((data_length_bytes - 8)/2))]
        
        # There are 8 bytes of extra header that aren't explained in the SCPI...
        for i in range(8, len(data), 2):
            num_in_bytes = data[i : i + 2]
            integers.append(int.from_bytes(num_in_bytes, byteorder="big", signed=True))

        return time, [(x / 25) * v_scale for x in integers]


if __name__ == "__main__":
    scope = GWIns("COM3")

    channel1 = scope.get_waveform(1)
    channel2 = scope.get_waveform(2)

    fig, ax = plt.subplots()
    ax.plot([x for x in range(len(channel1))], channel1, "r-")
    ax.plot([x for x in range(len(channel2))], channel2, "b-")

    plt.show()
