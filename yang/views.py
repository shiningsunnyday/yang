# Create your views here.
from django.shortcuts import render
from PIL import Image
import cv2
import numpy as np
from io import BytesIO
import pdb
from django.core.files.uploadedfile import InMemoryUploadedFile

from .forms import YangForm
import tensorflow as tf
from django.conf import settings

from .detect_yang.infer_face import *
import os
import pdb

def handle_file(img):
    opencv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    xml_path = "yang/detect_yang/haarcascade_frontalface_default.xml"
    model = "yang/detect_yang/new_model.tflite"
    return has_yang(opencv_img, model, xml_path)

def go_save(orig_img, img, imgs):
    cur_imgs = os.listdir('static/user')[::-1]
    if '.DS_Store' in cur_imgs:
        cur_imgs.remove('.DS_Store')
    if len(cur_imgs) >= 50:
        m, n = imgs[-2], imgs[-1]
        os.remove('static/user/%s' % m); os.remove('static/user/%s' % n)
    elif cur_imgs:
        m, n = '%d.jpg' % len(cur_imgs), '%d.jpg' % (len(cur_imgs) + 1)
        imgs.extend([m, n])
    else:
        m, n = '0.jpg', '1.jpg'
        imgs.extend([m, n])
    orig_img.save('static/user/%s' % m)
    img.save('static/user/%s' % n)
    return 'user/%s' % m, 'user/%s' % n


def yang_view(request):
    if request.method == 'POST':
        form = YangForm(request.POST, request.FILES)
        if form.is_valid():
            orig_img = Image.open(request.FILES['file'])
            yang, yang_score, yang_f = handle_file(orig_img)
            if yang:
                img = Image.fromarray(yang_f, 'RGB')
                imgs = os.listdir('static/user')
                if '.DS_Store' in imgs:
                    imgs.remove('.DS_Store')
                imgs = sorted(imgs, key=lambda x: int(x[:x.find('.')]))
                full, face = go_save(orig_img, img, imgs)
            if request.POST.get('input') != 'Andrew Yang':
                return render(request, 'boo.html', {'msg': "wrong name"})
            elif not yang:
                return render(request, 'boo.html', {'msg': "wrong pic"})
            else:
                imgs = ['user/%s' % x for x in imgs]
                return render(request, 'congrats.html', {'imgs': imgs, 'user_full': full, 'user_face': face})

    form = YangForm({'input': 'Andrew Yang'})
    return render(request, 'yang.html', {'form': form, 'imgs': os.listdir('static')})