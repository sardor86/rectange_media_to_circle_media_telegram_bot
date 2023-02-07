import cv2
from math import sqrt


async def video_redactor(img_path: str, video_path: str, result: str) -> str:
    cap = cv2.VideoCapture(video_path)

    frame_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    cap2 = cv2.VideoWriter(result, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 20, (width, height))

    photo = cv2.resize(cv2.imread(img_path), (width, height))

    for i in range(frame_number):
        ret, frame = cap.read()
        for x in range(width):
            for y in range(height):
                if not (sqrt((width//2 - x)**2 + (height//2 - y)**2) <= height//2):
                    frame[y, x] = photo[y, x]
        cap2.write(frame)
