import qrcode


data = input("Enter the URL of your website:  ")
filname = input("Enter the file name:  ")


if not (filname.endswith(".png")):
    filname += ".png"


img = qrcode.make(data)
img.save(filname)    