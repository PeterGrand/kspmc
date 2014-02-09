import random
import time
import datetime
import curses

def xstr(s):
    if s is None:
        return ''
    return str(s)

def pfloat(num):
    if isNum(num):
        nnum = xstr("{:,}".format(round(num,2)))
    else:
        nnum = num
    return nnum

def get_datetime():
    #let's make a pretty datetime
    global timeoutput
    global dateoutput
    t = datetime.datetime.now()
    currdatetime = t.timetuple()
    dateoutput = time.strftime("%Y-%m-%d",currdatetime)
    timeoutput = time.strftime("%d %b %Y %H:%M:%S",currdatetime)

def write_datetime(win):
    #separate function since this gets done A LOT
    get_datetime()

    win.move(0,59)
    win.clrtoeol()
    win.addstr(timeoutput, curses.A_REVERSE)
    win.refresh()

def isNum(num):
    try:
        float(num)
        return True
    except ValueError:
        pass
    return False

def rSlop(num):
    if isNum(num):
        nnum = num * random.uniform(0.99,1.01)
        return nnum
    else:
        return num

def rAlt(num):
    if isNum(num):
        nnum = round(int(num),-2)
        return nnum
    else:
        return num

def getTelemetry(d):
    maxgralt = "15000" #max altitude for ground radar
    if d["ttt1"] > 0:
        d["t1"] = d["mt"] + d["ttt1"]
    else:
        d["t1"] = d["ttt1"]
    if d["ttt2"] > 0:
        d["t2"] = d["mt"] + d["ttt2"]
    else:
        d["t2"] = d["ttt2"]
    d["apat"] = d["mt"] + d["ttap"]
    d["peat"] = d["mt"] + d["ttpe"]
    if isNum(d["pe"]) and d["pe"] < 0:
        d["pe"] = 0
    if d["pstat"] == 0:
        d["lat"] = rSlop(d["lat"])
        d["long"] = rSlop(d["long"])
    d["altt"] = "?"
    if isNum(d["vs"]):
        if d["vs"] < 0:
            d["altt"] = "-"
        else:
            d["altt"] = "+"
        if int(d["vs"]) == 0:
            d["altt"] = " "
        if isNum(d["vs"]):
            d["hs"] = d["sfcs"] - abs(d["vs"])
            d["vs"] = abs(d["vs"])
        else:
            d["hs"] = " "
    d["asl"] = d["alt"]
    if isNum(d["lf"]) and isNum(d["oxidizer"]):
        d["fuel"] = d["lf"] + d["oxidizer"]
    if isNum(d["mlf"]) and isNum(d["moxidizer"]):
        d["mfuel"] = d["mlf"] + d["moxidizer"]
    if isNum(d["asl"]):
        if d["hat"] == -1 or d["hat"] > maxgralt or d["pstat"] != 0:
            d["grstatus"] = "UNAVAIL"
            d["hat"] = "MAX"
            d["asl"] = " "
            d["vs"] = " "
            d["hs"] = " "
            d["sfcv"] = " "
            d["sfcvx"] = " "
            d["sfcvy"] = " "
            d["sfcvz"] = " "
        else:
            d["grstatus"] = "NOMINAL"
        return d

def fuck(status,instring):
    if status == 0 or status == 1:
        return instring
    if isNum(instring):
        workstring = str(instring)
    else:
        workstring = instring
    worklist = list(workstring)
    if status == 2:
        for i,char in enumerate(worklist):
            charlist = [char,char,char,char,char,char,char,char,char,char,char,char,char,char,char,char,char,char,'!','?','i','$','/','|','#']
            newchar = random.choice(charlist)
            worklist[i] = newchar
        outstring = "".join(worklist)
    if status == 3 or status == 4:
        for i,char in enumerate(worklist):
            newchar = " "
            worklist[i] = newchar
        outstring = "".join(worklist)    
    return outstring

def fucknum(status,indata):
    if status == 0 or status == 1:
        return indata
    if status == 2:
        if isNum(indata):
            errnum = random.uniform(0.75,1.25)
            outdata = indata * errnum
        else:
            return indata
    if status == 3 or status == 4:
        outdata = 0
    return outdata

def pnum(num):
    if isNum(num):
        nnum = xstr("{:,}".format(int(num)))
    else:
        nnum = num
    return nnum

def pvel(num):
    kmlimit = 10000
    if isNum(num):
        if num < kmlimit:
            nnum = xstr("{:,}".format(int(round(num,0)))) + "m/s"
        if num >= kmlimit:
            nnum = xstr("{:,}".format(round(num / 1000,1))) + "km/s"
    else:
        nnum = num
    return nnum

def phbar(num,mnum):
    if isNum(num) and isNum(mnum):
        pnum = int((num / mnum) * 100)
        onum = xstr(" " + "{:,}".format(round(num,1))) + " (" + xstr(pnum) + "%)"
    else:
        onum = num
    return onum

def printwarn(win,warn,state):
    if state == 0:
        win.addstr(1,1,warn,curses.A_BOLD)
    else:
        win.addstr(1,1,warn,curses.A_BLINK + curses.A_REVERSE)

def printhbar(win,instr,perc):
    i = 0
    barperc = int(35 * perc)
    barstring = instr.ljust(35)
    while i < 35:
        if i < barperc:
            win.addstr(barstring[i],curses.A_REVERSE)
        else:
            win.addstr(barstring[i])
        i = i + 1

def printvbar(win,perc):
    i = 0
    output = format(xstr(int(perc * 100)),">3s")
    barperc = int(9 * perc)
    while i < 9:
        if i < barperc:
            win.addstr(9-i,1,output,curses.A_REVERSE)
        else:
            win.addstr(9-i,1,output)
        i = i + 1
        output = "   "

def printvdef(win,perc):
    i = 0
    output = format(xstr(int(perc * 100)),">3s")
    barperc = int(9 * perc)
    while i < 9:
        if i < barperc:
            win.addstr(9-i,1,output,curses.A_REVERSE)
        else:
            win.addstr(9-i,1,output)
        i = i + 1
        output = "   "
   
def pdeg(inum):
    if isNum(inum):
        num = xstr(abs(int(inum))).zfill(3)
        if inum < 0:
            nnum = "-%s" % num
        else:
            nnum = "+%s" % num
    else:
        nnum = inum
    return nnum

def pdate(num):
    if isNum(num):
        m, s = divmod(num, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        y, d = divmod(d, 365)
        d = str(int(d)).zfill(3)
        y = str(int(y)).zfill(2)
        nnum = "Y%s D%s" % (y,d)
    else:
        nnum = num
    return nnum

def ptime(num):
    if isNum(num):
        m, s = divmod(num, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        y, d = divmod(d, 365)
        ys = str(int(y)).zfill(2)
        ds = str(int(d)).zfill(3)
        hs = str(int(h)).zfill(2)
        ms = str(int(m)).zfill(2)
        ss = str(int(s)).zfill(2)
        nnum = "%s:%s:%s" % (hs,ms,ss)
        if d >= 365:
            nnum = "%sy %sd" % (ys,ds)
        if h >= 24:
            nnum = "%sd %s:%s" % (ds,hs,ms) 
    else:
        nnum = num
    return nnum

def pltime(num):
    if isNum(num):
        m, s = divmod(num, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        y, d = divmod(d, 365)
        sy = xstr(int(y)).zfill(2)
        syl = xstr(int(y)).zfill(4)
        sd = xstr(int(d)).zfill(3)
        sh = xstr(int(h)).zfill(2)
        sm = xstr(int(m)).zfill(2)
        ss = xstr(int(s)).zfill(2)
        nnum = "%sd%s:%s:%s" % (sd,sh,sm,ss)
        if d >= 365:
            nnum = "%sy%sd%h:%d" % (sy,sd,sh,sm)
        if y >= 99:
            nnum = "%sy%sd%sh" % (syl,sd,sh)
    else:
        nnum = num
    return nnum

def palt(num):
    kmlimit = 100000
    mmlimit = 9999999
    if isNum(num):
        if num < kmlimit:
            nnum = xstr("{:,}".format(int(num))) + "m"
        if num >= kmlimit:
            nnum = xstr("{:,}".format(round(num / 1000,1))) + "km"
        if num >= kmlimit * 10:
            nnum = xstr("{:,}".format(int(round(num / 1000,0)))) + "km"
        if num >= mmlimit:
            nnum = xstr("{:,}".format(round(num / 1000000,1))) + "Mm"
    else:
        nnum = num
    return nnum

def pwgt(num):
    tonlimit = 10000
    if isNum(num):
        if num >= tonlimit:
            nnum = xstr("{:,}".format(round(num / 1000,3))) + "t"
        if num < tonlimit:
            nnum = xstr("{:,}".format(int(round(num,0)))) + "kg"
    else:
        nnum = num
    return nnum

def plat(inum):
    if isNum(inum):
        num = abs(inum)
        latmin = num - int(num)
        latdeg = num - latmin
        latmin = latmin * 60
        min = xstr(int(latmin)).zfill(2) + "'"
        deg = xstr(int(latdeg)).zfill(3) + " "
        if num < 0:
            nnum = deg + min + "S"
        else:
            nnum = deg + min + "N"
    else:
        nnum = inum
    return nnum

def plong(inum):
    if isNum(inum):
        if inum > 180:
            num = inum - 360
        else:
            num = inum
        longmin = abs(num - int(num))
        longdeg = abs(num - longmin)
        longmin = longmin * 60
        min = xstr(int(longmin)).zfill(2) + "'"
        deg = xstr(int(longdeg)).zfill(3) + " "
        if num < 0:
            nnum = deg + min + "W"
        else:
            nnum = deg + min + "E"
    else:
        nnum = inum
    return nnum
