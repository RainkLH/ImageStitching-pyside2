#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :stitch_img_alg.py
# @Time      :2020/11/20 16:08:11
# @Author    :Raink

import sys
import cv2
import numpy as np


class ImageStitching():
    def __init__(self):
        super().__init__()
        self.w = 0
        self.h = 0
        self.imgs = []

    def set_images(self, list_imgs):
        for img_pth in list_imgs:
            img = cv2.imread(img_pth,cv2.IMREAD_COLOR)
            h, w, d = img.shape
            if w >= self.w: self.w = w
            if h >= self.h: self.h = h
            self.imgs.append(img)

    def stitching(self, layout, lb_w, lb_h):
        # 计算所需稿纸大小
        if layout == "v":
            self.h=sum([i.shape[0] for i in self.imgs])
        if layout == "h":
            self.w=sum([i.shape[1] for i in self.imgs])
        # 初始化稿纸
        color = (255, 255, 255)
        self.dst = np.array([[color for i in range(self.w)]for j in range(self.h)], dtype=np.uint8)
        # 在稿纸上粘贴每一张图片的起始位置
        index = 0
        for img in self.imgs:
            if layout == "v":
                self.dst[index:index + img.shape[0], 0:img.shape[1]] = img
                index = index + img.shape[0]
            if layout == "h":
                self.dst[0:img.shape[0], index:index + img.shape[1]] = img
                index = index + img.shape[1]

        return self._resize_for_preview(lb_w, lb_h)
    
    def _resize_for_preview(self, lb_w, lb_h):
        ph, pw = 0, 0
        r = self.h / self.w
        rh = self.h / lb_h
        rw = self.w / lb_w
        if rh >= rw :
            ph, pw = lb_h, int(lb_h * self.w / self.h)
        else :
            ph, pw = int(lb_w * self.h / self.w), lb_w
        p_img = cv2.resize(self.dst, (pw, ph))
        return p_img

    def save_dst(self, save_bname, save_dir):
        pth_to_save = save_dir + "\\" + save_bname + ".jpg"
        cv2.imwrite(pth_to_save, self.dst)