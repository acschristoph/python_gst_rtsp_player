# python_gst_rtsp_player

Python Rtsp Player with Gstreamer that can messaure fps/bitrate and other internal stuff.

![enter image description here](https://i.imgur.com/dpQ7Q4d.png)

**Example Usage:**

    from rtsp_gst import GST_RTSP_PLAYER, RTSP_CONFIG, GstRtsp
    grp = GST_RTSP_PLAYER(
        rtspsrc_config = RTSP_CONFIG(
            location = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov",
            latency = 300,
        ),
        restart_on_error = True
    )
    grp.play()

## Player arguments
***rtspsrc_config***  RTSP_CONFIG (Dataclass)
***decoder***  Gstreamer decoder element as string or Gst-Element (Default: avdec_h264)
***sink***  Gstreamer sink element as string or Gst-Element  (Default: autovideosink)
***loglevel*** Loglevel (Default: INFO)
***restart_on_error*** Restart in case of error (Default: False)


### RTSP_CONFIG (Dataclass)
[Gstreamer rtspsrc documentation.](https://gstreamer.freedesktop.org/documentation/rtsp/rtspsrc.html?gi-language=c)
[Gtreamer RTSP flags documnetation](https://lazka.github.io/pgi-docs/GstRtsp-1.0/flags.html#GstRtsp.RTSPLowerTrans) 

***location***  RTSP Stream location (default: *demo stream*)
***latency***  RTSP Stream latency  (default: *200*)
***protocols***  RTSP Stream protocols  (default: *GstRtsp.RTSPLowerTrans.UDP*)
***user_id***  RTSP Stream Authentication Username  (default: *""*)
***user_pw***  RTSP Stream Authentication Password (default: *""*)

    from rtsp_gst import RTSP_CONFIG
    
    RTSP_CONFIG( 
       location = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov", 
       latency = 500, 
    )
