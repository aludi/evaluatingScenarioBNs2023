
from PIL import Image, ImageOps
import random
import csv

#  maps based on : http://maps.stamen.com/terrain/#12/37.7706/-122.3782

class CreateMap():
    def __init__(self, file_name, coverage, height):

        if coverage is not None:
            y = height
            x = int(y*1.5)
            self.rel = 1.5
            csv_file = file_name + ".csv"

            with open(csv_file, 'w') as csvfile:
                writer = csv.writer(csvfile)
                for i in range(0, y):
                    temp = []
                    for j in range(0, x):
                        val = random.randint(0, 100)
                        if val > coverage:
                            temp.append(str(1))
                        else:
                            temp.append(str(0))
                    writer.writerow(temp)

        else:

            img = Image.open(file_name)
            (w, h) = img.size
            rel = round(w/h, 1)
            self.rel = rel
            y = height
            x = int(y*rel)
            reduced_img = img.resize((x,y),resample=Image.BILINEAR)
            result = reduced_img.resize(img.size,Image.NEAREST)
            result = ImageOps.grayscale(result)    # black and white
            #reduced_filename = "Reduced"+file_name
            #result.save(reduced_filename)
            colors = result.getcolors()
            colors = sorted(colors, key = lambda x:-x[0])
            #print(colors[:12])

            csv_file = file_name + ".csv"
            f = []
            for i in range(0, x):
                f.append(str(i))

                with open(csv_file, 'w') as csvfile:
                    writer = csv.writer(csvfile)
                    for i in range(0, y):
                        temp = []
                        for j in range(0, x):
                            val = reduced_img.getpixel((j, i))[0]
                            if val < 199 and val > 189:
                                temp.append(str(0))
                            else:
                                temp.append(str(1))

                        writer.writerow(temp)







