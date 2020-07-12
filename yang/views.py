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

def handle_file(file):
    img = Image.open(file)
    img.save('static/user/full.jpg')
    opencv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    xml_path = "yang/detect_yang/haarcascade_frontalface_default.xml"
    model = "yang/detect_yang/new_model.tflite"
    return has_yang(opencv_img, model, xml_path)

def yang_view(request):
    print(request.POST)
    if request.method == 'POST':

        form = YangForm(request.POST, request.FILES)
        if form.is_valid():
            yang, yang_score, yang_f = handle_file(request.FILES['file'])
            if yang:
                img = Image.fromarray(yang_f, 'RGB')
                img.save('static/user/face.jpg')
            if request.POST.get('input') != 'Andrew Yang':
                return render(request, 'boo.html', {'msg': "wrong name"})
            elif not yang:
                return render(request, 'boo.html', {'msg': "wrong pic"})
            else:
                return render(request, 'congrats.html', {'full': 'user/full.jpg',
                                                         'face': 'user/face.jpg'})

    form = YangForm({'input': 'Andrew Yang'})
    return render(request, 'yang.html', {'form': form, 'imgs': os.listdir('static')})