from dataclasses import dataclass 
import time
import collections
from enum import Enum

from rtsp_gst import GstRtsp

@dataclass
class RTSP_CONFIG():
    """
        rtspsrc element props
    """
    location: str = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
    latency: int = 200
    protocols: int = GstRtsp.RTSPLowerTrans.UDP
    user_id: str = ""
    user_pw: str = ""
    name: str = "Default Stream 1"
    id: int = 0

class STATE(Enum):
    """
        VOID_PENDING     no pending state.
        NULL             the None state or initial state of an element.
        READY            the element is ready to go to PAUSED.
        PAUSED           the element is PAUSED, it is ready to accept and process data. Sink elements however only accept one buffer and then block.
        PLAYING          the element is PLAYING, the Gst.Clock is running and the data is flowing.
    """
    VOID_PENDING = 0
    NULL = 1
    READY = 2
    PAUSED = 3
    PLAYING = 4
    
    def __str__(self):
        return str(self.name)


@dataclass
class X_RTP_BIN_STATS:
    """
        RTP BIN Stats
    """
    base_time: int
    sr_ext_rtptime: int
    clock_rate: int
    base_rtptime: int

@dataclass
class X_RTP_JITTERBUFFER_STATS:
    """
        num-pushed          the number of packets pushed out.
        num-lost            the number of packets considered lost.
        num-late            the number of packets arriving too late.
        num-duplicates      the number of duplicate packets.
        avg-jitter          the average jitter in miliseconds.
        rtx-count           the number of retransmissions requested.
        rtx-success-count   the number of successful retransmissions.
        rtx-per-packet      average number of RTX per packet.
        rtx-rtt             average round trip time per RTX. 
        x_rtp               X_RTP_BIN_STATS dataclass
    """
    num_pushed: int
    num_lost: int
    num_late: int
    num_duplicates: int
    avg_jitter: int
    rtx_count: int
    rtx_success_count: int
    rtx_per_packet: int
    rtx_rtt: int
    x_rtp: X_RTP_BIN_STATS

@dataclass
class BUFFER:
    """
        dts	int	    decoding timestamp of the buffer, can be Gst.CLOCK_TIME_NONE when the dts is not known or relevant. The dts contains the timestamp when the media should be processed.
        duration	duration in time of the buffer data, can be Gst.CLOCK_TIME_NONE when the duration is not known or relevant.
        offset      a media specific offset for the buffer data. For video frames, this is the frame number of this buffer. For audio samples, this is the offset of the first sample in this buffer. For file data or compressed data this is the byte offset of the first byte in this buffer.
        offset_end  the last offset contained in this buffer. It has the same format as offset.
        pts	        presentation timestamp of the buffer, can be Gst.CLOCK_TIME_NONE when the pts is not known or relevant. The pts contains the timestamp when the media should be presented to the user.
    """
    dts: int
    duration: int
    offset: int
    offset_end: int
    pts: int
    data: bytes

@dataclass
class STATE_CHANGE:
    """
        oldstate	the previous state, or None
        newstate	the new (current) state, or None
        pending	the pending (target) state, or None
    """
    oldstate: str
    newstate: str
    pending: str
    
@dataclass
class TAGS:
    """
        Tags Stats
    """
    bitrate: int
    min_bitrate: int
    max_bitrate: int
    codec: str
    src: str
    
@dataclass
class RTSP_CAPS:
    """
        RTSP Caps
    """
    payload: int
    clock_rate: int
    packetization_mode: str
    encoding_name: str
    profile_level_id: str
    framesize: str
    framerate: float
    frame_height: int
    frame_width: int

class FPS_CALCULATOR:
    """
        Calculate avg fps
    """
    def __init__(self,avarageof=50):
        self.frametimestamps = collections.deque(maxlen=avarageof)
    
    def __call__(self):
        self.frametimestamps.append(time.time())
        if(len(self.frametimestamps) > 1):
            return round(len(self.frametimestamps)/(self.frametimestamps[-1]-self.frametimestamps[0]))
        else:
            return 0.0
