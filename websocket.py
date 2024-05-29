import asyncio
from datetime import datetime
from os import path
import cv2
import pyautogui
import websockets

CAMERA_PORT = 0


def get_mouse_coords():
    x, y = pyautogui.position()
    return x, y


async def send_mouse_coords(websocket):
    while True:
        mouse_pos = get_mouse_coords()
        await websocket.send(str(mouse_pos))
        await asyncio.sleep(0.01)


def capture_image(img_path, camera_port):
    camera = cv2.VideoCapture(camera_port)
    ret, frame = camera.read()
    if not ret:
        raise Exception('Cannot read from camera.')

    cv2.imwrite(img_path, frame)
    encoded, buffer = cv2.imencode('.png', frame)
    return buffer


async def on_mouse_click(websocket):
    while True:
        data = await websocket.recv()
        path_join = path.join(__file__, f'image/{datetime.now().isoformat()}.png')
        photo = capture_image(path_join, CAMERA_PORT)
        print(f'Image captured to path {path_join}')
        #TODO: save coords to DB
        await asyncio.sleep(0.01)


async def service(websocket):
    loop = asyncio.get_event_loop()
    mouse_coords_task = loop.create_task(send_mouse_coords(websocket))
    mouse_click_task = loop.create_task(on_mouse_click(websocket))
    await asyncio.wait([mouse_coords_task, mouse_click_task])


def main():
    start_server = websockets.serve(service, 'localhost', 8000)
    print(f'Websocket server started at http://localhost:8000')

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()