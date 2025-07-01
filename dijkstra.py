from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr

log = core.getLogger()

class FailoverController(EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.info("Failover Controller initialized")

    def _handle_ConnectionUp(self, event):
        log.info("Switch %s has connected", dpidToStr(event.dpid))
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match()
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)

def launch():
    core.registerNew(FailoverController)
