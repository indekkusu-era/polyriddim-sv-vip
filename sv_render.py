def DecodeToFile(osufile, newfilename, SVLines: list):
    with open(newfilename, "w+") as f:
        old = open(osufile, "r")
        old = old.readlines()
        old_TotimingPoints = old[:old.index("[TimingPoints]\n") + 1]
        old_afterTimingPoints = old[old.index("[TimingPoints]\n") + 1:]
        all_file = old_TotimingPoints + [i.encode() for i in SVLines] + old_afterTimingPoints
        for k in all_file:
            f.write(k)

def Noteoffset(osufile, start, end, return_only_LN=False):
    with open(osufile, 'r') as f:
        f = f.readlines()
        offseto = []
        notecount = []
        for i in range(f.index("[HitObjects]\n")+1, len(f) - 1):
            if start < int(f[i].split(",")[2]) <= end:
                if int(f[i].split(",")[2]) in offseto:
                    notecount[-1] += 1
                    continue
                if return_only_LN:
                    splited = f[i].split(",")
                    release = int(splited[-1].split(":")[0])
                    if release == 0:
                        continue
                    else:
                        offseto.append([int(splited[2]), release])
                else:
                    offseto.append(int(f[i].split(",")[2]))
                    notecount.append(1)
    return offseto, notecount
