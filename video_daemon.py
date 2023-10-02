import subprocess
import time

while True:
    try:
        result = subprocess.run(['python', 'video_pygame.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Script exited with error, restarting after 5 seconds. Error: {e}')
        time.sleep(5)
    else:
        print('Script completed successfully. Not restarting.')
        break
