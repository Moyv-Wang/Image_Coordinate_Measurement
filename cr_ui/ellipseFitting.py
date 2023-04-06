import base64
import time

import cv2


def fit_ellipse(testImg):
    bluredImg = cv2.GaussianBlur(testImg, (5, 5), 0)
    edges = cv2.Canny(bluredImg, 50, 150);
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    flag = 0
    list = []
    for cnt in contours:
        count = len(cnt)
        if count < 6:
            continue
        # retval = cv2.fitEllipse(cnt)
        retval = cv2.fitEllipse(cnt)
        if ((retval[1][0] < 40) and (retval[1][1] < 40)) or (
                (retval[1][0] > 1.15 * retval[1][1]) or (retval[1][1] > 1.15 * retval[1][0])):
            continue
        list.append(retval)

    if len(list) == 1:
        # 绘制代码在这儿不需要
        cv2.ellipse(testImg, list[0], (0, 0, 255), 2)
        cv2.namedWindow("res", cv2.WINDOW_FREERATIO)
        cv2.imshow("res", testImg)
        cv2.waitKey(1)
        time.sleep(2)
        cv2.destroyWindow("res")
        return list[0][0]
        # print(list)
        # cv2.circle(testImg, (int(retval[0][0]), int(retval[0][0])), 0, (0, 0, 255))
