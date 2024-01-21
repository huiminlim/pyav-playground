"""This script demuxes and decode ts files and displays them in an imshow window."""
import os
import av
import cv2
import klvdata

# Set directory path of data folder
DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/data"
print(f"Data dir: {DATA_DIR}")

# Set file path of sample file to check
SAMPLE_FILE = f"{DATA_DIR}/Truck_out.ts"

# Open sample file using PyAv
in_stream = av.open(SAMPLE_FILE)
dec_codec_ctx = av.Codec('hevc_cuvid', 'r').create()
for packet in in_stream.demux():
    print(packet)
    if packet.stream.type == "video":
        try:
            for frame in dec_codec_ctx.decode(packet):
                img = frame.to_ndarray(format="bgr24")
                img = cv2.resize(img, (img.shape[1] // 4, img.shape[0] // 4)) # pylint: disable=no-member
                cv2.imshow("", img) # pylint: disable=no-member
                cv2.waitKey(1) # pylint: disable=no-member
        except av.error.EOFError: # pylint: disable=c-extension-no-member
            break
    if packet.stream.type == "data":
        # View data
        for metadata in klvdata.StreamParser(packet.to_bytes()):
            # metadata.structure() # for debugging view
            metadata = metadata.MetadataList()

# Close Codec Context allocated
dec_codec_ctx.close()
in_stream.close()
