#!/usr/bin/python3
# Проверяем доступность каналов и можем ли мы позвонить

from os import system


class FreeChannels(object):
    """
    Класс, отвечающий за проверку и наличие каналов связи
    """

    def __init__(self, max_channels=3):
        self.max_channels = max_channels

    def check(self):
        system("sudo asterisk -vvvvvvrx 'core show channels' |" \
               " grep call > channels.list")
        with open('channels.list', 'r') as file:
            line = file.readline()
        words = line.split()
        active_channels = int(words[0])
        free_channels = self.max_channels - active_channels
        print(free_channels)
        return free_channels


if __name__ == "__main__":
    channels = Channels()
    channels.check()
