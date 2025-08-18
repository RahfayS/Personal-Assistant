import subprocess
import pyautogui

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


def youtube_skip(hand_label):
    if hand_label == 'Left':  # swipe right
        pyautogui.press('right')  # skip forward 5s
    elif hand_label == 'Right':  # swipe left
        pyautogui.press('left')   # skip backward 5s