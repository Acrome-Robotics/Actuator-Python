from crccheck.crc import Crc32Mpeg2 as CRC32
import struct
import acrome.controller
import time
import serial
from crccheck.crc import Crc32Mpeg2 as CRC32

from smd.red import *
from random import randint


m = Master('/dev/ttyUSB0')

