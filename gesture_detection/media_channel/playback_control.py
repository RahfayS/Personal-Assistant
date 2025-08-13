import subprocess

def toggle_play_pause():
    '''
    Pauses any google chrome application
    '''
    script = '''
    tell application "Google Chrome" to activate
    delay 0.1
    tell application "System Events" to keystroke " "  -- spacebar
    '''
    subprocess.call(['osascript', '-e', script])
