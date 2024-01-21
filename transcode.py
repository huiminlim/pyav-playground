"""This script demuxes and decode ts files and displays them in an imshow window."""
import os
import av
import cv2
import klvdata

# Set directory path of data folder
DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/data"
print(f"Data dir: {DATA_DIR}")

# Set file path of sample file to check
SAMPLE_FILE = f"{DATA_DIR}/Truck.ts"
OUTPUT_FILE = f"{DATA_DIR}/Truck_out.ts"

# Open sample file using PyAv
in_stream = av.open(SAMPLE_FILE)
print(in_stream.streams.data)
out_stream = av.open(OUTPUT_FILE, "w", format='mpegts')
out_stream.add_stream("hevc_nvenc")
data_stream_idx = out_stream.add_stream(template=in_stream.streams.data[0])
dec_codec_ctx = av.Codec('h264_cuvid', 'r').create()
enc_codec_ctx = av.Codec('hevc_nvenc', 'w').create()
enc_codec_ctx.pix_fmt = "yuv420p"
enc_codec_ctx.width = 1920
enc_codec_ctx.height = 1080
enc_codec_ctx.time_base = "1001/30000"
enc_codec_ctx.framerate = 1 / enc_codec_ctx.time_base
for packet in in_stream.demux():
    # print(packet)
    if packet.stream.type == "video":
        try:
            for frame in dec_codec_ctx.decode(packet):
                img = frame.to_ndarray(format="bgr24")
                img = cv2.resize(img, (img.shape[1] // 4, img.shape[0] // 4)) # pylint: disable=no-member
                cv2.imshow("", img) # pylint: disable=no-member
                cv2.waitKey(1) # pylint: disable=no-member

                # Attempt encoding
                for enc_pkt in enc_codec_ctx.encode(frame):
                    out_stream.mux(enc_pkt)
                    pass

        except av.error.EOFError: # pylint: disable=c-extension-no-member
            break
    if packet.stream.type == "data":
        # View data
        for metadata in klvdata.StreamParser(packet.to_bytes()):
            # metadata.structure() # for debugging view
            metadata = metadata.MetadataList()

        # Mux into stream
        packet.stream = data_stream_idx
        out_stream.mux(packet)

# Close Codec Context allocated
dec_codec_ctx.close()
enc_codec_ctx.close()
in_stream.close()
out_stream.close()
