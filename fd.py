#! /usr/bin/python
# coding=UTF-8
#--------------------
# KSP Telemachus
# Mission Control
# By Erik N8MJK
#--------------------

import time
import datetime
import curses
import traceback
import locale
import sys
import os
import pwd
import urllib2
import json
import random

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def xstr(s):
    if s is None:
        return ''
    return str(s)

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

def init_window(win):
    win.erase()
    topstring = "FLIGHT DATA"
    bottomstring = "TELEMETRY - RADAR"
    bottomfillstring = (78- len(bottomstring)) * " "
    topfillstring  = (78 - len(topstring)) * " "
    win.addstr(0,0," " + topstring + topfillstring, curses.A_REVERSE)
    win.addstr(23,0,bottomfillstring + bottomstring + " ", curses.A_REVERSE)

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

def checkTelemetry(pstat):
    if pstat == 0:
        return True
    else:
        return False

def fetchData():
    d = {'alt':'ERR!','altt':'?'}
    url = "http://108.196.82.116:8023/telemachus/datalink?throt=f.throttle&rcs=v.rcsValue&sas=v.sasValue&light=v.lightValue&pe=o.PeA&ap=o.ApA&ttap=o.timeToAp&ttpe=o.timeToPe&operiod=o.period&sma=o.sma&alt=v.altitude&hat=v.heightFromTerrain&mt=v.missionTime&sfcv=v.surfaceVelocity&ov=v.orbitalVelocity&vs=v.verticalSpeed&lat=v.lat&long=v.long&body=v.body&o2=r.resource[Oxygen]&co2=r.resource[CarbonDioxide]&h2o=r.resource[Water]&w=r.resource[ElectricCharge]&food=r.resource[Food]&waste=r.resource[Waste]&wastewater=r.resource[WasteWater]&mo2=r.resourceMax[Oxygen]&mco2=r.resourceMax[CarbonDioxide]&mh2o=r.resourceMax[Water]&mw=r.resourceMax[ElectricCharge]&mfood=r.resourceMax[Food]&mwaste=r.resourceMax[Waste]&mwastewater=r.resourceMax[WasteWater]&pitch=n.pitch&roll=n.roll&hdg=n.heading&pstat=p.paused&inc=o.inclination&ecc=o.eccentricity&aoe=o.argumentOfPeriapsis&lan=o.lan"
    try:
        u = urllib2.urlopen(url)
        d = json.load(u)
        d["tstatus"] = 1
    except:
        d["throt"] = " "	#Throttle
        d["rcs"] = " "		#RCS status
        d["sas"] = " "		#SAS status
        d["light"] = " "	#Lights status
        d["pe"] = " "		#PE
        d["ap"] = " "		#AP
        d["ttap"] = " "		#Time to AP
        d["ttpe"] = " "		#Time to PE
        d["operiod"] = " "	#Orbital period
        d["sma"] = " "		#SMA
        d["alt"] = " "		#Altitude
        d["hat"] = " "		#Height above terrain
        d["mt"] = " "		#Mission time
        d["sfcv"] = " "		#SFC velocity
        d["ov"] = " "		#Orbital velocity
        d["vs"] = " "		#Vertical speed
        d["lat"] = " "		#Latitude
        d["long"] = " "		#Longitude
        d["body"] = " "		#Orbital body
        d["o2"] = " "		#Oxygen
        d["co2"] = " "		#Carbon dioxide
        d["h2o"] = " "		#Water
        d["w"] = " "		#Electric charge
        d["food"] = " "		#Food
        d["waste"] = " "	#Solid waste
        d["wastewater"] = " "	#Liquid waste
        d["mo2"] = " "		#Max oxygen
        d["mco2"] = " "		#Max carbon dioxide
        d["mh2o"] = " "		#Max water
        d["mw"] = " "		#Max electric charge
        d["mfood"] = " "	#Max food
        d["mwaste"] = " "	#Max solid waste
        d["mwastewater"] = " "	#Max liquid waste
        d["pitch"] = " "	#Pitch degrees
        d["roll"] = " "		#Roll degrees
        d["hdg"] = " "		#Heading degrees
        d["pstat"] = "1"	#Telemetry status
        d["inc"] = " "		#Inclination
        d["ecc"] = " "		#Eccentricity
        d["aope"] = " "		#Argument of PE
        d["lan"] = " "		#Longitude of AN
        d["tstatus"] = 0
    return d

#def checkRadar(d):
#    maxralt = 7000000 #max radar altitude
#    minralt = 500 #min radar altitude
#    if d["body"] != "Kerbin":
#        return 1
#    if d["alt"] > maxralt:
#        return 2
#    if d["alt"] < minralt:
#        return 3
#    return 0

def getRadar(d):
    maxralt = 1000000 #max radar altitude
    minralt = 500 #min radar altitude
    d["ralt"] = rAlt(rSlop(d["alt"]))
    d["rpe"] = rAlt(rSlop(d["pe"]))
    d["rap"] = rAlt(rSlop(d["ap"]))
    if isNum(d["sma"]):
        d["smag"] = rAlt(rSlop(d["sma"] - 600000))
    else:
        d["smag"] = "ERR!"
    d["rlat"] = d["lat"]
    d["rlong"] = d["long"]
    d["rttap"] = d["ttap"]
    d["rttpe"] = d["ttpe"]
    d["rinc"] = d["inc"]
    d["rlan"] = d["lan"]
    d["roperiod"] = d["operiod"]
    d["rov"] = d["ov"]
    d["rstatus"] = "NOMINAL"
#    d["rstatus"] = d["tstatus"]
    if d["body"] != "Kerbin":
        d["ralt"] = "N/A"
        d["rpe"] = " "
        d["rap"] = " "
        d["rlat"] = " "
        d["rlong"] = " "
        d["smag"] = "N/A"
        d["rinc"] = " "
        d["rlan"] = " "
        d["roperiod"] = " "
        d["rov"] = " "
        d["rstatus"] = "UNAVAIL"
    if d["alt"] > maxralt:
        d["ralt"] = "MAX"
        d["rpe"] = " "
        d["rap"] = " "
        d["rlat"] = " "
        d["rlong"] = " "
        d["smag"] = "MAX"
        d["rinc"] = " "
        d["rlan"] = " "
        d["roperiod"] = " "
        d["rov"] = " "
        d["rstatus"] = "UNAVAIL"
    if d["alt"] < minralt:
        d["ralt"] = "MIN"
        d["rpe"] = " "
        d["rap"] = " "
        d["rlat"] = " "
        d["rlong"] = " "
        d["smag"] = "MIN"
        d["rinc"] = " "
        d["rlan"] = " "
        d["roperiod"] = " "
        d["rov"] = " "
        d["rstatus"] = "UNAVAIL"    
    if isNum(d["ralt"]):
        if d["ralt"] > 100000:
            if d["ralt"] > 1000000:
                  d["ralt"] = round(d["ralt"], -6)
            d["ralt"] = round(d["ralt"], -3)
        else:
            d["ralt"] = round(d["ralt"], -2)
    return d

def getTelemetry(d):
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
    if checkTelemetry(d["pstat"]):
        return d
    else:
        d["alt"] = "ERR!"
        d["altt"] = "?"
        d["lat"] = " "
        d["long"] = " "
        d["pitch"] = "0"
        d["roll"] = "0"
        d["hdg"] = "0"
        d["ttap"] = " "
        d["ttpe"] = " "
        d["sma"] = "ERR!"
        d["ap"] = " "
        d["pe"] = " "
        d["inc"] = " "
        d["ecc"] = " "
        d["lan"] = " "
        d["aop"] = " "
        d["ov"] = " "
        d["operiod"] = " "
        return d

def pnum(num):
    if isNum(num):
        nnum = xstr("{:,}".format(int(num)))
    else:
        nnum = num
    return nnum

def pvel(num):
    if isNum(num):
        nnum = xstr("{:,}".format(int(num))) + "m/s"
    else:
        nnum = num
    return nnum

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

def ptime(num):
    if isNum(num):
        m, s = divmod(num, 60)
        h, m = divmod(m, 60)
        h = str(int(h)).zfill(2)
        m = str(int(m)).zfill(2)
        s = str(int(s)).zfill(2)
        nnum = "%s:%s:%s" % (h,m,s)
    else:
        nnum = num
    return nnum

def pltime(num):
    if isNum(num):
        m, s = divmod(num, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        d = xstr(int(d)).zfill(2)
        h = xstr(int(h)).zfill(2)
        m = xstr(int(m)).zfill(2)
        s = xstr(int(s)).zfill(2)
        nnum = "%sd %s:%s:%s" % (d,h,m,s)
    else:
        nnum = num
    return nnum

def palt(num):
    kmlimit = 100000
    mmlimit = 999999000
    if isNum(num):
        if num < kmlimit:
            nnum = xstr("{:,}".format(int(num))) + "m"
        if num >= kmlimit:
            nnum = xstr("{:,}".format(int(num / 1000))) + "km"
        if num >= mmlimit:
            nnum = xstr("{:,}".format(int(num / 1000000))) + "Mm"
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

def init_time_window(win,y,x):
    timewin = curses.newwin(2,14,y,x)
    timewin.box()
    timewin.bkgd(curses.color_pair(1));
    win.refresh()
    timewin.addstr(0,1,"MISSION TIME",curses.A_BOLD)
    timewin.refresh()
    return timewin

def draw_time_window(win,data):
    win.addstr(1,1,"           ",curses.A_BOLD)
    win.addstr(1,1,pltime(data["mt"]),curses.A_BOLD)
    win.refresh()

def init_sys_window(win,y,x):
    syswin = curses.newwin(2,21,y,x)
    syswin.box()
    syswin.bkgd(curses.color_pair(1));
    win.refresh()
    syswin.addstr(0,1,"SYSYEMS",curses.A_BOLD)
    syswin.refresh()
    return syswin

def draw_sys_window(win,data):
    win.addstr(1,1,"RCS|SAS|LGT|TEL|RAD")
    if data["rcs"] == "True":
        win.addstr(1,1,"RCS",curses.A_REVERSE)
    if data["sas"] == "True":
        win.addstr(1,5,"SAS",curses.A_REVERSE)
    if data["light"] == "True":
        win.addstr(1,9,"LGT",curses.A_REVERSE)
    if isNum(data["alt"]):
        win.addstr(1,13,"TEL",curses.A_REVERSE)
    else:
        win.addstr(1,1,"???|???|???")
    if isNum(data["ralt"]):
        win.addstr(1,17,"RAD",curses.A_REVERSE)
    else:
        if data["ralt"] == "MAX":
            win.addstr(1,17,"RMX")
        if data["ralt"] == "MIN":
            win.addstr(1,17,"RMN")
        if data["ralt"] == "N/A":
            win.addstr(1,17,"RNA")
    win.refresh()

def init_tpos_window(win,y,x):
    twin = curses.newwin(11,18,y,x)
    twin.box()
    twin.bkgd(curses.color_pair(1));
    win.refresh()
    twin.addstr(0,1,"T.POS",curses.A_BOLD)
    twin.addstr(1,1,"  BODY ")
    twin.addstr(2,1," T.ALT ")
    twin.addstr(3,1," T.LAT ")
    twin.addstr(4,1,"T.LONG ")
    twin.addstr(5,1,"T.TTAP ")
    twin.addstr(6,1,"T.TTPE ")
    twin.addstr(7,1," T.PIT ")
    twin.addstr(8,1," T.ROL ")
    twin.addstr(9,1," T.HDG ")
    twin.refresh()
    return twin

def draw_tpos_window(win,data):
    win.addstr(1,8,"         ",curses.A_BOLD)
    win.addstr(2,8,"         ",curses.A_BOLD)
    win.addstr(3,8,"         ",curses.A_BOLD)
    win.addstr(4,8,"         ",curses.A_BOLD)
    win.addstr(5,8,"         ",curses.A_BOLD)
    win.addstr(6,8,"         ",curses.A_BOLD)
    win.addstr(7,8,"         ",curses.A_BOLD)
    win.addstr(8,8,"         ",curses.A_BOLD)
    win.addstr(9,8,"         ",curses.A_BOLD)
    win.addstr(1,8,pnum(data["body"]).upper(),curses.A_BOLD)
    win.addstr(2,7,pnum(data["altt"]))
    win.addstr(2,8,palt(data["alt"]),curses.A_BOLD)
    win.addstr(3,8,plat(data["lat"]),curses.A_BOLD)
    win.addstr(4,8,plong(data["long"]),curses.A_BOLD)
    win.addstr(5,8,ptime(data["ttap"]),curses.A_BOLD)
    win.addstr(6,8,ptime(data["ttpe"]),curses.A_BOLD)
    win.addstr(7,8,pdeg(data["pitch"]),curses.A_BOLD)
    win.addstr(8,8,pdeg(data["roll"]),curses.A_BOLD)
    win.addstr(9,8,pdeg(data["hdg"]),curses.A_BOLD)
    win.refresh()

def init_rpos_window(win,y,x):
    rwin = curses.newwin(8,18,y,x)
    rwin.box()
    rwin.bkgd(curses.color_pair(1));
    win.refresh()
    rwin.addstr(0,1,"R.POS",curses.A_BOLD)
    rwin.addstr(1,1,"STATUS ")
    rwin.addstr(2,1," R.ALT ")
    rwin.addstr(3,1," R.LAT ")
    rwin.addstr(4,1,"R.LONG ")
    rwin.addstr(5,1,"R.TTAP ")
    rwin.addstr(6,1,"R.TTPE ")
    rwin.refresh()
    return rwin

def draw_rpos_window(win,data):
    win.addstr(1,8,"         ",curses.A_BOLD)
    win.addstr(2,8,"         ",curses.A_BOLD)
    win.addstr(3,8,"         ",curses.A_BOLD)
    win.addstr(4,8,"         ",curses.A_BOLD)
    win.addstr(5,8,"         ",curses.A_BOLD)
    win.addstr(6,8,"         ",curses.A_BOLD)
    win.addstr(1,8,pnum(data["rstatus"]).upper(),curses.A_BOLD)
    win.addstr(2,8,palt(data["ralt"]),curses.A_BOLD)
    win.addstr(3,8,plat(data["rlat"]),curses.A_BOLD)
    win.addstr(4,8,plong(data["rlong"]),curses.A_BOLD)
    win.addstr(5,8,ptime(data["rttap"]),curses.A_BOLD)
    win.addstr(6,8,ptime(data["rttpe"]),curses.A_BOLD)
    win.refresh()

def init_rorb_window(win,y,x):
    rowin = curses.newwin(9,18,y,x)
    rowin.box()
    rowin.bkgd(curses.color_pair(1));
    win.refresh()
    rowin.addstr(0,1,"R.ORBIT",curses.A_BOLD)
    rowin.addstr(1,1,"R.SMAG ")
    rowin.addstr(2,1,"  R.AP ")
    rowin.addstr(3,1,"  R.PE ")
    rowin.addstr(4,1," R.INC ")
    rowin.addstr(5,1," R.LAN ")
    rowin.addstr(6,1,"R.OPRD ")
    rowin.addstr(7,1,"R.OVEL ")
    rowin.refresh()
    return rowin

def draw_rorb_window(win,data):
    win.addstr(1,8,"         ",curses.A_BOLD)
    win.addstr(2,8,"         ",curses.A_BOLD)
    win.addstr(3,8,"         ",curses.A_BOLD)
    win.addstr(4,8,"         ",curses.A_BOLD)
    win.addstr(5,8,"         ",curses.A_BOLD)
    win.addstr(6,8,"         ",curses.A_BOLD)
    win.addstr(7,8,"         ",curses.A_BOLD)
    win.addstr(1,8,palt(data["smag"]),curses.A_BOLD)
    win.addstr(2,8,palt(data["rap"]),curses.A_BOLD)
    win.addstr(3,8,palt(data["rpe"]),curses.A_BOLD)
    win.addstr(4,8,pdeg(data["rinc"]),curses.A_BOLD)
    win.addstr(5,8,plong(data["rlan"]),curses.A_BOLD)
    win.addstr(6,8,ptime(data["roperiod"]),curses.A_BOLD)
    win.addstr(7,8,pvel(data["rov"]),curses.A_BOLD)
    win.refresh()

def init_orbit_window(win,y,x):
    owin = curses.newwin(9,18,y,x)
    owin.box()
    owin.bkgd(curses.color_pair(1));
    win.refresh()
    owin.addstr(0,1,"T.ORBIT",curses.A_BOLD)
    owin.addstr(1,1," T.SMA ")
    owin.addstr(2,1,"  T.AP ")
    owin.addstr(3,1,"  T.PE ")
    owin.addstr(4,1," T.INC ")
    owin.addstr(5,1," T.LAN ")
    owin.addstr(6,1,"T.OPRD ")
    owin.addstr(7,1,"T.OVEL ")
    owin.refresh()
    return owin

def draw_orbit_window(win,data):
    win.addstr(1,8,"         ",curses.A_BOLD)
    win.addstr(2,8,"         ",curses.A_BOLD)
    win.addstr(3,8,"         ",curses.A_BOLD)
    win.addstr(4,8,"         ",curses.A_BOLD)
    win.addstr(5,8,"         ",curses.A_BOLD)
    win.addstr(6,8,"         ",curses.A_BOLD)
    win.addstr(7,8,"         ",curses.A_BOLD)
    win.addstr(1,8,palt(data["sma"]),curses.A_BOLD)
    win.addstr(2,8,palt(data["ap"]),curses.A_BOLD)
    win.addstr(3,8,palt(data["pe"]),curses.A_BOLD)
    win.addstr(4,8,pdeg(data["inc"]),curses.A_BOLD)
    win.addstr(5,8,plong(data["lan"]),curses.A_BOLD)
    win.addstr(6,8,ptime(data["operiod"]),curses.A_BOLD)
    win.addstr(7,8,pvel(data["ov"]),curses.A_BOLD)
    win.refresh()

def mainloop(win):
    timeposx = 0
    timeposy = 1
    tposx = 0
    tposy = 3
    rposx = 18
    roposy = 3
    roposx = 54
    rposy = 3
    oposx = 36
    oposy = 3
    sysx = 14
    sysy = 1
    win.nodelay(1)
    init_window(win)
    timewin = init_time_window(win,timeposy,timeposx)
    syswin = init_sys_window(win,sysy,sysx)
    twin = init_tpos_window(win,tposy,tposx)
    rwin = init_rpos_window(win,rposy,rposx)
    rowin = init_rorb_window(win,roposy,roposx)
    owin = init_orbit_window(win,oposy,oposx)
    while 1 is 1:
        data = fetchData()
        radar = getRadar(data)
        tele = getTelemetry(data)
        write_datetime(win)
        draw_time_window(timewin,tele)
        draw_sys_window(syswin,tele)
        draw_tpos_window(twin,tele)
        draw_rpos_window(rwin,radar)
        draw_rorb_window(rowin,radar)
        draw_orbit_window(owin,tele)
        time.sleep(1)

def startup():
    #wrapper to avoid console errors on program bug
    #totally stolen btw
    try:
        # Initialize curses
        stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        stdscr.bkgd(curses.color_pair(1));
        stdscr.bkgd(curses.color_pair(1));

        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)

        mainloop(stdscr)                # Enter the main loop

        # Set everything back to normal
        curses.echo()
        curses.nocbreak()
        stdscr.keypad(0)

        curses.endwin()                 # Terminate curses
    except:
        # In event of error, restore terminal to sane state.
        curses.echo()
        curses.nocbreak()
        stdscr.keypad(0)
        curses.endwin()
        traceback.print_exc()           # Print the exception

if __name__=='__main__':
    startup()



