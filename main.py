import os
import requests

# вывести текущую директорию
print("Текущая деректория:", os.getcwd())

if os.path.isdir("map"):
     os.rmdir("map")
os.mkdir("map")
# https://a.tile-cyclosm.openstreetmap.fr/cyclosm/1/1/1.png
zmax = 5
zmin = 1
urlbase = 'a.tile-cyclosm.openstreetmap.fr/cyclosm/'

for z in range(zmin,zmax+1):
    os.makedirs("map/"+str(z))
    for x in range(0, 2 ** z):
        os.makedirs("map/"+str(z)+'/'+str(x))
        for y in range(0, 2 ** z):
            url = 'https://'+urlbase+str(z)+'/'+str(x)+'/'+str(y)+'.png'
            data = requests.get(url).content
            print(url)
            f = open("map/"+str(z)+'/'+str(x)+'/'+str(y)+'.png','wb')
            # Storing the image data inside the data variable to the file
            f.write(data)
            f.close()
            #open("map/1/text.txt", "w")