import os
import time
import pyautogui
import moviepy.editor as mpy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def capture_replay(html_file_path, output_video_path, duration):
    # Set up headless Chrome browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)

    # Open the HTML file in the browser
    driver.get(f"file://{os.path.abspath(html_file_path)}")

    # Wait for the replay to load (adjust if needed)
    time.sleep(5)

    # Play the replay
    play_button = driver.find_element_by_css_selector(".playbutton")
    play_button.click()

    # Capture the screen for the duration of the replay
    frames = []
    start_time = time.time()
    while time.time() - start_time < duration:
        frame = pyautogui.screenshot()
        frames.append(frame)
        time.sleep(1 / 30)  # Capture at 30 fps

    # Close the browser
    driver.quit()

    # Convert frames to video
    video_clips = [mpy.ImageClip(frame).set_duration(1 / 30) for frame in frames]
    video = mpy.concatenate_videoclips(video_clips, method="compose")
    video.write_videofile(output_video_path, fps=30)

if __name__ == "__main__":
    # Path to the Pokémon Showdown replay HTML file
    html_file_path = "path/to/replay.html"
    
    # Path to save the output MP4 video
    output_video_path = "output_video.mp4"
    
    # Duration of the replay in seconds (adjust as needed)
    duration = 120  # 2 minutes

    capture_replay(html_file_path, output_video_path, duration)