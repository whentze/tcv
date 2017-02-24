#!/usr/bin/python3

from PIL import Image, ImageFilter
from statistics import median
import shutil, argparse

def bilevel_block(ul, ur, dl, dr, treshold = 100):
    bools = list(map(lambda pix : pix > treshold, [ul, ur, dl, dr]))
    return " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"[bools[0]+2*bools[1]+4*bools[2]+8*bools[3]]

def truecolor_block(string, fg, bg):
    if(bg == "none"):
        return "\x1b[38;2;{};{};{}m{}".format(fg[0], fg[1], fg[2], string)
    else:
        return "\x1b[38;2;{};{};{};48;2;{};{};{}m{}".format(fg[0], fg[1], fg[2], bg[0], bg[1], bg[2], string)

def print_image_bl(img):
    out = ""
    for y in range(0, img.height-1, 2):
        for x in range(0, img.width-1, 2):
            ul = img.getpixel((x  , y  ))
            ur = img.getpixel((x+1, y  ))
            dl = img.getpixel((x  , y+1))
            dr = img.getpixel((x+1, y+1))
            out += bilevel_block(ul, ur, dl, dr)
        if(img.width % 2 == 1):
            ul = img.getpixel((img.width-1 ,y  ))
            dl = img.getpixel((img.width-1 ,y+1))
            out += bilevel_block(ul, 0, dl, 0)
        out += "\n"
    if(img.height % 2 == 1):
        for x in range(0, img.width-1, 2):
            ul = img.getpixel((x   ,img.height-1))
            ur = img.getpixel((x+1 ,img.height-1))
            out += bilevel_block(ul, ur, 0, 0)
        if(img.width % 2 == 1):
            ul = img.getpixel((img.width-1, img.height-1))
            out += bilevel_block(ul, 0, 0, 0)
    print(out)

def print_image_tc(img):
    out = ""
    for y in range(0, img.height-1, 2):
        for x in range(img.width):
            upper = img.getpixel((x,y))
            lower = img.getpixel((x,y+1))
            out += truecolor_block("▀", upper, lower)
        out += "\n"
    if(img.height % 2 == 1):
        out += "\x1b[0m"
        for x in range(img.width):
            upper = img.getpixel((x, img.height-1))
            out += truecolor_block("▀", upper, "none")
    out += "\x1b[0m"
    print(out)

def print_fitting(path):
    img      = Image.open(path)
    termsize = shutil.get_terminal_size((9001, 9001))
    if args.bilevel:
        scale    = min(1, termsize[0]/img.size[0], 2*(termsize[1]-2)/(img.size[1]))
        newsize  = (2*int(scale*img.size[0]), int(scale*img.size[1]))
        newimg   = img.convert("1").resize(newsize, Image.LANCZOS)
        print_image_bl(newimg)
    else:
        scale    = min(1, termsize[0]/img.size[0], 2*(termsize[1]-2)/(img.size[1]))
        newsize  = (int(scale*img.size[0]), int(scale*img.size[1]))
        newimg   = img.convert("RGBA").resize(newsize, Image.LANCZOS)
        print_image_tc(newimg)

def error(errorstring):
    if not args.quiet:
        print(errorstring)

def main():
    for arg in args.images:
        try:
            print_fitting(arg)
        except IsADirectoryError:
            error(arg + ": Is a directory, skipping.")
        except FileNotFoundError:
            error(arg + ": No such file or directory, skipping.")
        except OSError:
            error(arg + ": Not a known format, skipping.")
        except ValueError:
            error(arg + ": Weird Dimensions, skipping.")
        finally:
            if (len(args.images) > 1):
                print(arg)


parser = argparse.ArgumentParser(
    description='A script to print image files to a terminal using true-color codes'
)
parser.add_argument('images', metavar='File', type=str, nargs='+', help='Filenames of images to display')
parser.add_argument('--bilevel', '-b',help='Don\'t use colors. Instead, bilevel black/white blocks', action="store_true")
parser.add_argument('--quiet', '-q', help ='Don\'t print any errors.', action='store_true')
args = parser.parse_args()
main()
