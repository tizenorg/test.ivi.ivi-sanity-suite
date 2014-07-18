#!/usr/bin/python
import time
import os
import string
import fmbttizen

app_icons = {}
app_icons_str = """
global app_icons
app_icons = { 
    "applist"           : "applist.%theme%.png",
    "browser-icon"      : "browser.icon.png",
    "settings-icon"     : "settings.icon.png",
    "terminal-icon"     : "terminal.icon.png",
    "saythis-icon"      : "saythis.icon.%theme%.png",
    "mediaplayer-icon"  : "mediaplayer.icon.%theme%.png",
    "dialer-icon"       : "dialer.icon.%theme%.png",
    "ghostcluster-icon" : "ghostcluster.icon.%theme%.png",
    "mp-main"           : ["mp.main0.%theme%.png", "mp.main1.%theme%.png", "mp.main2.%theme%.png"],
    "dl-main"           : ["dl.main0.%theme%.png"],
    "gc-main"           : ["gc.main0.png"],
    "say-main"          : ["say.main0.png"],
    "st-main"           : ["st.main0.png"],
    "brw-main"          : ["brw.main0.png"],
    "color"             : ["color.jpg"],
}
"""

class AppStack():
    def __init__(self):
        self.apps = ["desktop"]

    def __str__(self):
        return self.apps.__str__()

    def pushApp(self, app_name):
        try:
            self.apps.remove(app_name)
        except:
            pass
        self.apps.append(app_name)
        return self.apps[-1]
     
    def removeApp(self, app_name):
        assert self.isLaunched(app_name), '%s not in app stack' % app_name
        self.apps.remove(app_name)
        return self.apps[-1]
     
    def isLaunched(self, app_name):
        return app_name in self.apps
 
class fMBTController(fmbttizen.Device):
    def __init__(self, move_cursor=False, *args, **kwds):
        global ivi_args
        self.dev_ip = ivi_args.device
        assert self.dev_ip and ivi_args.ui, "++ incomplete parameters: dev_ip, ui!!!"
        fmbttizen.Device.__init__(self, loginCommand='ssh ' + self.dev_ip, *args, **kwds)
        self.maxX, self.maxY = 0, 0
        self.move_cursor = move_cursor
        if self.move_cursor == True:
            print "++ force using mouse !!!"
        self.maxX, self.maxY = self.screenSize()
        print "++ maxX(%d), maxY(%d)" % (self.maxX, self.maxY)
        self.dev_display = "%sx%s" % (self.maxX, self.maxY)
        bitmap_path = "/usr/lib/ivi-tests_pics/" + self.dev_display +"/" + ivi_args.ui + "/"
        print "++ using bitmap path: " + bitmap_path
        #self.enableVisualLog("ivi_apps.html", copyBitmapsToScreenshotDir=True)
        self.setBitmapPath(bitmap_path)

    def eventPlayback(self, ev_script, wait_time=1):
        cmd = "ev_playback /usr/lib/event_scripts/%s/%s" \
              % (self.dev_display, ev_script)
        print "++ run device cmd: " + cmd
        (ret, so, se) = self.shellSOE(cmd)
        if ret != 0:
            print "++ fail to playback event"
            print "++ standard output: " + so 
            print "++ standard error:" + se
        time.sleep(wait_time)
        return ret

    def swipeToEast(self, wait_time=1):
        print "++ swipe to the east"
        ret = self.swipe((0.5,0.5), direction="e")
        time.sleep(wait_time)
        return ret

    def swipeToWest(self, wait_time=1):
        print "++ swipe to the west"
        ret = self.swipe((0.5,0.5), direction="w")
        time.sleep(wait_time)
        return ret

    def swipeToNorth(self, wait_time=1):
        print "++ swipe to the north"
        ret = self.swipe((0.5,0.5), direction="n")
        time.sleep(wait_time)
        return ret

    def swipeToSouth(self, wait_time=1):
        print "++ swipe to the south"
        ret = self.swipe((0.5,0.5), direction="s")
        time.sleep(wait_time)
        return ret
    
    def tap(self, *args, **kwds):
        ret = fmbttizen.Device.tap(self, *args, **kwds)
        time.sleep(1)
        return ret

    def refAndTapBitmap(self, png, wait_time=1):
        print "++ refresh screen and tapBitmap " + png
        ret = self.refreshScreenshot() and self.tapBitmap(png)
        time.sleep(wait_time)
        return ret

    def refAndVerifyBitmap(self, png, wait_time=1):
        print "++ refresh screen and verify bitmap " + png
        ret = self.refreshScreenshot() and self.verifyBitmap(png)
        time.sleep(wait_time)
        return ret
        
    def refAndWaitAllBitmap(self, picture_list):
        print "++ refresh screen and wait all bitmap: " \
               + ', '.join(picture_list)
        self.refreshScreenshot()
        ret = True
        for p in picture_list:
            if not self.waitBitmap(p):
                print "++ %s not found" % p
                ret = False
        return ret

    def findPid(self, process_name):
        cmd = "pgrep -f '%s'" % process_name
        (r, so, se ) = self.shellSOE(cmd)
        pids = []
        if r == 0:
            pids = [string.atoi(n) for n in filter(lambda l: len(l)>0, so.split("\n"))]
        return r, pids

    def verifyAllProcess(self, process_list):
        print "++ check process: " + ', '.join(process_list)
        ret = True
        for p in process_list:
            if len(self.findPid(p)[1]) == 0:
                print "++ %s not found" % p
                ret = False
            else:
                print "++ found %s" % p
        return ret

    def _hoover(self, x, y):
        self.drag((x, y), (x, y), delayBeforeMoves=-1, delayAfterMoves=-1, movePoints=1)

    def refreshScreenshot(self):
        ret = False
        if self.move_cursor == True:
            if self.maxX != 0:
                print "++ move cursor to %d, %d" % (self.maxX, self.maxY)
                self._hoover(self.maxX, self.maxY)
            ret = fmbttizen.Device.refreshScreenshot(self)
            if self.maxX != 0:
                print "++ move cursor to 0, 0"
                self._hoover(0, 0)
        else:
            ret = fmbttizen.Device.refreshScreenshot(self)
        return ret
            
    def check_call(self, cmd):
        (ret, so, se) = self.shellSOE(cmd)
        if ret != 0:
            print "++ fail to run cmd `%s'" % (cmd)
            print "++ standard output: " + so 
            print "++ standard error:" + se
            raise TizenError("cmd_issue", "fail to run cmd `%s'" % (cmd))
        return so

class cl_app():
    def __init__(self, name, process, controller):
        self.name = name
        self.process = process
        self.controllerImp = controller

class NightModeController():
    def __init__(self, controller):
        self.controllerImp = controller
        self.theme = ""
    
    def refNightMode(self):
        self.theme = ""
        (ret, so, se) = self.controllerImp.shellSOE("amb-get NightMode")
        if ret == 0:
            if '"NightMode": 1' in so:
                self.theme = "night"
            elif '"NightMode": 0' in so:
                self.theme = "day"
        if self.theme:
            print "++ get NightMode successfully, the theme is " + self.theme
        else:
            self.theme = "day"
            print "++ fail to get NightMode, use default theme `%s'" % self.theme
        theme_str = app_icons_str.replace("%theme%", self.theme)
        exec(theme_str)
        print "++ app_icons: %s" % app_icons

    def setNightMode(self, night_mode=True):
        if night_mode:
            pass
        else:
            pass
        self.refNightMode()

class WestonDesktop(cl_app):
    def __init__(self, controller):
        cl_app.__init__(self, "WestonDesktop", "", controller)
        self.night_mode_ctrl = NightModeController(controller)

    def wrt_launch(self, app_name):
        out = self.controllerImp.check_call("wrt-launcher -l")
        for l in out.splitlines():
            if l.find(app_name) != -1:
                app_id = l.split()[-1]
                if app_id.find(".%s" % app_name) == -1:
                    print "++ app_id format is not correct `%s'" % (app_id)
                    return False
                print "++ found app_id `%s'" % (app_id)
                break
        else:
            print "++ not found app_id for %s" % (app_name)
            return False
        self.controllerImp.type("wrt-launcher -s %s\n" % app_id)

    def cmd_launch(self, app_name):
        self.controllerImp.type("%s\n" % app_name)

    def launch_app(self, app_name):
        self.controllerImp.type("launch_app %s\n" % app_name)

    def launch(self, app_name, picture_list=[], process_list=[]):
        if self.controllerImp.refAndTapBitmap("term.icon.png") or \
           self.controllerImp.refAndTapBitmap("term.icon.png"):
            print "++ sucessfully tap western term icon"
        else:
            return False
        # to fetch focus, tricky !!
        self.controllerImp._hoover(self.controllerImp.maxX, self.controllerImp.maxY)

        print "++ proper launch app"
        if app_name in ["saythis", "Settings", "GhostCluster", "MediaPlayer"]:
            self.wrt_launch(app_name)
        elif app_name in ["org.tizen.dialer"]:
            self.launch_app(app_name)
        else:
            self.cmd_launch(app_name)
        print "++ try to refresh screenshot"
        self.controllerImp.refreshScreenshot()
        time.sleep(2)

        if process_list:
            print "++ verify started process..."
            if not self.controllerImp.verifyAllProcess(process_list):
                print "++ expected process not found"
                return False

        if picture_list:
            print "++ verify expected bitmap..."
            if not self.controllerImp.refAndWaitAllBitmap(picture_list):
                print "++ fail to verify bitmap"
                return False

        print "++ launch %s successfully" % (app_name)
        time.sleep(2)
        return True

    def refNightMode(self):
        self.night_mode_ctrl.refNightMode()

class ICOHomeScreen(cl_app):
    def __init__(self, controller):
        cl_app.__init__(self, "homescreen", "", controller)
        self.current_page = 0
        self.app_status = {}
        self.max_page = 3
        self.night_mode_ctrl = NightModeController(controller)
        self.apps = []

    def registerApp(self, app):
        self.apps.append(app)

    def clickApplist(self):
        return self.controllerImp.refAndTapBitmap(app_icons["applist"])
    
    def swipeToWest(self):
        ret = self.controllerImp.swipeToWest()
        if self.current_page < self.max_page - 1:
            self.current_page += 1
        print "++ current page: %d" % self.current_page
        assert(self.current_page < self.max_page)
        return ret

    def swipeToEast(self):
        ret = self.controllerImp.swipeToEast()
        if self.current_page > 0:
            self.current_page -= 1
        print "++ current page: %d" % self.current_page
        assert(self.current_page >= 0)
        return ret

    def swipePages(self, start, end):
        assert start >= 0, "wrong start page %d"  % start
        assert end < self.max_page, "wrong end page %d" % end
        print "++ current_page: %d, start page: %d, end page: %d" \
            % (self.current_page, start, end)
        if start > end:
            for i in range(start - end):
                if not self.swipeToEast():
                    return False
        else:
            for i in range(end - start):
                if not self.swipeToWest():
                    return False
        return True

    def swipeToPage(self, end):
        return self.swipePages(self.current_page, end)

    def swipeToLeftmost(self):
        return self.swipePages(self.current_page, 0)

    def launch(self, app_name, app_icon, picture_list=[], process_list=[]):
        print "++ click applist button"
        if not self.clickApplist():
            print "++ fail to click applist button!"
            return False
        
        first_launch = False
        icon = app_icon
        print "++ try to launch %s" % app_name
        if app_name in self.app_status.keys():
            print "++ %s is already launched" % app_name

            app_page = self.app_status[app_name][0]
            print "++ swipe to app page %d" % app_page
            if not self.swipeToPage(app_page):
                print "++ fail to swipe to the specified page! cur page: %d" \
                    % self.current_page
                return False
            print "++ try to tap the old item"
            if not self.controllerImp.tapItem((self.app_status[app_name])[1]):
                print "++ fail to tap item!"
                return False
        else: # first launch
            print "++ %s is the first launch" % app_name
            first_launch = True
            print "++ swipe to the left most side"
            if not self.swipeToLeftmost():
                print "++ fail to swipe to the left most side!"
                return False

            for i in range(self.max_page):
                print "++ check app page %d" % i
                if self.controllerImp.refreshScreenshot() == None:
                    print "++ fail to refresh screenshot!"
                    return False
                if self.controllerImp.tapBitmap(icon) == True:
                    print "++ found icon " + icon
                    app_item = self.controllerImp._lastScreenshot.findItemsByBitmap(icon)[0]
                    break
                else:
                    print "++ swipe to the next page"
                    if not self.swipeToWest():
                        print "++ fail to swipe to next page!"
                        return False
            else:
                print "++ not found app icon %s" % icon
                if not self.clickApplist():
                    print "++ fail to click applist button!"
                return False
        
        if process_list:
            print "++ verify started process..."
            if not self.controllerImp.verifyAllProcess(process_list):
                print "++ expected process not found"
                return False

        if picture_list:
            print "++ verify expected bitmap..."
            if not self.controllerImp.refAndWaitAllBitmap(picture_list):
                print "++ fail to verify bitmap"
                return False
        
        print "++ launch %s successfully at page %d" % (app_name, self.current_page)
        if first_launch:
            self.app_status[app_name] = [self.current_page, app_item, process_list[0]] 
        time.sleep(2)
        return True

    def clickCloseYes(self, wait_time=1):
        self.controllerImp.tap((0.4, 0.55))
        time.sleep(wait_time)

    def clickCloseNo(self, wait_time=1):
        pass

    def close(self, app_name, process_name):
        def calculateRedClosePosition(item):
            center = item.coords()
            width, height = self.controllerImp.screenSize()
            row = int(float(center[1])/float(height)/0.16)
            col = int(float(center[0])/float(width)/0.3) + 1
            print "++ %s location is: row %d, col %d" %(app_name, row, col)
            y = row * 0.16 
            x = col * 0.3
            return (x,y)

        ret = True
        if app_name in self.app_status.keys():
            pids = self.controllerImp.findPid(process_name)[1]
            if len(pids) == 0:
                print "++ %s closed unexpectedly" %app_name
                return False       

            print "++ click applist button"
            if not self.clickApplist():
                print "++ fail to click applist button!"
                return False

            app_page = self.app_status[app_name][0]
            print "++ swipe to app page %d" % app_page
            if not self.swipeToPage(app_page):
                print "++ fail to swipe to the specified page! cur page: %d" \
                    % self.current_page
                return False

            print "++ try to long tap the center of old item"
            if not self.controllerImp.tapItem(self.app_status[app_name][1], 
                                        tapPos=(0.5, 0.5), long=True, hold=7.0):
                print "++ fail to long tap the old item!"
                return False

            self.controllerImp.tap(calculateRedClosePosition(self.app_status[app_name][1]))
            time.sleep(1)
            self.clickCloseYes()
        else:
            print "++ warning: %s is not launched" % app_name

        time.sleep(1)
        pids = self.controllerImp.findPid(process_name)[1]
        print "++ check process existence: " + process_name
        for i in range(len(pids)):
            print "++ pid: %d" % pids[i]
        if len(pids) != 0:
            print "++ process still exsits, fail to close %s" % app_name
            ret = False
        else:# closed successfully
            print "++ %s closed successfully" %app_name
            self.app_status.pop(app_name)
        return ret

    def closeByKill(self, app_name, process_name):
        ret = True
        pids = self.controllerImp.findPid(process_name)[1]
        print "++ process_name: %s, pids: %s" % (process_name, pids)
        for p in pids:
            cmd = "kill %d" % p
            (r, so, se) =self.controllerImp.shellSOE(cmd)
            if r != 0:
                print "faile to kill pid %d" % pid_list[0]
                ret = False
            time.sleep(1)

        time.sleep(1)
        print "++ check process existence: " + process_name
        pids = self.controllerImp.findPid(process_name)[1]
        print "++ process_name: %s, pids: %s" % (process_name, pids)
        if len(pids) != 0:
            print "++ pid check fail, fail to close %s" % app_name
            ret = False
        else:
            print "++ no process exists"
            try:
                self.app_status.pop(app_name)
            except:
                print "++ expected exception, not in app_status"
                pass
        return ret

    def forceCloseAllApps(self):
        for app in self.apps:
            if app.process:
                self.closeByKill(app.name, app.process)

    def refNightMode(self):
        self.night_mode_ctrl.refNightMode()

class Terminal(cl_app):
    def __init__(self, controller):
        cl_app.__init__(self, "terminal", "weston-term", controller)

    def typeCmd(self, cmd, wait_time=0.5):
        self.controllerImp.type(cmd)
        time.sleep(wait_time)

class Dialer(cl_app):
    def __init__(self, controller):
        cl_app.__init__(self, "dialer", "dialer", controller)

class GhostCluster(cl_app):
    def __init__(self, controller):
        cl_app.__init__(self, "ghostcluster", "GhostCluster", controller)

class TizenError(Exception): 
    def __init__(self, type, details):
        Exception.__init__(self)
        self.type = type
        self.details = details
    def __str__(self):
        return self.type + ', ' + self.details
