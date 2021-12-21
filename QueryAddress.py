
#    Copyright (c) 2021 Christian Carlowitz <chca@cmesh.de>
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
from javax.swing import JOptionPane

class AddrQuery(jmri.ProgListener):
    def __init__(self, prg):
        self.prg = prg
        self.misscnt = 0
        self.cur = 0
        self.qregs = (1,29,17,18)
        self.regs = {}
        
    def startQuery(self):
        self.prg.readCV(str(self.qregs[self.cur]), self)
        
    def programmingOpReply(self, value, status):
        if status != jmri.ProgListener.OK:
            JOptionPane.showMessageDialog(None, "failed reading register %d" % self.reg)
            return
        self.regs[self.qregs[self.cur]] = value
        self.cur += 1
        if self.cur < len(self.qregs):
            self.startQuery()
        else:
            self.analyze()
        
    def analyze(self):
        s = "short address (1): %d\n" % self.regs[1]
        r29 = self.regs[29]
        s += "flags (29): \n" +  \
            "    direction: " + ("reversed" if (r29&1) else "normal") + "\n" + \
            "    speed: " + ("28/128" if (r29&2) else "14") + "\n" + \
            "    DC: " + ("yes (DCC+DC)" if (r29&4) else "no (DCC only)") + "\n" + \
            "    BiDi: " + ("yes" if (r29&8) else "no") + "\n" + \
            "    speed: " + ("curve" if (r29&16) else "min/mid/max") + "\n" + \
            "    address: " + ("long" if (r29&32) else "short") + "\n" + \
            "    type: " + ("accessory" if (r29&128) else "multi") + "\n"
        r17 = self.regs[17]
        r18 = self.regs[18]
        valid = (r17 >> 6) == 0b11
        longAddr = ((r17 & 0b111111) << 8) + r18
        longActive = (r29&32)
        s += ("long address (17/18): %d, " % longAddr) \
            + ("valid" if valid else "invalid")
            
        pre = "address: %d\n\n" % (longAddr if longActive else self.regs[1])
                        
        JOptionPane.showMessageDialog(None, pre+s)
        print "QueryAddress: done"

prg = jmri.InstanceManager.getDefault(jmri.GlobalProgrammerManager).getGlobalProgrammer()
qry = AddrQuery(prg)
qry.startQuery()

print "QueryAddress: started query"
