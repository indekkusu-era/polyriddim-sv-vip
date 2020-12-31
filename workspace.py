from sv_render import DecodeToFile, Noteoffset
from fundamentalF import stutter, LinearAccerlation
from SVEncodeDecode import SV
from random import random
poly_filedir = "nsvfile.osu"
out_filedir = "test6969.osu"
main_bpm = 140

# little heavy stutter
"""
>>> note = 0; nextNote-1 = fast; lastnote = 1
"""
allsv = []
def section1(start, end):
    offsets, notecount = Noteoffset(poly_filedir, start, end)
    del notecount
    for ofs, ofsend in zip(offsets[:-1], offsets[1:]):
        allsv.append(SV(ofs, 0.001, 20, 1))
        allsv.append(SV(ofsend - 1, 14000, 20, 1))
    allsv.append(SV(offsets[-1], main_bpm, 20, 1))

def section1GlitchSeq(start, end):
    offsets, notecount = Noteoffset(poly_filedir, start, end)
    del notecount
    for ofs in offsets:
        allsv.append(SV(ofs - 1, random() * 40000 + 10000, 20, 1))
        allsv.append(SV(ofs + 1, main_bpm, 20, 1))

def buildup(start, end):
    offsets, notecount = Noteoffset(poly_filedir, start, end)
    del notecount
    slope = 30000 / (offsets[-1] - offsets[0])
    for ofs, ofsend in zip(offsets[:-1], offsets[1:]):
        allsv.append(SV(ofs, 0.001, 20, 1))
        allsv.append(SV(ofsend - 1, slope * (ofsend - 1 - offsets[0]) + 0.001, 20, 1))
    allsv.append(SV(offsets[-1], main_bpm, 20, 1))

def drop_visual1(start, end):
    temp = start
    slope = (0.01 - 0.1) / (end - temp)
    while start < end:
        allsv.append(SV(start, 1000000, 20, 1))
        allsv.append(SV(start, 0.1 + slope * (start - temp), 20, 0))
        allsv.append(SV(start + 5, 1000000, 20, 1))
        allsv.append(SV(start + 6, 0.001, 20, 1))
        start += 10
    allsv.append(SV(end, main_bpm, 20, 1))

def chorus11(start, end):
    ofss, notecount = Noteoffset(poly_filedir, start, end)
    del notecount

    for t0, t1 in zip(ofss, ofss[1:] + [-1]):
        if t1 == -1:
            continue
        allsv.append(SV(t0 + 1, 100000, 20, 1))
        allsv.append(SV(t0 + 2, 30000 / (t1 - t0), 20, 1))
    allsv.append(SV(ofss[-1], main_bpm, 20, 1))

def chorus12(start, end):
    ofss, notecount = Noteoffset(poly_filedir, start, end)
    del notecount
    slope = 50000 / (ofss[-1] - ofss[0])

    for t0, t1 in zip(ofss, ofss[1:] + [-1]):
        if t1 == -1:
            continue
        allsv.append(SV(t0 + 1, 100000, 20, 1))
        allsv.append(SV(t0 + 2, slope / (t1 - t0) * (t0 - ofss[0]) + 0.001, 20, 1))
    allsv.append(SV(ofss[-1], main_bpm, 20, 1))

def chorus13(start, end):
    default = 2500
    multipiler = 1
    offsets, notecount = Noteoffset(poly_filedir, start, end)
    for i in range(len(offsets) - 1):
        if notecount[i] > 1:
            multipiler = 1
        allsv.append(SV(offsets[i], 0.001, 20, 1))
        allsv.append(SV(offsets[i+1] - 1, default * multipiler, 20, 1))
        multipiler += 1

def chorus135(start, end):
    # reverseLinearAccerlation from 0 to 50000
    # every notecount > 1 set bpm to 0
    offsets, notecount = Noteoffset(poly_filedir, start, end)
    is_greaterthan1 = list(map(lambda x: int(x > 1), notecount))
    # collect all offsets with > 1
    ofs_notsingle = []
    for ofs, isg in zip(offsets, is_greaterthan1):
        if isg == 1:
            ofs_notsingle.append(ofs)
    # sv
    slope = 0
    base = 0
    for t0, t1 in zip(offsets[:-1], offsets[1:]):
        if t0 in ofs_notsingle:
            nextnotsingle = ofs_notsingle[ofs_notsingle.index(t0) + 1]
            slope = 50000 / (nextnotsingle - t0)
            base = t0
        allsv.append(SV(t0 + 1, 100000, 20, 1))
        allsv.append(SV(t0 + 2, 0.001, 20, 1))
        allsv.append(SV(t1 - 1, slope * (t1 - base), 20, 1))
    allsv.append(SV(offsets[-1], main_bpm, 20, 1))

def chorus14(start, end):
    offsets, notecount = Noteoffset(poly_filedir, start, end)
    del notecount
    slope = 50000 / (offsets[-1] - offsets[0])
    for ofs in offsets:
        allsv.append(SV(ofs - 1, slope * (ofs - offsets[0]) + 0.001, 20, 1))
        allsv.append(SV(ofs, 100000, 20, 1))
        allsv.append(SV(ofs + 1, main_bpm, 20, 1))

def chorus21(start, end):
    offsets, notecount = Noteoffset(poly_filedir, start, end)
    del notecount
    section = (end - start) / 4
    slopeup = 30000 / (offsets[-1] - offsets[0])
    slopedown = -slopeup
    initvelup = 0.001
    initveldown = 60000
    for t0, t1 in zip(offsets[:-1], offsets[1:]):
        sect = (t1 - offsets[0]) // section
        allsv.append(SV(t0 + 1, 100000, 20, 1))
        allsv.append(SV(t0 + 2, 0.001, 20, 1))
        if sect % 2 == 0:
            allsv.append(SV(t1 - 1, initvelup +  slopeup * (t1 - 1 - offsets[0]), 20, 1))
        else:
            allsv.append(SV(t1 - 1, initveldown + slopedown * (t1 - 1 - offsets[0]), 20, 1))
        if t1 >= offsets[-1] - 2 * (60000/(main_bpm * 7/8)) - 10:
            allsv.append(SV(t1, main_bpm, 20, 1))
            break

def chorus22(start, end):
    # reverseLinearAccerlation from 0 to 50000
    # every notecount > 1 set bpm to 0
    offsets, notecount = Noteoffset(poly_filedir, start, end)
    is_greaterthan1 = list(map(lambda x: int(x > 1), notecount))
    # collect all offsets with > 1
    ofs_notsingle = []
    numbers = []
    for ofs, isg in zip(offsets, is_greaterthan1):
        if isg == 1:
            ofs_notsingle.append(ofs)
            numbers.append(1)
        else:
            numbers[-1] += 1
    # bpm visual
    counts = 1
    total = numbers[0]
    bpmlineperiod = 10000 / total
    for ofs in offsets[1:]:
        points = []
        if ofs in ofs_notsingle:
            counts = 0
            total = numbers[ofs_notsingle.index(ofs)]
            bpmlineperiod = 10000 / total
        points.append(bpmlineperiod * (counts + 1))
        for i in range(total - counts - 1):
            points.append(bpmlineperiod)
        points.append(200000)
        # place bpm
        for i in range(len(points)):
            co_i = len(points) - i
            off = ofs - 5 * co_i
            allsv.append(SV(off, points[i], 20, 1))
        allsv.append(SV(ofs + 1, 0.001, 20, 1))
        counts += 1
    allsv.append(SV(end, main_bpm, 20, 1))

def chorus23(start, end):
    offsets, notecount = Noteoffset(poly_filedir, start, end)
    del notecount
    for ofs in offsets:
        allsv.append(SV(ofs - 1, random() * 45000, 20, 1))
        allsv.append(SV(ofs, 100000, 20, 1))
        allsv.append(SV(ofs + 1, main_bpm, 20, 1))
def chorus24(start, end):
    offsets, notecount = Noteoffset(poly_filedir, start, end)
    del notecount
    for t0, t1 in zip(offsets[:-1], offsets[1:]):
        allsv.append(SV(t0 + 1, 100000, 20, 1))
        allsv.append(SV(t0 + 2, 0.001, 20, 1))
        allsv.append(SV(t1 - 1, random() * 50000, 20, 1))
    allsv.append(SV(offsets[-1], main_bpm, 20, 1))

allsv += list(LinearAccerlation(26992, 27460, 1, 10, 15))
section1(27481, 28950)
section1GlitchSeq(28950, 30787)
section1(30909, 33357)
section1GlitchSeq(33481, 34215)
buildup(34338, 39237)
drop_visual1(39237, 40215)
chorus11(41194, 53931)
chorus12(54908, 68623)
chorus13(69602, 76460)
chorus135(76459, 81522)
chorus14(82337, 96052)
allsv += list(LinearAccerlation(136705, 137180, 1, 10, 15))
section1(137194, 138663)
section1GlitchSeq(138663, 140500)
section1(140621, 143194)
section1GlitchSeq(143194, 143928)
buildup(144047, 148945)
drop_visual1(148949, 149926)
chorus21(150907, 164623)
chorus22(164621, 178337)
chorus23(179315, 191071)
chorus24(192050, 205765)
drop_visual1(219479, 225479)

# Render
DecodeToFile(poly_filedir, out_filedir, allsv)
print(len(allsv), "SV Lines Rendered")