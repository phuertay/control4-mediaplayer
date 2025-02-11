import socket
import random
import select

def send_udp_command(command, host, port):
    COUNTER = "0s2a" + str(random.randint(10, 99))
    COMMAND = COUNTER + " " + command + " \r\n"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    sock.setblocking(0)
    sock.sendto( bytes(COMMAND, "utf-8"), (host, port))

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(bytes(COMMAND, "utf-8"), (host, port))
        data, _ = sock.recvfrom(1024)
        received = str(data, "utf-8")
    except socket.timeout:
        received = "Timeout occurred during data reception"
    except Exception as e:
        received = {e}
    finally:
        sock.close()

    return received




class control4AmpChannel(object):
# Represents a channel of a Control 4 Matrix Amp

    def __init__(self, host, port, channel):
        self._host = host
        self._port = port
        self._channel = channel
        self._source = 1
        self._volume = 0

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def channel(self):
        return self._channel

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self,value):
        self._source = value
        return send_udp_command("c4.amp.out 0" + str(self._channel) + " 0" + str(self._source), self._host, self._port)

    @source.deleter
    def source(self):
        del self._source

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self,value):
        self._volume = value
        new_volume = int(float(self._volume) * 100) + 156
        new_volume = hex(min(new_volume,255))[2:]
        send_udp_command("c4.amp.chvol 0" + str(self._channel) + " " + new_volume, self._host, self._port)

    @volume.deleter
    def volume(self):
        del self._volume

    def turn_on(self):
        return send_udp_command("c4.amp.out 0" + str(self._channel) + " 0" + str(self._source), self._host, self._port)

    def turn_off(self):
        return send_udp_command("c4.amp.out 0" + str(self._channel) + " 00", self._host, self._port)

