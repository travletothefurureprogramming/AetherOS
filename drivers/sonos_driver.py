from soco import SoCo
from drivers.base_device import BaseDevice

class SonosSpeaker(BaseDevice):
    def __init__(self, device_id, dev_type, ip):
        super().__init__(device_id, dev_type, ip)


        self.device = SoCo(ip)

    async def play(self):
        self.device.play()
        return f"Successfully played media on the device: {self.device_id}"

    async def pause(self):
        self.device.pause()
        return f"Successfully paused media on the device: {self.device_id}"

    async def stop(self):
        self.device.stop()
        return f"Successfully stopped media on the device: {self.device_id}"

    async def volume_up(self):
        self.device.volume += 1
        return f"Successfully increased volume on the device: {self.device_id}"

    async def volume_down(self):
        self.device.volume -= 1
        return f"Successfully decreased volume on the device: {self.device_id}"

    async def mute(self):
        self.device.mute = not self.device.mute
        status = "muted" if self.device.mute else "unmuted"
        return f"Successfully {status} the device: {self.device_id}"

    async def next(self):
        self.device.next()
        return f"Successfully skipped to next track on the device: {self.device_id}"

    async def previous(self):
        self.device.previous()
        return f"Successfully skipped to previous track on the device: {self.device_id}"

    async def get_track_info(self):
        track = self.device.get_current_track_info()

        return {
            "title": track.get('title', 'Unknown'),
            "artist": track.get('artist', 'Unknown'),
            "album": track.get('album', 'Unknown')
        }