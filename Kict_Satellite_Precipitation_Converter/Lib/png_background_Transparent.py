# -*- coding: utf-8 -*-
'''
Created on 2019. 11. 4.


png 배경 투명화

@author: USER
'''

import os,sys

from PIL import Image

def png_background_Transparent(png_path):
    img = Image.open(png_path)
    img = img.convert("RGBA")
    datas = img.getdata()
     
    newData = []
    for item in datas:
        if (item[0] != 255):
#         if item[0] ==1 and item[1] ==1 and item[2] == 1:
#         if item[0] > 200 and item[1] > 200 and item[2] > 200:
            newData.append((item[0], item[1], item[2], 0))
        else:
            newData.append(item)
#     
#     print (newData)
#     img.putdata(newData)
    filename = os.path.splitext(png_path)
    img.save(filename[0]+"_test" + filename[1], "PNG")
    img.save(png_path+"_test", "PNG")
    
    
# png="D:/Temp/test3.png"
# png_background_Transparent(png)