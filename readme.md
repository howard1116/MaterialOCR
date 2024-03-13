# MaterialOCR

系统：ubuntu22.04

## 建立环境

```sh
sudo apt install g++ tesseract-ocr
conda create -n ocr_env python=3.9
conda activate ocr_env
pip install -r requirements.txt
pip install git+https://github.com/facebookresearch/detectron2.git@v0.5#egg=detectron2
pip install Pillow==9.5.0 #强制把pillow版本降下来
```

倒数第二步要是慢就上魔法

## 运行代码

### step0

代码`0.caj2pdf.py`的作用为把`.caj`文档转换为`.pdf`格式

考虑到

- 此代码仅需运行一次
- 代码是在windows环境下写的，现在我电脑重装成了ubuntu
- 我还忘了它依赖哪个安装包

所以请忽略

### step1

```sh
python 1.pdf2image.py
```

将`data_demo/paper`中的pdf文件拆分成图片，并存入`data_demo/image`

请注意，每篇paper对应的image为一个文件夹，文件夹名称为paper文件名的md5编码

### step2

```sh
python 2.image2layout.py
```

识别`data_demo/image`中每张图片的layout，存入`data_demo/layout`

注意这一步需要下载模型，需要魔法，自行调整`2.image2layout.py`代码的第2，3行

### step3

```sh
python 3.layout2text.py
```

根据`data_demo/layout`中的每个layout，进行文本识别ocr，拼接后存入`data_demo/text`，并更新`data_demo/layout/XXXX/X.layout`

遇到错误，请看

https://blog.csdn.net/qq451882471/article/details/106967942

我的解决记录如下

```sh
cd /usr/lib
sudo ln -s /home/h10/miniconda3/envs/ocr_env/lib/python3.9/site-packages/nvidia/cudnn/lib/libcudnn.so.8 libcudnn.so
sudo ln -s /home/h10/miniconda3/envs/ocr_env/lib/python3.9/site-packages/nvidia/cublas/lib/libcublas.so.12 libcublas.so
sudo ln -s /home/h10/miniconda3/envs/ocr_env/lib/python3.9/site-packages/nvidia/cudnn/lib/libcudnn_ops_infer.so.8 libcudnn_ops_infer.so.8
sudo ln -s /home/h10/miniconda3/envs/ocr_env/lib/python3.9/site-packages/nvidia/cublas/lib/libcublasLt.so.12 libcublasLt.so.12
sudo ln -s /home/h10/miniconda3/envs/ocr_env/lib/python3.9/site-packages/nvidia/cublas/lib/libcublas.so.12 libcublas.so.12
sudo ln -s /home/h10/miniconda3/envs/ocr_env/lib/python3.9/site-packages/nvidia/cudnn/lib/libcudnn_cnn_infer.so.8 libcudnn_cnn_infer.so.8
```

傻逼百度