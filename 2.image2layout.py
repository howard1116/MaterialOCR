import os
import cv2
import json
import shutil
from tqdm import tqdm
import layoutparser as lp

input_dir = 'data_demo/image'
output_dir = 'data_demo/layout'
model = lp.Detectron2LayoutModel('lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
                                #  'lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config',
                                extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"})

def get_blocks(image, double_column = True):
    layout = model.detect(image)
    text_blocks = lp.Layout([b for b in layout if (b.type=='Text' or b.type == 'Title')])
    figure_blocks = lp.Layout([b for b in layout if (b.type=='Figure' or b.type == 'Table')])
    text_blocks = lp.Layout([b for b in text_blocks if not any(b.is_in(b_fig) for b_fig in figure_blocks)])

    if (double_column):
        h, w = image.shape[:2]
        left_interval = lp.Interval(0, w/2*1.05, axis='x').put_on_canvas(image)
        left_text = text_blocks.filter_by(left_interval, center=True)
        right_text = lp.Layout([b for b in text_blocks if b not in left_text])
        left_text.sort(key = lambda b:b.coordinates[1], inplace=True)
        right_text.sort(key = lambda b:b.coordinates[1], inplace=True)
        figure_blocks.sort(key = lambda b:b.coordinates[1], inplace=True)
        blocks = lp.Layout([b for b in left_text + right_text + figure_blocks])
    else:
        text_blocks.sort(key = lambda b:b.coordinates[1], inplace=True)
        figure_blocks.sort(key = lambda b:b.coordinates[1], inplace=True)
        blocks = lp.Layout([b for b in text_blocks + figure_blocks])

    id_map = {"Text": 0, "Title": 0, "List": 0, "Table": 0, "Figure": 0}
    for x in blocks:
        id_map[x.type] += 1
        x.id = x.type + '-' + str(id_map[x.type])
    return blocks

def extract_subimage_from_image(md5, bar):
    input_subdir = os.path.join(input_dir, md5)
    output_subdir = os.path.join(output_dir, md5)
    if os.path.isdir(output_subdir):
        shutil.rmtree(output_subdir)
    os.makedirs(output_subdir)

    for file_name in os.listdir(input_subdir):
        input_path = os.path.join(input_subdir, file_name)
        output_path = os.path.join(output_subdir, file_name)
        image = cv2.imread(input_path)
        blocks = get_blocks(image)
        lp.draw_box(image, blocks, box_width = 3, show_element_id = True).save(output_path)

        with open(output_path[:-3] + 'json', 'w') as file:
            json.dump([b.to_dict() for b in blocks], file)
        bar.update(1)

count = 0
for md5 in os.listdir(input_dir):
    input_subdir = os.path.join(input_dir, md5)
    assert(os.path.isdir(input_subdir))
    for file_name in os.listdir(input_subdir):
        assert(file_name[-3:] == 'png')
        count += 1

bar = tqdm(total = count)
for md5 in os.listdir(input_dir):
    extract_subimage_from_image(md5, bar)