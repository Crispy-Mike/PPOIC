import BiometricScanner

class FingerprintScanner(BiometricScanner):
    def __init__(self, scanner_id, accuracy, is_enabled, resolution):
        super().__init__(scanner_id, "fingerprint", accuracy, is_enabled)
        self.resolution = resolution
        self.false_accept_rate = 0.001

    def scan_fingerprint(self):
        return "Fingerprint scanned"
