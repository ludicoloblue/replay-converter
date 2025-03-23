import os
import time
import pyppeteer
import pyautogui
import moviepy.editor as mpy
import asyncio

async def capture_replay(html_file_path, output_video_path, duration):
    # Set up headless browser using pyppeteer
    browser = await pyppeteer.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    
    # Open the HTML file in the browser
    await page.goto(f"file://{os.path.abspath(html_file_path)}")
    
    # Wait for the replay to load (adjust if needed)
    await asyncio.sleep(5)
    
    # Play the replay
    play_button = await page.querySelector('.playbutton')
    await play_button.click()

    # Capture the screen for the duration of the replay
    frames = []
    start_time = time.time()
    while time.time() - start_time < duration:
        screenshot = await page.screenshot()
        frames.append(screenshot)
        await asyncio.sleep(1 / 30)  # Capture at 30 fps

    # Close the browser
    await browser.close()

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

    asyncio.get_event_loop().run_until_complete(capture_replay(html_file_path, output_video_path, duration))
