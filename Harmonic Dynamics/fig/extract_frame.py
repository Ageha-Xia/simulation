from PIL import Image, ImageSequence
import os


def save_last_frame_as_jpg(directory):
    # 获取目录中所有的.gif文件
    gif_files = [f for f in os.listdir(directory) if f.endswith('.gif')]

    for gif_file in gif_files:
        with Image.open(os.path.join(directory, gif_file)) as img:
            # 获取帧数
            frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
            # 获取最后一帧
            last_frame = frames[-1]
            # 保存为.jpg
            jpg_filename = os.path.splitext(gif_file)[0] + '.jpg'
            last_frame = last_frame.convert('RGB')
            last_frame.save(os.path.join(directory, jpg_filename), 'JPEG')

if __name__ == "__main__":
    # 获取当前工作目录
    print(os.getcwd())
    directory = input("请输入目录路径: ")
    save_last_frame_as_jpg(directory)
