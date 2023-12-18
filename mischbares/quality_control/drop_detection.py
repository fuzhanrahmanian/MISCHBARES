import time
import cv2
import numpy as np

from mischbares.logger import logger
from mischbares.config.main_config import config

log = logger.get_logger("quality_control.drop_detection")
config = config['QC']['waste_camera']

class DropDetection:
    def __init__(self, timeout=None) -> None:
        self.drop_detected = False
        self.timeout = config["timeout"] if timeout is None else timeout
        self.got_timeout_error = False

    def analyze_video_dynamic_roi(self):
        # Access the webcam

        cap = cv2.VideoCapture(config["camera_num"])
        if not cap.isOpened():
            log.info("Error: Camera not accessible.")
            return
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_time = int(1000 / fps)
        # Read the first frame to get ROI
        ret, first_frame = cap.read()
        if not ret:
            cap.release()
            raise Exception("Error: Cannot read from camera.")
        height, width, _ = first_frame.shape

        # Define ROI around the center of the video
        roi_size = 100  # Square ROI of 100x100 pixels
        x1 = (width - roi_size) // 2 + config["offset_x"]
        y1 = (height - roi_size) // 2 + config["offset_y"]
        x2 = x1 + roi_size
        y2 = y1 + roi_size
        self.drop_detected = False
        start_time = time.time()
        first_roi = cv2.cvtColor(first_frame[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)
        first_roi = cv2.GaussianBlur(first_roi, (21, 21), 0)

        while True:
            ret, frame = cap.read()
            if not ret:
                log.info("Stream ended.")
                break

            # Current ROI frame
            roi = frame[y1:y2, x1:x2]
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray_roi = cv2.GaussianBlur(gray_roi, (21, 21), 0)

            if not self.drop_detected:
                # Compute the absolute difference between the current and first frame
                frame_delta = cv2.absdiff(first_roi, gray_roi)
                threshold_delta = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

                roi_color = (0, 255, 0)  # Green by default
                annotation = "Monitoring..."

                # Update motion detection status
                if np.sum(threshold_delta) > 0:
                    self.drop_detected = True
                    drop_detected_time = time.time()
                    roi_color = (0, 0, 255)  # Red when motion detected
                    annotation = "Drop detected. Discharging..."

            cv2.putText(frame, annotation, (x1+40, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), roi_color, 2)
            # Display remaing seconds to timeout
            cv2.putText(frame, f"Timeout: {round(self.timeout - (time.time() - start_time), 1)} s", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # Display frame
            cv2.imshow('Frame', frame)

            # Wait for delay seconds after drop detection, then break
            if self.drop_detected and (time.time() - drop_detected_time) > config["delay"]:
                break

            if not self.drop_detected and (time.time() - start_time) > self.timeout:
                self.got_timeout_error = True
                break

            # Press 'q' to exit immediately
            if cv2.waitKey(frame_time) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


    def trigger_timeout_error(self):
        """Trigger a timeout error."""
        raise TimeoutError("This is a test error.")


    def get_drop_detection_status(self) -> bool:
        """Get the drop detection status"""
        return self.drop_detected