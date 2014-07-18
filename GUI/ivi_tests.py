#!/usr/bin/python
import sys
import unittest
import time
import random
import os
import subprocess
import argparse
from functools import partial
import fmbttizen
import ivi_apps

def setupTestConnection():
    print "++ set up new test connection"
    ivi_apps.gHSMgr = ivi_apps.ivi_args.ui
    assert ivi_apps.gHSMgr, "++ incomplete parameters!!!"
    if ivi_apps.gHSMgr == "icoui":
        ivi_apps.device = ivi_apps.fMBTController(rotateScreenshot=-90)
        ivi_apps.hsmgr = ivi_apps.ICOHomeScreen(ivi_apps.device)
    elif ivi_apps.gHSMgr == "westonui":
        ivi_apps.device = ivi_apps.fMBTController(move_cursor=True)
        ivi_apps.hsmgr = ivi_apps.WestonDesktop(ivi_apps.device)
    ivi_apps.hsmgr.refNightMode()

def stopTestConnection():
    print "++ close test connection"
    ivi_apps.device.close()
    ivi_apps.device = ""

class ivi_tests(unittest.TestCase):
    def setUp(self):
        print "++ enter setUp"
        setupTestConnection()

    def tearDown(self):
        print "++ enter tearDown"
        stopTestConnection()

    def testICOHomeScreenIsShown(self):
        self.assertTrue(ivi_apps.hsmgr.controllerImp.refAndVerifyBitmap(ivi_apps.app_icons["applist"]))

    def testWestonDesktopIsShown(self):
        self.assertTrue(ivi_apps.hsmgr.controllerImp.refAndVerifyBitmap("term.icon.png"))

    def testLaunchDialer(self):
        self.assertTrue(ivi_apps.hsmgr.launch("org.tizen.dialer", [ivi_apps.app_icons["dl-main"][0]], ["dialer"]))

    def testLaunchXWalk_colorpg(self):
        self.assertTrue(ivi_apps.hsmgr.launch("xwalk 'http://tzivi_worker02.sh.intel.com/ivi_cont_data/color.jpg'", 
                                              [ivi_apps.app_icons["color.jpg"]],
                                              ["xwalk"]))

def first(iterable, default=None, key=None):
    if key is None:
        for el in iterable:
            if el:
                return el
    else:
        for el in iterable:
            if key(el):
                return el
    return default

def setup_default_arguments(args):
    strict_first = partial(first, key=lambda obj: obj is not None)
    args.device = strict_first([args.device, os.environ.get('IVI_DEVICE_IP'), None])
    args.ui = strict_first([args.ui, os.environ.get('IVI_HOMESCREEN'), 'westonui'])

def parse_args():
    parser = argparse.ArgumentParser(description='Starts Tizen GUI testing.')
    parser.add_argument('--device', '-D', default=None,
                        help='device name: "root@ivi-box".')
    parser.add_argument('--ui', '-U', default=None,
                        help='homescreen manager: westonui, icoui.')
    parser.add_argument('unittest_args', nargs='*')
    return parser.parse_args()

if __name__ == "__main__":
    ivi_apps.ivi_args = parse_args()
    setup_default_arguments(ivi_apps.ivi_args)

    if not (ivi_apps.ivi_args.device and ivi_apps.ivi_args.ui):
        print "++ incomplete parameters!!!"
        sys.exit(1)

    sys.argv[1:] = ivi_apps.ivi_args.unittest_args
    print ivi_apps.ivi_args.unittest_args
    unittest.main()
