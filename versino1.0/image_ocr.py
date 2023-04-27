
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from multiprocessing import Pool as Pool
import time
import requests


class OcrImage:
    def __init__(self, image, box, text):
        self.box = box
        self.image = image
        self.text = text
        self.number = 0

    def cover(self, box):
        # print(box)
        # print("cover")
        # 坐标 position (x,y) 顺序为 左上/右上/右下/左下
        x2y1 = box[0]
        x1y2 = box[1]
        # 细化坐标
        x1 = int(x1y2[0])
        x2 = int(x2y1[0])
        y1 = int(x2y1[1])
        y2 = int(x1y2[1])
        # 遮挡
        # print(x1)
        self.image[y1:y2, x1:x2] = [255, 255, 255]

    def cover_main(self):
        # print("main")
        start = time.time()
        list(map(self.cover, self.box))
        end = time.time()
        print(f"图片覆盖处理时间{end - start}")
        # res = list(map(self.cover_and_write, self.box))

    @classmethod
    def to_chinese(cls, english_text):
        data = {'doctype': 'json', 'type': 'EN2ZH_CN', 'i': english_text}
        r = requests.get("http://fanyi.youdao.com/translate", params=data)
        trans_res = r.json()['translateResult'][0][0]['tgt']
        return trans_res

    @classmethod
    def chinese_main(cls, english_text):
        # print("main")
        start = time.time()
        pool = Pool(processes=5)
        text = pool.map(cls.to_chinese, english_text)
        pool.close()
        pool.join()
        # text = map(cls.to_chinese, english_text)
        end = time.time()
        print(f"翻译处理时间{end - start}")
        return text

    def write_image(self, box):
        # print(box)
        # 初始化Pillow的Image对象和Draw对象以及要使用的字体
        pillow_image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pillow_image)
        font = ImageFont.truetype("./JiZiJingDianFangSongJianFan-Shan(GEETYPE-FangSongGBT-Flash)-2.ttf", size=15)
        # 坐标 position (x,y) 顺序为 左上/右上/右下/左下
        # 用左上/右下 index 0/2
        # 坐标 position (x,y) 顺序为 左上/右上/右下/左下
        x2y1 = box[0]
        x1y2 = box[1]
        # 细化坐标
        x1 = int(x1y2[0])
        y1 = int(x2y1[1])
        # 在图像上绘制文本
        draw_txt = self.text[self.number]
        text_len_half = len(draw_txt) // 2
        before_text = draw_txt[:text_len_half]
        after_text = draw_txt[text_len_half:]
        draw.text((x1, y1), before_text + "\n" + after_text, font=font, fill=(0, 0, 0))
        self.number = self.number + 1
        # 将Pillow的Image对象转换回OpenCV格式的图像
        self.image = cv2.cvtColor(np.array(pillow_image), cv2.COLOR_RGB2BGR)
        del draw
        del pillow_image

    def write_main(self):
        # print("main")
        start = time.time()
        # print(print(i) for i in self.box)
        list(map(self.write_image, self.box))
        end = time.time()
        print(f"画字处理时间{end - start}")
        return self.image
