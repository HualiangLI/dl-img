import json
import os
import requests
import base64
import random
import string
import cv2
from imutils import paths

def retreiv_images():
  with open('./imgs.json') as f:
    img_url_list = json.loads(json.load(f))

  if not os.path.exists('images'):
      os.mkdir('images')
  image_path = 'images'
  total = 0

  for img_url in img_url_list:
    if img_url is None: continue
    if img_url.startswith('data:'):
      code = img_url.replace('data:image/jpeg;base64,', '')
      img_data = base64.b64decode(code)
    else:
      try:
        req = requests.get(img_url, timeout=60)
        img_data = req.content
      except KeyboardInterrupt:
        print('Interrupt!')
        break
      except:
        print('Could not download {}. Downloading next file'.format(img_url))

    filename = '{}.jpg'.format(str(total).zfill(6))
    file_path = os.path.sep.join([image_path, filename])
    with open(file_path, 'wb') as f:
      f.write(img_data)

    print('Downloaded {}'.format(file_path))
    total += 1

def del_broken_images():
  for imagePath in paths.list_images('images'):
    delete_image = False
    try:
        image = cv2.imread(imagePath)
        if image is None:
            delete_image = True
    # if OpenCV cannot load the image
    except:
        delete_image = True
    if delete_image:
        print('Deleting {}'.format(imagePath))
        os.remove(imagePath)

if __name__ == '__main__':
  del_broken_images()
