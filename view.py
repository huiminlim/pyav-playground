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

# Open sample file using PyAv
stream = av.open(SAMPLE_FILE)
codec = av.Codec('h264_cuvid', 'r').create()
for packet in stream.demux():
    # print(packet)
    if packet.stream.type == "video":
        try:
            for img in codec.decode(packet):
                img = img.to_ndarray(format="bgr24")
                img = cv2.resize(img, (img.shape[1] // 4, img.shape[0] // 4)) # pylint: disable=no-member
                cv2.imshow("", img) # pylint: disable=no-member
                cv2.waitKey(1) # pylint: disable=no-member
        except av.error.EOFError: # pylint: disable=c-extension-no-member
            break
    if packet.stream.type == "data":
        for metadata in klvdata.StreamParser(packet.to_bytes()):
            # metadata.structure() # for debugging view
            metadata = metadata.MetadataList()
