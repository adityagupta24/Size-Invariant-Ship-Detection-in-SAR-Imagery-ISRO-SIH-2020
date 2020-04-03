import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import shutil
import sys
import PIL, PIL.Image, PIL.ImageFile
from sklearn.cluster import KMeans
# from exceptions import IOError

s = str(sys.argv[1])


# s = None
# for image in os.listdir():
    # if image.endswith(".jpg") and image != "result.jpg":
        # s = image

img = cv2.imread(s)
# img = cv2.imread(str('./'+s))
# img = PIL.Image.open("c:\\users\\adam\\pictures\\in.jpg")
# destination = "c:\\users\\adam\\pictures\\test.jpeg"
# try:
#     img.save(destination, "JPEG", quality=100, optimize=True, progressive=True)
# except IOError:
#     PIL.ImageFile.MAXBLOCK = img.size[0] * img.size[1]*3
#     img.save(destination, "JPEG", quality=100, optimize=True, progressive=True)

m = img.shape[0]
n = img.shape[1]
img = img[:,:,[2,1,0]]

print('Original shape of image:', img.shape)
dim = 512
m = dim*(m//dim)
n = dim*(n//dim)
img = img[:m, :n, :]
print('New shape of image for chipping: ', img.shape)

os.system('sudo rm -r ./Chipped')
os.system('sudo rm -r ./results')
os.system('mkdir ./Chipped')
os.system('mkdir ./results')
count = 1
print('Chipping....', end = ' ')
path = str(os.getcwd())
fw = open('./testImages.txt', 'w')
for i in range(0,m,dim):
    for j in range(0,n,dim):
        temp = img[i:i+dim,j:j+dim,:]
        plt.imsave("./Chipped/"+str(i + dim)+'_'+str(j + dim)+".jpg",temp)
        fw.write(path + "/Chipped/"+str(i + dim)+'_'+str(j + dim)+".jpg\n")
        count += 1
fw.close()
print('Chipped')

print('Predicting....', count)
if count == 2:
    os.system("sudo ./darknet detector test ./data/ship.data ./cfg/yolov3-ship.cfg ./yolov3-ship_last.weights\ 3 ./Chipped/512_512.jpg")
    os.system("cp ./predictions.jpg "+sys.argv[2] + '/media/images/result.jpg')
else:
    # os.system("./darknet detector valid ./data/ship.data ./cfg/yolov3-ship.cfg ./yolov3-ship_last.weights\ 3 ./results.txt")
    os.system("sudo ./darknet detector valid ./data/ship.data ./cfg/yolov3-ship.cfg ./yolov3-ship_1200.weights ./results.txt")
# for image in os.listdir("./Chipped"):
#     print(count, image)
#     count += 1
#     # os.system("./darknet detector test /content/gdrive/My Drive/darknet/ship.data /content/gdrive/My Drive/darknet/cfg/yolov3-ship.cfg  /content/gdrive/My Drive/darknet/backup/yolov3-ship_last.weights\ 5")
#     os.system("./darknet detector test ./data/ship.data ./cfg/yolov3-ship.cfg ./yolov3-ship_last.weights\ 3 ./Chipped/"+image)
#     shutil.move("./predictions.jpg","./Chipped/"+image) # Renames the  file

print('Creating rectangles...')
fr = open('./results/comp4_det_test_ship.txt', 'r')
ls = fr.readlines()
count = 1
print('current path: ' + os.getcwd())
print(sys.argv[3])
for line in ls:
    line = str(line)
    image, prob, x, y, w, h = line.split()
    prob, x, y, w, h = float(prob), float(x), float(y), float(w), float(h)
    if prob > 0.18:
        im = cv2.imread('./Chipped/' + image + '.jpg')
        im = cv2.cvtColor(im,cv2.COLOR_RGB2BGR)
        im = np.array(im, dtype=np.uint8)
        # print('im shape: ' + im.shape)
        print(count, image, prob)
        count += 1

        pt1 = (int(x), int(y))
        pt2 = (int(w), int(h))
        col = (255, 0, 0)

        cv2.rectangle(im, pt1, pt2, col, 4)
        ship_size = (np.sum((np.array(pt1) - np.array(pt2))**2)**0.5)*float(sys.argv[3])
        cv2.putText(im, 'Size: ' + str(ship_size) , (int(x), int(y-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, col, 1)
        plt.imsave('./Chipped/' + image + '.jpg', im)
        # plt.imsave('/content/gdrive/My Drive/darknet/Chipped/' + image + '.jpg', im)

fr.close()
print('rectangles drawn')
l = sorted(os.listdir("Chipped"))
new_img = np.zeros((m, n, 3))

print('Combining results...', end = '')
for i in range(0,m,dim):
    for j in range(0,n,dim):
        temp = cv2.imread("./Chipped/"+str(i + dim)+'_'+str(j + dim)+".jpg")
        temp = cv2.cvtColor(temp,cv2.COLOR_RGB2BGR)
        new_img[i:i+dim,j:j+dim,:] = temp/255
plt.imsave(sys.argv[2] + '/media/images/result.jpg', new_img)
print('combined')

##  Segmentation
print('Discriminating between land and water')
img = cv2.imread(s)
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
X = img.reshape((-1,3))
km = KMeans(n_clusters=3)
km.fit(X)
centers = np.round(km.cluster_centers_)
new_center = np.mean(centers,axis =1)
zero_out = [np.argmin(new_center)]
for i in zero_out:
    centers[i] = np.array([0,0,0])
new_img = centers[km.labels_]
new_img = new_img.reshape(img.shape[0], img.shape[1], 3)
# new_img[new_img[:,:,:]>0] = 1
plt.imsave(sys.argv[2] + '/media/images/result_2.jpg',new_img/255.0)
print('saved results')

print('images saved as results.jpg in:', end = ' ')
os.system('pwd')
