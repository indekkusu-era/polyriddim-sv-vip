def encode_SV(offset, velocity, hitsoundvolume, isbpm):
    if isbpm == 1:
        return "{},{},4,1,0,{},1,0\n".format(offset,60000 / velocity,hitsoundvolume)
    return "{},{},4,1,0,{},0,0\n".format(offset,-100/velocity,hitsoundvolume)

class SV():
    def __init__(self, offset, velocity, hitsoundvolume, isbpm):
        self.offset = offset
        self.velocity = velocity
        self.hitsoundvolume = hitsoundvolume
        self.isbpm = isbpm
    
    def encode(self):
        return encode_SV(self.offset, self.velocity, self.hitsoundvolume, self.isbpm)

def decode_SV(timingPoints: str) -> SV:
    splited = timingPoints.split(",")
    return SV(float(splited[0]), float(splited[1]), int(splited[5]), int(splited[6]))


def invisibleLinearAcceration(start, end, bpm_start, bpm_end, points):
    slope = (bpm_end - bpm_start) / (end - start)
    get_bpm = lambda p: bpm_start + slope * (p - start)
    for point in points:
        yield SV(point-1, get_bpm(point), 25, 1)
        yield SV(point+1, 100000, 20, 1)
        yield SV(point+2, 0.001, 20, 1)
