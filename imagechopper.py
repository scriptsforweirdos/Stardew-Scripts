import argparse
import os
import pprint
import sys

from PIL import Image


def chopImages(inputData):
    origin = Image.open(inputData["srcFile"])
    filePrefix = inputData["srcFile"].rsplit("/", 1)[1][0:-4]
    basewidth, baseheight = origin.size
    spriteWidth = inputData["originWidth"]
    spriteHeight = inputData["originHeight"]
    rows = int(baseheight / inputData["originHeight"])
    cols = int(basewidth / inputData["originWidth"])
    lefts = [spriteWidth * x for x in range(0, cols)]
    tops = [spriteHeight * x for x in range(0, rows)]
    wpercent = (inputData["outWidth"] / float(spriteWidth))
    outWidth = inputData["outWidth"]
    outHeight = int((float(spriteHeight) * float(wpercent)))
    destDir = inputData["destDir"]
    if destDir[-1] != "/":
        destDir += "/"
    i = 0
    left = lefts[0]
    top = tops[0]
    filenames = None
    if "names" in inputData and inputData["names"]:
        with open(inputData["names"], 'r') as f:
            filenames = [line.rstrip() for line in f]
    for top in tops:
        for left in lefts:
            savepath = None
            img_crop = origin.crop((left, top, left + spriteWidth, top + spriteHeight))
            img_res = img_crop.resize((outWidth, outHeight), Image.Resampling.NEAREST)
            if not filenames or len(filenames) < i:
                savepath = "{}{}_{}.png".format(destDir, filePrefix, i)
            elif len(filenames) > i:
                savepath = "{}{}_{}.png".format(destDir, filePrefix, filenames[i])
            img_res.save(savepath)
            i += 1


def getInput():
    inputData = {}
    srcFileRaw = input("Where is the file you wish to chop?: ")
    while "srcFile" not in inputData:
        if not os.path.exists(srcFileRaw) or not srcFileRaw.endswith(".png"):
            srcFileRaw = input("That path does not exist. Try again? ")
        else:
            inputData["srcFile"] = srcFileRaw.replace("\\", "/")
    print(inputData["srcFile"])
    originWidth = input("How wide is a sprite in that file?: ")
    while "originWidth" not in inputData:
        if not originWidth.isnumeric() or int(originWidth) < 1:
            originWidth = input("Invalid number. Try again?: ")
        else:
            inputData["originWidth"] = int(originWidth)
    originHeight = input("How tall is a sprite in that file?: ")
    while "originHeight" not in inputData:
        if not originHeight.isnumeric() or int(originHeight) < 1:
            originHeight = input("Invalid number. Try again?: ")
        else:
            inputData["originHeight"] = int(originHeight)
    destDir = input("Where would you like to save the new images?: ")
    while "destDir" not in inputData:
        if not os.path.isdir(destDir):
            destDir = input("Invalid path. Try again?: ")
        else:
            inputData["destDir"] = destDir.replace("\\", "/")
    outWidth = input("How wide should the new images be?: ")
    while "outWidth" not in inputData:
        if not outWidth.isnumeric() or int(outWidth) < 1:
            outWidth = input("Invalid number. Try again?: ")
        else:
            inputData["outWidth"] = int(outWidth)
    fileName = inputData["srcFile"].rsplit("/", 1)[1][0:-4]
    print("Files will be named numerically {}_1.png, {}_2.png, etc unless you have a name list text file with one name per line".format(fileName, fileName))
    names = input("If you have a txt file with image names, where is that file? (Press Enter to skip): ")
    if names:
        while "names" not in inputData:
            if os.path.exists(names) and names.endswith(".txt"):
                inputData["names"] = names.replace("\\", "/")
            else:
                names = input("Invalid path. Try again.: ")
    return inputData


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError("{} is not a valid path".format(path))


def img_path(path):
    if os.path.exists(path) and path.endswith(".png"):
        return path
    else:
        raise argparse.ArgumentTypeError("{} is not a valid path".format(path))


def txt_path(path):
    if os.path.exists(path) and path.endswith(".txt"):
        return path
    else:
        raise argparse.ArgumentTypeError("{} is not a valid path".format(path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--i", "-input", dest="srcFile", type=img_path, help="Path to source file")
    parser.add_argument("--w", "-width", dest="originWidth", type=int, help="Sprite width")
    parser.add_argument("--h", "-height", dest="originHeight", type=int, help="Sprite height")
    parser.add_argument("--o", "-output", dest="destDir", type=dir_path, help="Path to destination directory")
    parser.add_argument("--rw", "-resultwidth", dest="outWidth", type=int, help="Output width")
    parser.add_argument("--n", "-names", dest="nameList", type=txt_path, help="Path to list of names (optional)")
    args = parser.parse_args()
    shortcutNeeded = True
    if args.srcFile and args.originWidth and args.originHeight and args.destDir and args.outWidth:
        inputData = {"srcFile": args.srcFile.strip('"').strip("'"),
                     "originWidth": args.originWidth,
                     "originHeight": args.originHeight,
                     "destDir": args.destDir.strip('"').strip("'"),
                     "outWidth": args.outWidth,
                     "names": None}
        try:
            inputData["names"] = args.names.strip('"').strip("'")
        except Exception:
            pass
        shortcutNeeded = False
    else:
        inputData = getInput()
    chopImages(inputData)
    print("Images saved to {}".format(inputData["destDir"]))
    if shortcutNeeded:
        if "names" in inputData and inputData["names"]:
            outStr = 'To repeat this process quickly, type:\npython imagechopper.py --i="{}" --w={} --h={} --o="{}" --rw={}, --n="{}"'.format(inputData["srcFile"], inputData["originWidth"], inputData["originHeight"], inputData["destDir"], inputData["outWidth"], inputData["names"])
        else:
            outStr = 'To repeat this process quickly, type:\npython imagechopper.py --i="{}" --w={} --h={} --o="{}" --rw={}'.format(inputData["srcFile"], inputData["originWidth"], inputData["originHeight"], inputData["destDir"], inputData["outWidth"])
        print(outStr)
