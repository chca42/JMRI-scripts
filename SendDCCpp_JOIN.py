
#    Copyright (c) 2021 Christian Carlowitz <chca@cmesh.de>
#    based on JMRI jython/SendDCCppMessages.py
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import jmri
import java

whichDCCppConnection = 0; #which DCCpp connection to use if multiples (0 is 1st connection, 1 is 2nd, etc.)

class PeerListener (jmri.jmrix.dccpp.DCCppListener) :
    def message(self, msg):
        return

# function to send a string message to the DCCpp connection
def send(strMessage) :
    m = jmri.jmrix.dccpp.DCCppMessage.makeMessage(strMessage)
    tc.sendDCCppMessage(m, dl)

# get the DCCpp connection stuff once
dc = jmri.InstanceManager.getList(jmri.jmrix.dccpp.DCCppSystemConnectionMemo).get(whichDCCppConnection);
tc = dc.getDCCppTrafficController()
pl = PeerListener()
dl = tc.addDCCppListener(0xFF, pl)
    
send("1 JOIN")               # Join Main and Prog Track
print "DCC++ JOIN Enabled "

tc.removeDCCppListener(0xFF, pl)

