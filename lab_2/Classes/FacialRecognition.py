import BiometricScanner

class FacialRecognition(BiometricScanner):
    def __init__(self, scanner_id, accuracy, is_enabled, recognition_speed):
        super().__init__(scanner_id, "facial", accuracy, is_enabled)
        self.recognition_speed = recognition_speed
        self.mask_detection = True

    def recognize_face(self):
        """Распознать лицо"""
        return "Face recognized"
