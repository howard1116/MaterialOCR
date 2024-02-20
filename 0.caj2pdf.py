import os
import shutil

input_dir = os.path.join('data', 'paper')

def clear_name():
    for name in os.listdir(input_dir):
        if (name[0] == '_'):
            new_name = name[1:]
            name = os.path.join(input_dir, name)
            new_name = os.path.join(input_dir, new_name)
            print(name)
            shutil.move(name, new_name)

    for name in os.listdir(input_dir):
        name = os.path.join(input_dir, name)
        target = '_ _          _                 _        _            _               _            _          _'
        if (name.find(target) != -1):
            print(name)
            shutil.move(name, name.replace(target, ''))

    for name in os.listdir(input_dir):
        if (name[-3:] != 'pdf' and name[-3:].lower() == 'pdf'):
            new_name = name[:-3] + 'pdf'
            name = os.path.join(input_dir, name)
            new_name = os.path.join(input_dir, new_name)
            print(name)
            shutil.move(name, new_name)

# clear_name()

# tmp_dir = 'data/image/a9214494c6ce8de96ce3b9575dbb5dfc'
# for png in os.listdir(tmp_dir):
#     name = png.split('.')[0]
#     old_path = os.path.join(tmp_dir, png)
#     new_path = os.path.join(tmp_dir, str(int(name) + 1).zfill(3) + '.png')
#     if (os.path.isfile(old_path) and not os.path.isfile(new_path)):
#         print(old_path, new_path)

# for caj in os.listdir(input_dir):
#     caj = os.path.join(input_dir, caj)
#     if (caj[-3:] == 'caj'):
#         pdf = caj[:-3] + 'pdf'
#         if not os.path.isfile(pdf):
#             print(pdf)
#             os.chdir('caj2pdf')
#             os.system('python caj2pdf convert ../%s -o ../%s' % (caj, pdf))
#             os.chdir('..')