#!/bin/bash

set -e
resdir=~
resfile=$resdir/GUI.testkit.result.xml

echo '## execution script: preparing environment'
rm -rf $resdir/*.result.xml

timeout 3600 testkit-lite -f /usr/share/tests/ivi/ivi-sanity-suite/GUI/testkit.xml --comm tizenivi --deviceid root@TEST_DEVICE_IP -o $resfile

echo '## execution script: finished'
