# MaterialOCR

## 建立环境

```sh
conda create -n ocr_env python=3.8
conda activate ocr_env
pip install -r requirements.txt
# python -m ipykernel install --user --name tem_env --display-name "tem_env"
```

## 跑代码

```sh
python 0.caj2pdf.py
python 1.pdf2image.py
python 2.image2layer.py
python 3.layer2text.py
python 4.text2dataset.py
```

## Todo

- [ ] 移植ubuntu
- [ ] lib写markdown，并移出.gitignore