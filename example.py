from rtsp_gst import GST_RTSP_PLAYER, RTSP_CONFIG, GstRtsp, Gst

if __name__ == '__main__':
    grp = GST_RTSP_PLAYER(
        rtspsrc_config = RTSP_CONFIG(
            location = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov",
            latency = 300,
            protocols = GstRtsp.RTSPLowerTrans.UDP
            #protocols = GstRtsp.RTSPLowerTrans.TCP
        ),
        restart_on_error = True
        # decoder = Gst.ElementFactory.make("d3d11videosink")
        # decoder = d3d11videosink
        # sink = Gst.ElementFactory.make("avdec_h264")
        # sink = avdec_h264
    )
    grp.play()
