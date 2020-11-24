#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :stitch_img_main.py
# @Time      :2020/11/18 11:26:23
# @Author    :Raink

import sys, time
from os.path import dirname
from PySide2.QtCore import Qt
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import *
from stitch_img_alg import ImageStitching


class MainWindow(QWidget):
    MainWindowTitle = "RkImageStitching"
    image_stitching = ImageStitching()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.MainWindowTitle)
        self.resize(600, 600)
        # 设置UI
        self._setup_ui()        
        # 初始化窗口
        self._init_window()
        # 绑定事件
        self._binding_event()

    def _setup_ui(self):
        # 主界面布局
        self.layout_config = self._setup_config_layout()
        self.layout_result = self._setup_preview_layout()    
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.layout_config)
        self.main_layout.addLayout(self.layout_result)
        self.main_layout.setStretch(0,2)
        self.main_layout.setStretch(1,8)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)
    
    def _setup_config_layout(self):
        # 配置栏
        layout_config = QVBoxLayout()
        layout_conf_btns = QHBoxLayout()
        layout_stitching_layout = QHBoxLayout()
        # 说明
        self.lb_conf_inf = QLabel("选择需要拼接的图像文件和拼接方式")
        # 选择图片
        self.btn_imgs = QPushButton("选择图片")
        self.btn_imgs.setFixedWidth(100)
        # 拼接方向
        self.v_stitching = QRadioButton("竖向拼接")
        self.h_stitching = QRadioButton("横向拼接")
        self.btn_stitching = QPushButton("执行")
        self.btn_stitching.setFixedWidth(100)
        self.tedit_selected_imgs = QTextEdit("所选图片：")
        # 添加布局
        layout_stitching_layout.addWidget(self.v_stitching)
        layout_stitching_layout.addWidget(self.h_stitching)
        layout_stitching_layout.setAlignment(Qt.AlignRight)
        layout_conf_btns.addWidget(self.btn_imgs)
        layout_conf_btns.addLayout(layout_stitching_layout)
        layout_conf_btns.addWidget(self.btn_stitching)
        layout_config.addWidget(self.lb_conf_inf)
        layout_config.addLayout(layout_conf_btns)
        layout_config.addWidget(self.tedit_selected_imgs)
        layout_config.setStretch(0,1)
        layout_config.setStretch(1,2)
        layout_config.setStretch(2,4)
        layout_config.setSpacing(2)
        return layout_config

    def _setup_preview_layout(self):
        # 预览及保存
        widget_res_btns = QWidget()
        layout_res_btns = QHBoxLayout(widget_res_btns)
        layout_result = QVBoxLayout()
        # 结果预览（缩略图）
        self.lb_img_preview = QLabel("结果预览")         
        self.lb_img_preview.setAlignment(Qt.AlignCenter)       
        self.lb_info_name_for_save = QLabel("存储名称")
        self.lb_info_dir_for_save = QLabel("存储目录")
        self.tedit_save_name = QLineEdit()
        self.tedit_save_dir = QLineEdit()
        self.btn_result_save = QPushButton("保存")
        layout_res_btns.addWidget(self.lb_info_name_for_save)
        layout_res_btns.addWidget(self.tedit_save_name)
        layout_res_btns.addWidget(self.lb_info_dir_for_save)
        layout_res_btns.addWidget(self.tedit_save_dir)
        layout_res_btns.addWidget(self.btn_result_save)
        layout_res_btns.setStretch(0,1)
        layout_res_btns.setStretch(1,2)
        layout_res_btns.setStretch(2,1)
        layout_res_btns.setStretch(3,6)
        layout_res_btns.setStretch(4,1)
        layout_res_btns.setAlignment(Qt.AlignLeft)
        widget_res_btns.setFixedHeight(40)
        layout_result.addWidget(widget_res_btns)
        layout_result.addWidget(self.lb_img_preview)
        return layout_result
    
    def _init_window(self):
        # 初始化窗口
        self.v_stitching.setChecked(True)
        self.tedit_selected_imgs.setReadOnly(True)
        self.tedit_save_dir.setReadOnly(True)

    def _binding_event(self):
        # 绑定事件        
        self.btn_imgs.clicked.connect(self._open_file_dialog) 
        self.btn_stitching.clicked.connect(self._stitch_images)       
        self.btn_result_save.clicked.connect(self._save_result)

    def _open_file_dialog(self):
        # 打开文件对话框
        dlg_file = QFileDialog()
        dlg_file.setWindowTitle("选择图片")
        dlg_file.setNameFilter("image files (*.jpg *.png *.bmp)")
        dlg_file.setFileMode(QFileDialog.ExistingFiles)
        dlg_file.setViewMode(QFileDialog.Detail)
        if dlg_file.exec_():
            self.file_names = dlg_file.selectedFiles()
            self.image_stitching.set_images(self.file_names)
            for file_name in self.file_names:
                self.tedit_selected_imgs.append(file_name)
    
    def _stitch_images(self):
        # 执行拼接
        dir_to_save = dirname(self.file_names[0])
        name_to_save = time.strftime("%y%m%d%H%M%S", time.localtime())
        self.tedit_save_dir.setText(dir_to_save)
        self.tedit_save_name.setText(name_to_save)
        lb_size = self.lb_img_preview.frameSize().toTuple()
        stitch_type = "v"
        if self.h_stitching.isChecked():
            stitch_type = "h"            
        img = self.image_stitching.stitching(stitch_type, lb_size[0], lb_size[1])
        image = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_BGR888)        
        pmap = QPixmap.fromImage(image)  #.scaled(lb_size,aspectMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.lb_img_preview.clear()
        self.lb_img_preview.setPixmap(pmap) 

    def _save_result(self):
        # 保存结果
        dir_to_save = self.tedit_save_dir.text()
        name_to_save = self.tedit_save_name.text()
        self.image_stitching.save_dst(name_to_save, dir_to_save)
        self.tedit_save_dir.clear()
        self.tedit_save_name.clear()
        self.lb_img_preview.setText("结果已保存")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())