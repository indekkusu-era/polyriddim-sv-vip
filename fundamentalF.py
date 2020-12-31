from SVEncodeDecode import SV, decode_SV
from random import random
import numpy as np

def stutter(average_velocity, start, end, slowstart, add_norm=False):
    st = []
    t_1 = slowstart - start
    v_2 = (end - start) * (average_velocity) / (end - start + 3 * t_1)
    v_1 = 4 * v_2
    st.append(SV(start, v_1, 20, 0))
    st.append(SV(slowstart, v_2, 20, 0))
    if add_norm:
        st.append(SV(end, 1, 20, 0))
    return st.copy()

# BPMLineReverse
def BPMLineReverse(start, end):
    bpmStart = 50
    allSVLines = []
    while start < end:
        allSVLines.append(SV(start, bpmStart, 20, 1))
        allSVLines.append(SV(start + 1, 100000, 20, 1))
        allSVLines.append(SV(start + 3, 0.06, 20, 1))
        start += 10
        bpmStart += 1500
    return allSVLines

# BPMLineShrink
def BPMLineShrink(start, end):
    bpmStart = 75000
    divider = 1
    allSVLines = []
    while start < end:
        allSVLines.append(SV(start, bpmStart / divider, 20, 1))
        allSVLines.append(SV(start + 1, 100000, 20, 1))
        allSVLines.append(SV(start + 3, 0.06, 20, 1))
        divider += 0.05
        start += 10
    return allSVLines

# DropAndTelePort
def DropAndTelePort(start, end, normalbpm):
    # 0 long, normal 10, fast ms
    delay = 0.06
    fast = 1000000
    allSVLines = []
    peak = ((start + end) / 2 + end) / 2
    allSVLines.append(SV(start, fast, 20, 1))
    allSVLines.append(SV(start, 0.01, 20, 0))
    allSVLines.append(SV(start + 10, delay, 20, 1))
    allSVLines.append(SV(peak, normalbpm * 1.5, 20, 1)) 
    return allSVLines

# BPMLines
def BPMLinesAppear(start, end, ms, normalbpm):
    allSVLines = []
    while start < end:
        allSVLines.append(SV(start, normalbpm, 20, 1))
        start += ms
    return allSVLines

# Glitch
def BPMGlitch(start, end):
    fastest = 75000
    allSVLines = []
    while start < end:
        allSVLines.append(SV(start, fastest * random(), 20, 1))
        allSVLines.append(SV(start + 1, 696969, 20, 1))
        allSVLines.append(SV(start + 3, 0.00069, 20, 1))
        start += 10
    return allSVLines

# BPMLineIncrement
def BPMLineIncrement(start, end, normalbpm):
    freqstart = 100
    freqmax = 10
    allSVLines = []
    while start < end:
        allSVLines.append(SV(start, normalbpm, 20, 1))
        start += max(freqstart, freqmax)
        freqstart /= 1.05
    return allSVLines

# BPMLineDec
def BPMLineDec(start, end, normalbpm):
    freqstart = 10
    allSVLines = []
    while start < end:
        allSVLines.append(SV(start, normalbpm, 20, 1))
        start += freqstart
        freqstart *= 1.01
    return allSVLines

# HeavyStutter
def HeavyStutter(listTP: list):
    allSVLines = []
    for i in listTP:
        allSVLines.append(SV(i-1, 7500, 20, 1))
        allSVLines.append(SV(i, 0.001, 20, 1))
    return allSVLines

def TelePortThenGhostLines(start, end, normalbpm):
    allSVLines = []
    allSVLines.append(SV(start, 696969, 20, 1))
    allSVLines += BPMLinesAppear(start + 10, end, 10, normalbpm)
    return allSVLines

def LinearAccerlation(start, end, start_velocity, end_velocity, freq):
    slope = (end_velocity - start_velocity) / (end - start)
    temp = start
    while temp < end:
        yield SV(temp, start_velocity + slope * (temp - start), 20, 0)
        temp += freq