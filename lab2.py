import cv2 
import numpy 
from matplotlib import pyplot
import math

user_input = ''
while user_input != '0':
    print("Jakie zadanie wywołać?")
    print("Wciśnij nr 1 - zadanie nr 4 lab 1")
    print("Wciśnij nr 2 - zadanie nr 5 lab 1")
    print("Wciśnij nr 3 - zadanie nr 1 lab 2")
    print("Wciśnij nr 4 - zadanie nr 2 lab 2")
    print("Wciśnij nr 0 - zakończ program")
    user_input = input("Nr: ")

    if user_input == '1':
        def downsampling(image, k):
            if not k > 0:
                result = image
            else:
                result = cv2.pyrDown(image)
                for _ in range(k-1):
                    result = cv2.pyrDown(result)
            return result

        def upsampling(image, k):
            if not k > 0:
                result = image
            else:
                result = cv2.pyrUp(image)
                for _ in range(k-1):
                    result = cv2.pyrUp(result)
            return result

        primaryImageBGR = cv2.imread("images/kwiatki.jpg")
        primaryImageRGB = cv2.cvtColor(primaryImageBGR, cv2.COLOR_BGR2RGB)

        yCrCb = cv2.cvtColor(primaryImageRGB, cv2.COLOR_RGB2YCrCb)

        Y = yCrCb[:, :, 0]
        Cr = yCrCb[:, :, 1]
        Cb = yCrCb[:, :, 2]

        CrAfterDown = downsampling(Cr, 1)
        CbAfterDown = downsampling(Cb, 1)

        CrAfterUp = upsampling(CrAfterDown, 1)
        CbAfterUp = upsampling(CbAfterDown, 1)

        againYCrCb = cv2.merge([Y, CrAfterUp, CbAfterUp])

        againRGB = cv2.cvtColor(againYCrCb, cv2.COLOR_YCrCb2RGB)

        pyplot.subplot(231), pyplot.imshow(primaryImageRGB), pyplot.title("Primary Image")
        pyplot.xticks([]), pyplot.yticks([])
        pyplot.subplot(232), pyplot.imshow(Y, cmap='gray'), pyplot.title("Y")
        pyplot.xticks([]), pyplot.yticks([])
        pyplot.subplot(233), pyplot.imshow(CrAfterUp, cmap='gray'), pyplot.title("Cr")
        pyplot.xticks([]), pyplot.yticks([])
        pyplot.subplot(234), pyplot.imshow(CbAfterUp, cmap='gray'), pyplot.title("Cb")
        pyplot.xticks([]), pyplot.yticks([])
        pyplot.subplot(235), pyplot.imshow(againRGB), pyplot.title("Again RGB")
        pyplot.xticks([]), pyplot.yticks([])
        pyplot.show()
    
    elif user_input == '2':
        primaryImageBGR = cv2.imread("images/kwiatki.jpg")
        primaryImageRGB = cv2.cvtColor(primaryImageBGR, cv2.COLOR_BGR2RGB)

        def downsampling(image, k):
            if not k > 0:
                result = image
            else:
                result = cv2.pyrDown(image)
                for _ in range(k-1):
                    result = cv2.pyrDown(result)
            return result

        def upsampling(image, k):
            if not k > 0:
                result = image
            else:
                result = cv2.pyrUp(image)
                for _ in range(k-1):
                    result = cv2.pyrUp(result)
            return result

        def doMSE(matrix1, matrix2):
            return numpy.mean((matrix1 - matrix2)**2)

        yCrCb = cv2.cvtColor(primaryImageRGB, cv2.COLOR_RGB2YCrCb)

        Y = yCrCb[:, :, 0]
        Cr = yCrCb[:, :, 1]
        Cb = yCrCb[:, :, 2]

        Y = numpy.clip(Y, 0, 1)
        Cr = numpy.clip(Cr, 0, 1)
        Cb = numpy.clip(Cb, 0, 1)

        CrAfterDown = downsampling(Cr, 1)
        CbAfterDown = downsampling(Cb, 1)

        CrAfterUp = upsampling(CrAfterDown, 1)
        CbAfterUp = upsampling(CbAfterDown, 1)

        againYCrCb = cv2.merge([Y, CrAfterUp, CbAfterUp])

        againRGB = cv2.cvtColor(againYCrCb, cv2.COLOR_YCrCb2RGB)

        max_possible_mse = (255.0**2) 

        if(againRGB.size != primaryImageRGB.size):
            print("Obrazy mają różną liczbę pikseli!!! Koniec programu")
        else:
            print("MSE = " + str("{:.2f}".format(doMSE(primaryImageRGB, againRGB))))
            print("Maksymalne możliwe MSE:", max_possible_mse) 
    
    elif user_input == '3':
        class PPM:
            def __init__(self, width, height, color_range):
                self.width = width
                self.height = height
                self.color_range = color_range
                self.pixels = []

            def add_pixel(self, x, y, color_rgb):
                self.pixels.append((x, y, color_rgb))

            def saveP3(self, filename):
                with open(filename, 'w') as file:
                    file.write(f'P3\n{self.width} {self.height}\n{self.color_range}\n')
                    for pixel in self.pixels:
                        file.write(f'{pixel[2][0]} {pixel[2][1]} {pixel[2][2]}\n')

            def saveP6(self, filename):
                with open(filename, 'wb') as file:
                    header = f'P6\n{self.width} {self.height}\n{self.color_range}\n'
                    header_bytes = header.encode('utf-8')
                    file.write(bytearray(header_bytes))
                    for pixel in self.pixels:
                        file.write(bytes(pixel[2]))

        def saveImage_P3(image, filename):
            height = len(image)
            width = len(image[0])
            color_range = 255
            with open(filename, 'w') as file:
                file.write(f'P3\n{width} {height}\n{color_range}\n')
                for i in range(height):
                    for j in range(width):
                        file.write(f'{image[i, j, 0]} {image[i, j, 1]} {image[i, j, 2]}\n')

        def saveImage_P6(image, filename):
            height = len(image)
            width = len(image[0])
            color_range = 255
            with open(filename, 'wb') as file:
                header = f'P6\n{width} {height}\n{color_range}\n'
                header_bytes = header.encode('utf-8')
                file.write(bytearray(header_bytes))
                for i in range(height):
                    for j in range(width):
                        file.write(bytes(image[i, j]))


        sketch = PPM(2, 2, 255)
        sketch.add_pixel(0, 0, (255, 0, 0))
        sketch.add_pixel(0, 1, (0, 255, 0))
        sketch.add_pixel(1, 0, (0, 0, 255))
        sketch.add_pixel(1, 1, (255, 0, 255))

        sketch.saveP3('szkicP3.ppm')
        sketch.saveP6('szkicP6.ppm')

        sketch_from_file_P3 = cv2.imread('szkicP3.ppm')
        sketch_from_file_P6 = cv2.imread('szkicP6.ppm')
        sketch_from_file_P3 = cv2.cvtColor(sketch_from_file_P3, cv2.COLOR_BGR2RGB)
        sketch_from_file_P6 = cv2.cvtColor(sketch_from_file_P6, cv2.COLOR_BGR2RGB)

        primaryImageBGR = cv2.imread("images/krajobraz.jpg")
        primaryImageRGB = cv2.cvtColor(primaryImageBGR, cv2.COLOR_BGR2RGB)

        saveImage_P3(primaryImageRGB, 'photoP3.ppm')
        saveImage_P6(primaryImageRGB, 'photoP6.ppm')

        image_from_file_P3 = cv2.imread('photoP3.ppm')
        image_from_file_P6 = cv2.imread('photoP6.ppm')
        image_from_file_P3 = cv2.cvtColor(image_from_file_P3, cv2.COLOR_BGR2RGB)
        image_from_file_P6 = cv2.cvtColor(image_from_file_P6, cv2.COLOR_BGR2RGB)

        pyplot.subplot(221), pyplot.imshow(sketch_from_file_P3), pyplot.title("Sketch PPM P3")
        pyplot.subplot(222), pyplot.imshow(sketch_from_file_P6), pyplot.title("Sketch PPM P6")
        pyplot.subplot(223), pyplot.imshow(image_from_file_P3), pyplot.title("Image PPM P3")
        pyplot.subplot(224), pyplot.imshow(image_from_file_P6), pyplot.title("Image PPM P6")
        pyplot.show()
    
    elif user_input == '4':
        class PPM:
            def __init__(self, width, height, color_range):
                self.width = width
                self.height = height
                self.color_range = color_range
                self.pixels = []

            def add_pixel(self, x, y, color_rgb):
                self.pixels.append((x, y, color_rgb))

            def saveP3(self, filename):
                with open(filename, 'w') as file:
                    file.write(f'P3\n{self.width} {self.height}\n{self.color_range}\n')
                    for pixel in self.pixels:
                        file.write(f'{pixel[2][0]} {pixel[2][1]} {pixel[2][2]}\n')
            
            def setRainbow(self):
                transition = (self.width - 1) / 7
                term = self.color_range / transition
                term = int(term)
                for i in range(self.height):
                    red = 0
                    green = 0
                    blue = 0
                    self.add_pixel(i, 0, (red, green, blue))
                    for j in range(self.width - 1):
                        if j < transition:
                            blue += term
                        elif j >= transition and j < transition*2:
                            green += term
                        elif j >= transition*2 and j < transition*3:
                            blue -= term
                        elif j >= transition*3 and j < transition*4:
                            red += term
                        elif j >= transition*4 and j < transition*5:
                            green -= term
                        elif j >= transition*5 and j < transition*6:
                            blue += term
                        elif j >= transition*6 and j < transition*7:
                            green += term
                        else:
                            red = 0
                            green = 0
                            blue = 0
                        self.add_pixel(i, j+1, (red, green, blue))

            def setBlackAndWhite(self):
                for i in range(self.height):
                    for j in range(self.width):
                        self.add_pixel(i, j, (j, j, j))


        spectrumRainbow = PPM(1786, 100, 255)
        spectrumRainbow.setRainbow()
        spectrumRainbow.saveP3('spektrum-teczowe.ppm')

        spectrumBlackAndWhite = PPM(256, 100, 255)
        spectrumBlackAndWhite.setBlackAndWhite()
        spectrumBlackAndWhite.saveP3('spektrum-czarno-biale.ppm')

        spectrumRainbow_from_file = cv2.imread('spektrum-teczowe.ppm')
        spectrumBlackAndWhite_from_file = cv2.imread('spektrum-czarno-biale.ppm')
        spectrumRainbow_from_file = cv2.cvtColor(spectrumRainbow_from_file, cv2.COLOR_BGR2RGB)
        spectrumBlackAndWhite_from_file = cv2.cvtColor(spectrumBlackAndWhite_from_file, cv2.COLOR_BGR2RGB)

        pyplot.subplot(211), pyplot.imshow(spectrumRainbow_from_file), pyplot.title("Spectrum (1,...,8)")
        pyplot.subplot(212), pyplot.imshow(spectrumBlackAndWhite_from_file), pyplot.title("Spectrum (1 - 8)")
        pyplot.show()