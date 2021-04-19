from rtsp_gst import GST_RTSP_PLAYER, RTSP_CONFIG, GstRtsp, Gst
import time
from dataclasses import asdict
import sys

from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        self.grp.socket_io = self
        self.grp.start()
        self.grp.play()
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        # echo back message verbatim

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory("ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol
    grp = GST_RTSP_PLAYER(
        rtspsrc_config = RTSP_CONFIG(
            location = "rtsp://ADMIN:1234@88.117.204.110:5554/live/second0",
            latency = 300,
            protocols = GstRtsp.RTSPLowerTrans.UDP,
            name ="Stream1",
            id = 0
        ),
        restart_on_error = False,
        socket_io = None,
    )
    factory.protocol.grp = grp
    reactor.listenTCP(9000, factory)
    reactor.run()