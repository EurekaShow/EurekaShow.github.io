# ubuntu下Python-openCV-face_recognition的安装和使用

### 安装Python发布版本

- 安装pip

```bash
//安装 pip
# sudo apt-get install python-pip
```

- 安装Virtualenv

Virtualenv 是什么?
virtualenv is a tool to create isolated Python environments.
virtualenv通过创建独立Python开发环境的工具, 来解决依赖、版本以及间接权限
问题. 比如一个项目依赖Django1.3 而当前全局开发环境为Django1.7, 版本跨度过大, 导致不兼容使项目无法正在运行, 使用virtualenv可以解决这些问题.

virtualenv创建一个拥有自己安装目录的环境, 这个环境不与其他虚拟环境共享库, 能够方便的管理python版本和管理python库

```bash

# sudo pip install virtualenv

# mkdir face
# cd face
# cd facenv/

//创建我们的独立环境
# source bin/activate
```

```bash
//安装 Python 发布版本，dev包必须安装，很多用pip安装包都需要编译
# sudo apt-get install python2.7 python2.7-dev

//或者安装 Python 发布版本，dev包必须安装，很多用pip安装包都需要编译
# sudo apt-get install python3.2 python3.2-dev
```

- 安装build依赖包

```bash
//很多pip安装的包都需要libssl和libevent编译环境
# sudo apt-get install build-essential libssl-dev libevent-dev libjpeg-dev libxml2-dev libxslt-dev
```

### 安装openCV

- 安装

```bash
# pip install --upgrade setuptools
# pip install numpy Matplotlib
# pip install opencv-python
```

完整安装后,我们来做个测试:

- 测试

```bash
# touch test.py
# vim test.py
```

在test.py中黏贴下面内容,th.jpeg改为你自己的图片文件.

```python
 import cv2
 
 img = cv2.imread('th.jpeg')
 cv2.imshow('image',img)
 k = cv2.waitKey(0)
 cv2.destroyAllWindows()
```

保存退出,执行

```bash
# python test.py
```

弹出图片框,加载显示我们的图片正常就Ok了.

### 安装脸部识别类库,face_recognition

- 安装

```bash
# sudo apt-get install build-essential cmake

# sudo apt-get install libgtk-3-dev

# sudo apt-get install libboost-all-dev

# pip install dlib

# pip install face_recognition
//如果执行上一步反复报错,请执行下面.具体错误信息请跳转到最后.
# pip --no-cache-dir install face_recognition
```

- run测试代码

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/3 15:52
# @Author  : He Hangjiang
# @Site    : 
# @File    : 摄像头实时识别.py
# @Software: PyCharm

import face_recognition
import cv2

video_capture = cv2.VideoCapture(0)

# 本地图像
hhj_image = face_recognition.load_image_file("hhj.jpg")
hhj_face_encoding = face_recognition.face_encodings(hhj_image)[0]

#
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # 读取摄像头画面
    ret, frame = video_capture.read()

    # 改变摄像头图像的大小，图像小，所做的计算就少
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # opencv的图像是BGR格式的，而我们需要是的RGB格式的，因此需要进行一个转换。
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # 根据encoding来判断是不是同一个人，是就输出true，不是为flase
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # 默认为unknown
            match = face_recognition.compare_faces([hhj_face_encoding], face_encoding)
            name = "Unknown"

            if match[0]:
                name = "hhj"

            face_names.append(name)

    process_this_frame = not process_this_frame

    # 将捕捉到的人脸显示出来
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # 矩形框
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        #加上标签
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display
    cv2.imshow('Video', frame)

    # 按Q退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
```

### 完美测试没问题啦,我们是不是还想让我们的虚拟环境可以便携,直接到别的环境上直接运行,那么:

```bash
# virtualenv --relocatable ./
Making script /home/eureka/Documents/face/facenv/bin/easy_install-2.7 relative
Making script /home/eureka/Documents/face/facenv/bin/easy_install relative
Making script /home/eureka/Documents/face/facenv/bin/f2py relative
Making script /home/eureka/Documents/face/facenv/bin/pip relative
Making script /home/eureka/Documents/face/facenv/bin/wheel relative
Making script /home/eureka/Documents/face/facenv/bin/python-config relative
Making script /home/eureka/Documents/face/facenv/bin/pip2.7 relative
Making script /home/eureka/Documents/face/facenv/bin/face_recognition relative
Making script /home/eureka/Documents/face/facenv/bin/pip2 relative
```

Ok,降龙十八掌,打完收工.对了,顺便交代下,下次进入虚拟环境的方法:

```bash
# cd face
# cd facenv/
# source ./bin/activate
//执行之前的测试代码看看
# cd ..
# python pace.py
//退出环境的方法是
# deactivate

//安装计算模块
# sudo pip install numpy
# sudo pip install scipy
# pip install matplotlib

// sudo apt-get install python-scipy
// sudo apt-get install python-numpy
// sudo apt-get install python-matplotlib

//安装http请求模块
# pip install requests

//安装RESTful api用的flask
# pip install flask
```

- 安装face_recognition错误及处理

执行最后一步 
sudo pip install face_recognition
一而再,再而三的报如下错误.

```bash
Traceback (most recent call last):
  File "/usr/lib/python2.7/dist-packages/pip/basecommand.py", line 215, in main
    status = self.run(options, args)
  File "/usr/lib/python2.7/dist-packages/pip/commands/install.py", line 342, in run
    requirement_set.prepare_files(finder)
  File "/usr/lib/python2.7/dist-packages/pip/req/req_set.py", line 380, in prepare_files
    ignore_dependencies=self.ignore_dependencies))
  File "/usr/lib/python2.7/dist-packages/pip/req/req_set.py", line 620, in _prepare_file
    session=self.session, hashes=hashes)
  File "/usr/lib/python2.7/dist-packages/pip/download.py", line 821, in unpack_url
    hashes=hashes
  File "/usr/lib/python2.7/dist-packages/pip/download.py", line 659, in unpack_http_url
    hashes)
  File "/usr/lib/python2.7/dist-packages/pip/download.py", line 882, in _download_http_url
    _download_url(resp, link, content_file, hashes)
  File "/usr/lib/python2.7/dist-packages/pip/download.py", line 603, in _download_url
    hashes.check_against_chunks(downloaded_chunks)
  File "/usr/lib/python2.7/dist-packages/pip/utils/hashes.py", line 46, in check_against_chunks
    for chunk in chunks:
  File "/usr/lib/python2.7/dist-packages/pip/download.py", line 571, in written_chunks
    for chunk in chunks:
  File "/usr/lib/python2.7/dist-packages/pip/utils/ui.py", line 139, in iter
    for x in it:
  File "/usr/lib/python2.7/dist-packages/pip/download.py", line 560, in resp_read
    decode_content=False):
  File "/usr/share/python-wheels/urllib3-1.19.1-py2.py3-none-any.whl/urllib3/response.py", line 432, in stream
    data = self.read(amt=amt, decode_content=decode_content)
  File "/usr/share/python-wheels/urllib3-1.19.1-py2.py3-none-any.whl/urllib3/response.py", line 380, in read
    data = self._fp.read(amt)
  File "/usr/share/python-wheels/CacheControl-0.11.7-py2.py3-none-any.whl/cachecontrol/filewrapper.py", line 63, in read
    self._close()
  File "/usr/share/python-wheels/CacheControl-0.11.7-py2.py3-none-any.whl/cachecontrol/filewrapper.py", line 50, in _close
    self.__callback(self.__buf.getvalue())
  File "/usr/share/python-wheels/CacheControl-0.11.7-py2.py3-none-any.whl/cachecontrol/controller.py", line 275, in cache_response
    self.serializer.dumps(request, response, body=body),
  File "/usr/share/python-wheels/CacheControl-0.11.7-py2.py3-none-any.whl/cachecontrol/serialize.py", line 87, in dumps
    ).encode("utf8"),
MemoryError
```
翻到如下帖子,虽然安装的不是同一个东西,错误何其相似,尝试下,解决.
[stackoverflow](https://stackoverflow.com/questions/46141998/install-gensim-error-in-ubuntu)

```bash
# pip --no-cache-dir install face_recognition
```
终于看到了成功返回.
Successfully installed Click-6.7 Pillow-5.0.0 dlib-19.9.0 face-recognition-1.2.1 face-recognition-models-0.3.0 numpy-1.14.2 scipy-1.0.0