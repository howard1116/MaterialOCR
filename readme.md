# MaterialOCR

## 建立环境

```sh
conda create -n ocr_env python=3.8
conda activate ocr_env
pip install -r requirements.txt
apt install tesseract-ocr
```


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

### step3

```sh
python 3.layout2text.py
```

根据`data_demo/layout`中的每个layout，进行文本识别ocr，拼接后存入`data_demo/text`，并更新`data_demo/layout/XXXX/X.layout`