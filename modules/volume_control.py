import keyboard

class VolumeControl:
    def increase_volume(self):
        """Simulate pressing the volume up key."""
        keyboard.press_and_release("volume up")

    def decrease_volume(self):
        """Simulate pressing the volume down key."""
        keyboard.press_and_release("volume down")

    def mute_volume(self):
        """Simulate pressing the mute key."""
        keyboard.press_and_release("volume mute")
        
    def unmute_volume(self):
        """Unmute the volume (same key as mute)."""
        keyboard.press_and_release("volume mute")
