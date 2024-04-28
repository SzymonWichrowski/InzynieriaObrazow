import cv2 
import numpy 
from matplotlib import pyplot

primaryImageBGR = cv2.imread("images/kwiatki.jpg")
primaryImageRGB = cv2.cvtColor(primaryImageBGR, cv2.COLOR_BGR2RGB)

kernel = numpy.array([[-1, -1, -1], 
                      [-1, 8, -1],
                      [-1, -1, -1]])

multiplier_2 = numpy.array([[0.393, 0.769, 0.189],
                          [0.349, 0.689, 0.168],
                          [0.272, 0.534, 0.131]])

multiplier_3 = numpy.array([[0.229, 0.587, 0.114],
                       [0.500, -0.418, -0.082],
                       [-0.168, -0.331, 0.500]])

addend = numpy.array([0, 128, 128])

print("Pobrano już obraz do zadań!")
exercise = input("Jakie zadanie wywołać? Wciśnij nr 1, 2, lub 3: ")

if(exercise == '1'):
    sumOfWeights = kernel.sum()
    if (sumOfWeights == 0):
        sumOfWeights = 1
    kernel = kernel / sumOfWeights
    filteredImage = cv2.filter2D(primaryImageRGB, -1, kernel)

    pyplot.subplot(121), pyplot.imshow(primaryImageRGB), pyplot.title("Primary Image")
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.subplot(122), pyplot.imshow(filteredImage), pyplot.title("Filtered Image")
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.show()
elif(exercise == '2'):
    primaryImageRGB = primaryImageRGB / 255.0
    newRGB = numpy.dot(primaryImageRGB, multiplier_2.T)
    newRGB = numpy.clip(newRGB, 0, 1)
    pyplot.subplot(121), pyplot.imshow(primaryImageRGB), pyplot.title("Primary Image")
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.subplot(122), pyplot.imshow(newRGB), pyplot.title("Filtered Image")
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.show()
elif(exercise == '3'):
    primaryImageRGB = primaryImageRGB / 255.0
    addend = addend / 255.0
    Y = multiplier_3[0][0] * primaryImageRGB[:,:,0] + multiplier_3[0][1] * primaryImageRGB[:, :, 1] \
    +  multiplier_3[0][2] * primaryImageRGB[:, :, 2]
    Cr = addend[1] + multiplier_3[1][0] * primaryImageRGB[:,:,0] + multiplier_3[1][1] \
    * primaryImageRGB[:, :, 1] +  multiplier_3[1][2] * primaryImageRGB[:, :, 2]
    Cb = addend[2] + multiplier_3[2][0] * primaryImageRGB[:,:,0] + multiplier_3[2][1] \
    * primaryImageRGB[:, :, 1] +  multiplier_3[2][2] * primaryImageRGB[:, :, 2]
    Y = numpy.clip(Y, 0, 1)
    Cr = numpy.clip(Cr, 0, 1)
    Cb = numpy.clip(Cb, 0, 1)
    # konwersja odwrotna ------------------------
    R = Y + 1.402 * (Cr - addend[1])
    G = Y - 0.34414 * (Cb - addend[2]) - 0.71414 * (Cr - addend[1])
    B = Y + 1.772 * (Cb - addend[2])
    R = numpy.clip(R, 0, 1)
    G = numpy.clip(G, 0, 1)
    B = numpy.clip(B, 0, 1)
    againRGB = cv2.merge([R, G, B])
    pyplot.subplot(231), pyplot.imshow(primaryImageRGB), pyplot.title("Primary Image")
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.subplot(232), pyplot.imshow(Y, cmap='gray'), pyplot.title("Y")
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.subplot(233), pyplot.imshow(Cr, cmap='gray'), pyplot.title("Cr")
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.subplot(234), pyplot.imshow(Cb, cmap='gray'), pyplot.title("Cb")
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.subplot(235), pyplot.imshow(againRGB), pyplot.title("Again RGB")
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.show()
else:
    print("Nie ma zadania o takim numerze!!!")
