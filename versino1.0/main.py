import re
import cv2
import os
from ScreenCapture import ScreenCapture
from image_ocr import OcrImage
from paddleocr import PaddleOCR
import time
import logging
from functools import reduce

global result


def run(sc):
    # 'en_PP-OCRv3_rec'
    # 实例化ocr
    ocr = PaddleOCR(use_angle_cls=True, lang="en", modele='en_PP-OCRv3_rec', use_gpu=True, drop_score=0.8, debug=False)
    # 循环体
    while True:
        # print("--------------------")
        # all_start = time.time()
        # 截屏

        img = sc.grab_screen_mss()

        cv2.namedWindow(sc.window_name, cv2.WINDOW_NORMAL)  # cv2.WINDOW_NORMAL 根据窗口大小设置图片大小

        cv2.resizeWindow(sc.window_name, 1920, 1080)

        # 创建识别对象
        result = ocr.ocr(img)

        # 清洗数据
        # print(result)

        # 数据清洗
        def check(txt):
            info = txt[1][0]
            if not info.isalpha():
                if not re.match(r'^[a-zA-Z0-9\s\W]+$', info):
                    result[0].remove(txt)
                else:
                    if re.match(r'^[0-9\W]+$', info):
                        # print(result)
                        # print(txt)
                        result[0].remove(txt)

        # 优化数据
        def limit(txt):
            res = []
            info_len = len(txt)
            # print(info_len)
            star_index = 0
            button = True
            while button:
                # 判断是否为段落开头
                # print(f"button {star_index}")
                # print(txt[star_index][1][0][0])
                if re.match('^[A-Z]', txt[star_index][1][0][0].lstrip()):
                    # print(f"验证 {txt[star_index][1][0]}")
                    tmp = [star_index]
                    tmp_index = 0
                    # 验证是否为末尾
                    if star_index == info_len - 1:
                        # print("ending")
                        res.append(txt[star_index])
                        break
                    # 是开头
                    while button:
                        tmp_index = tmp_index + 1
                        if (loop_index := tmp_index + star_index) >= info_len:
                            # print("超出了")
                            button = False
                            break
                        # print(loop_index)
                        if not re.match('^[A-Z]', txt[loop_index][1][0][0].lstrip()):
                            # print(txt[loop_index][1][0])
                            tmp.append(loop_index)
                            continue
                        else:
                            # 遇到了下一个大写
                            star_index = star_index + tmp_index
                            # print(tmp)
                            new_txt = reduce(lambda x, y: x + y, map(lambda x: txt[x][1][0], tmp))
                            # print(new_txt)
                            # x2,y1  x1,y2  text
                            res.append([[txt[tmp[0]][0][1], txt[tmp[-1]][0][3]], new_txt])
                            # print(star_index)
                            if star_index == info_len:
                                button = False
                            break
                else:
                    star_index = star_index + 1
                    # print(f"error {star_index}")
            return res

        # start = time.time()
        res__ = list(map(check, result[0]))
        # end = time.time()
        # print(f"数据清洗处理时间{end - start}")
        # print(result)
        # 数据优化
        # start = time.time()
        # print(result[0])
        result = limit(result[0])
        # end = time.time()
        # print(f"数据优化处理时间{end - start}")
        # print(result)
        # box
        box = list(map(lambda x: x[0], result))
        # print(box)
        # text
        text = list(map(lambda x: x[1], result))
        # print(text)
        # 翻译
        text = OcrImage.chinese_main(text)
        # print([i for i in text])
        # 实例化
        img_change = OcrImage(img, box, text)
        # 覆盖
        img_change.cover_main()
        # 写字
        img = img_change.write_main()
        # 输出画面
        cv2.imshow(sc.window_name, img)
        #
        # all_end = time.time()
        # print(f"总时间{all_end - all_start}")
        #
        del img_change

        if cv2.waitKey(1000) == sc.exit_code:  # 默认：ESC

            cv2.destroyAllWindows()

            os._exit(0)


if __name__ == '__main__':
    logging.disable(logging.DEBUG)
    sc = ScreenCapture(capture_region=(1, 1))
    run(sc)
