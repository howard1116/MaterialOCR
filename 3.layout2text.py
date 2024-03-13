import os
import cv2
import json
from tqdm import tqdm
import layoutparser as lp
import paddle
paddle.disable_signal_handler()
from paddleocr import PaddleOCR
# from img2table.document import Image

image_dir = 'data_demo/image'
layout_dir = 'data_demo/layout'
output_dir = 'data_demo/text'
if (not os.path.isdir(output_dir)):
  os.mkdir(output_dir)

# def tesseractocr(image):
#     ocr_agent = lp.TesseractAgent(languages = ['eng', 'chi_sim'])
#     return ocr_agent.detect(image)

engine = PaddleOCR(enable_mkldnn = True, use_angle_cls = True, show_log = False)
def paddleocr(image):
    result = engine.ocr(image)[0]
    if (result is None):
        return ''
    text = [x[-1][0].replace('\n', '') for x in result]
    return '\n'.join(text) + '\n'

def extract_text_from_subimage(md5, bar):
    layout_subdir = os.path.join(layout_dir, md5)

    all_text = []
    for file_name in os.listdir(layout_subdir):
        if (file_name[-4:] != 'json'):
            continue
        file_path = os.path.join(layout_subdir, file_name)
        image_path = os.path.join(image_dir, md5, file_name[:-4] + 'png')
        assert(os.path.isfile(image_path))

        # doc = Image(image_path, detect_rotation=False)
        # doc.to_xlsx(dest=file_path[:-4] + 'xlsx',
        #             ocr=ocr,
        #             implicit_rows=True,
        #             borderless_tables=True,
        #             min_confidence=50)

        with open(file_path, 'r') as file:
            blocks = json.load(file)
        blocks = [lp.TextBlock.from_dict(b) for b in blocks]

        image = cv2.imread(image_path)
        with open(os.path.join(layout_subdir, file_name[:-4] + 'txt'), 'w', encoding='utf-8') as page_text:
            for b in blocks:
                if (b.type == 'Title' or b.type == 'Text'):
                    sub_image = b.pad(left=5, right=5, top=5, bottom=5).crop_image(image)
                    # b.text = tesseractocr(sub_image)
                    b.text = paddleocr(sub_image)
                    page_text.write(b.text)
                    all_text.append(b.text)
        with open(file_path, 'w') as file:
            json.dump([b.to_dict() for b in blocks], file)
        bar.update(1)

    output_path = os.path.join(output_dir, f'{md5}.txt')
    with open(output_path, 'w', encoding='utf-8') as file:
        for text in all_text:
            file.write(text)

count = 0
for md5 in os.listdir(layout_dir):
    for file_name in os.listdir(os.path.join(layout_dir, md5)):
        if (file_name[-4:] == 'json'):
            count += 1
bar = tqdm(total = count)
for md5 in os.listdir(layout_dir):
    extract_text_from_subimage(md5, bar)