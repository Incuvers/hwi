#!/bin/bash

# BCM 22 is wPi 3
gpio edge 22 falling
# BCM 17 is wPi 0
gpio edge 17 both
# BCM 27 is wPi 2
gpio edge 27 both

chmod -R ugo+rw /sys/class/gpio
sudo chmod g+rw /dev/gpiomem
sudo chown root.gpio /dev/gpiomem
