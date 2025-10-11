
class SecurityCamera:
    def __init__(self, camera_id, location, resolution, is_recording):
        self.camera_id = camera_id
        self.location = location
        self.resolution = resolution
        self.is_recording = is_recording
        self.footage = []

    def start_recording(self):
        """Начать запись"""
        self.is_recording = True
        return "Recording started"

