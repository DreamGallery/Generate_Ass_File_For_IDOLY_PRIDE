import cv2, cv2.typing
import os, sys
import threading
from src.read_ini import config
from src.match import to_binary_adaptive
from concurrent.futures import ThreadPoolExecutor, wait


_CACHE_PATH = config.get("File PATH", "CACHE_PATH")
_VIDEO_PATH = config.get("File PATH", "VIDEO_PATH")

_lock = threading.Lock()
_current_count = int(0)


class FrameProcess(object):
    fps: float

    def one_task(
        self,
        image_folder_path: str,
        frame: cv2.typing.MatLike,
        width: int,
        height: int,
        milliseconds: float,
        total_fps: int,
    ) -> None:
        global _current_count
        seconds = "%.4f" % (milliseconds // 1000 + (milliseconds % 1000) / 1000)
        name = seconds[:-1].replace(".", "_")
        # Modify the following content if your resolution ratio is not 16:9
        img = frame[
            (height * 29 // 36) : (height * 8 // 9),
            (width * 1 // 16) : (width * 15 // 16),
        ]
        image_path = f"{image_folder_path}/{name}.png"
        binary = to_binary_adaptive(cv2.UMat(img), 11, 0)
        kernel = cv2.UMat(cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
        binary_opn = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        cv2.imwrite(image_path, binary_opn)
        _lock.acquire()
        _current_count += 1
        percent = round(_current_count / total_fps * 100)
        print(
            f"\rPre-Progress:({_current_count}/{total_fps})" + "{}%: ".format(percent),
            "▓" * (percent // 2),
            end="",
        )
        sys.stdout.flush()
        _lock.release()

    def to_frame(self, input: str) -> None:
        image_folder_path = f"{_CACHE_PATH}/{input.split('.')[0]}"
        os.makedirs(image_folder_path, exist_ok=True)
        video_path = f"{_VIDEO_PATH}/{input}"
        vc = cv2.VideoCapture(video_path)
        self.fps = vc.get(cv2.CAP_PROP_FPS)
        width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_fps = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))
        executor = ThreadPoolExecutor(max_workers=20)
        frame_tasks = []
        while vc.isOpened():
            status, frame = vc.read()
            if not status:
                break
            milliseconds = vc.get(cv2.CAP_PROP_POS_MSEC)
            frame_tasks.append(
                executor.submit(
                    self.one_task, image_folder_path, frame, width, height, milliseconds, total_fps
                )
            )
        vc.release()
        wait(frame_tasks, return_when="ALL_COMPLETED")
        print("\u0020", "Pre-Progress finished")

    def get_fps(self, input: str) -> None:
        video_path = f"{_VIDEO_PATH}/{input}"
        vc = cv2.VideoCapture(video_path)
        self.fps = vc.get(cv2.CAP_PROP_FPS)
