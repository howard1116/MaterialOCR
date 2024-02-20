import os
import fitz
import shutil
import hashlib
import threading
from tqdm import tqdm

input_dir = 'data/paper'
output_dir = 'data/image'

def extract_image_from_pdf(input_file_name):
    md5 = hashlib.md5(input_file_name.encode('utf-8')).hexdigest()
    output_subdir = os.path.join(output_dir, md5)
    if os.path.isdir(output_subdir):
        shutil.rmtree(output_subdir)
    os.makedirs(output_subdir)

    input_path = os.path.join(input_dir, input_file_name)
    pdf_document = fitz.open(input_path)
    for page_number in range(pdf_document.page_count):
        image = pdf_document[page_number].get_pixmap()
        output_path = os.path.join(output_subdir, '%s.png' % str(page_number + 1).zfill(3))
        image.save(output_path, 'png')
    pdf_document.close()

for file_name in tqdm(os.listdir(input_dir)):
    if (file_name[-3:] == 'pdf'):
        extract_image_from_pdf(file_name)
        # t = threading.Thread(target=extract_image_from_pdf, args=(file_name, ))
        # t.start()