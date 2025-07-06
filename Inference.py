import serial
import time
import cv2
from yoloDet import YoloTRT
import subprocess
subprocess.run(["sudo", "chmod", "666", "/dev/ttyTHS1"])

# Inisialisasi Serial ke Teensy 4.1
serialTeensy = serial.Serial('/dev/ttyTHS1', 115200, timeout=1)
time.sleep(2)  # Tunggu agar port serial siap

# Load model YOLO TensorRT
model = YoloTRT(library="yolov5/build/libmyplugins.so",
                engine="yolov5/build/yolov5n_3Class.engine",
                conf=0.1, yolo_ver="v5")
category = ["Dummy", "Korban", "Turu"]

# Fungsi pipeline CSI Camera (sama seperti sebelumnya)
def gstreamer_pipeline(sensor_id=0, capture_width=640, capture_height=480,
                       display_width=640, display_height=480, framerate=30):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=%d, height=%d, framerate=%d/1, format=NV12 ! "
        "nvvidconv flip-method=0 ! queue max-size-buffers=1 leaky=downstream ! "
        "video/x-raw, width=%d, height=%d, format=BGRx ! "
        "videoconvert ! video/x-raw, format=BGR ! "
        "appsink sync=false max-buffers=1 drop=true max-lateness=0"
        % (sensor_id, capture_width, capture_height, framerate, display_width, display_height)
    )

cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

# Kirim sinyal siap (1 byte) ke Teensy
serialTeensy.write(b'\x01')
print("Jetson Nano Ready...")

while True:
    ret, frame = cap.read()
    # Jika ada permintaan data dari Teensy
    if serialTeensy.in_waiting > 0:
        # Baca string class_choice dari Teensy
        class_choice_str = serialTeensy.readline().decode('utf-8').strip()
        try:
            class_choice = int(class_choice_str)  # Konversi ke integer
        except ValueError:
            print(f"Invalid class_choice received: {class_choice_str}")
            continue  # Lewati loop jika format tidak valid

        if class_choice < len(category):
            result = model.Inference(frame)
            for obj in result:
                if obj["class"] == category[class_choice]:
                    bbox = obj["box"]
                    xcenter = int((bbox[0] + bbox[2]) / 2)
                    ycenter = int((bbox[1] + bbox[3]) / 2)

                    # Siapkan data dalam format string: "xcenter,ycenter\n"
                    data_str = f"{xcenter},{ycenter}\n"
                    serialTeensy.write(data_str.encode('utf-8'))
        else:
            print(f"Nilai class_choice ({class_choice}) tidak valid.")
    
    cv2.imshow("CSI Camera", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
serialTeensy.close()

