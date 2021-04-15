import logging
import coloredlogs
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtsp', '1.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gst, GstRtsp, GObject, GLib
from rtsp_gst.bus import BUS_HANDLERS
from rtsp_gst.classes import RTSP_CONFIG

Gst.init(None)


# https://lazka.github.io/pgi-docs/GstRtsp-1.0/mapping.html

class GST_RTSP_PLAYER(BUS_HANDLERS):
    
    def __init__(self, rtspsrc_config=RTSP_CONFIG(), decoder="avdec_h264", sink="autovideosink", loglevel="INFO", restart_on_error=False):
        self.rtspsrc_config = rtspsrc_config
        self.decoder_arg = decoder
        self.sink_arg = sink
        self.jitterbuffer_stats = None
        self.state = None
        self.tags = None
        self.fps = None
        self.identity_buffer = None
        self.rtpbin_stats = None
        self.rtsp_video_caps = None
        self.restart_on_error = restart_on_error
        self.loop = GLib.MainLoop()
        self.create_pipeline()
        self.connect_element_signals()
        coloredlogs.install(level=loglevel)
        logging.info("RTSP Player started...")
        
    def convert_arg_to_element(self, arg):
        if type(arg) == str:
            return Gst.ElementFactory.make(arg)
        else:
            return arg
        
    def connect_element_signals(self):
        self.rtspsrc.connect('pad-added', self.on_pad_added)
        self.rtspsrc.connect("new-manager", self.on_new_manger)
        self.identity.connect("handoff", self.on_handoff)    
        
    def create_pipeline(self):
        self.pipeline = Gst.Pipeline()
        self.connect_bus()
        
        # rtspsrc 
        self.rtspsrc = Gst.ElementFactory.make('rtspsrc')
        self.rtspsrc.set_property('location', self.rtspsrc_config.location)
        self.rtspsrc.set_property('latency', self.rtspsrc_config.latency)
        self.rtspsrc.set_property('protocols', self.rtspsrc_config.protocols)
        self.rtspsrc.set_property('user-id', self.rtspsrc_config.user_id)
        self.rtspsrc.set_property('user-pw', self.rtspsrc_config.user_pw)
        
        # rtph264depay
        self.rtph264depay = Gst.ElementFactory.make("rtph264depay")
        
        # h264parse
        self.h264parse = Gst.ElementFactory.make("h264parse")
        
        # identity
        self.identity = Gst.ElementFactory.make("identity")
        
        # decoder 
        self.decoder = self.convert_arg_to_element(self.decoder_arg)
        
        # videoconvert 
        self.videoconvert = Gst.ElementFactory.make('videoconvert')
        
        # sink 
        self.sink = self.convert_arg_to_element(self.sink_arg)
        
        self.pipeline.add(self.rtspsrc)
        self.pipeline.add(self.rtph264depay)
        self.pipeline.add(self.h264parse)
        self.pipeline.add(self.identity)
        self.pipeline.add(self.decoder)
        self.pipeline.add(self.videoconvert)
        self.pipeline.add(self.sink)
        
        self.rtph264depay.link(self.h264parse)
        self.h264parse.link(self.identity)
        self.identity.link(self.decoder)
        self.decoder.link(self.videoconvert)
        self.videoconvert.link(self.sink)
        
    def connect_bus(self):
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::error', self.on_error, self)
        self.bus.connect('message::state-changed', self.on_status_changed)
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::qos', self.on_qos)
        self.bus.connect('message::info', self.on_info)
        self.bus.connect('message::stream-status', self.on_stream_status)
        self.bus.connect('message::tag', self.on_tag)  
        self.bus.connect('message::element', self.on_element) 
        
    def play(self): 
        logging.info(f"PLAY {self.rtspsrc_config.location}")
        self.pipeline.set_state(Gst.State.PLAYING) 
        self.loop.run()
        
    def stop(self):
        logging.info(f"STOP {self.rtspsrc_config.location}")
        self.pipeline.set_state(Gst.State.NULL)
        self.loop.quit()
