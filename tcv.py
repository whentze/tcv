#!/usr/bin/python3

from PIL import Image
import shutil, argparse

def print_tc(string, fg, bg):
    if(bg == "none"):
        print("\x1b[38;2;{};{};{}m{}".format(fg[0], fg[1], fg[2], string), end="")
    else:
        print("\x1b[38;2;{};{};{};48;2;{};{};{}m{}".format(fg[0], fg[1], fg[2], bg[0], bg[1], bg[2], string), end="")

def print_image(img):
    for y in range(0, img.height-1, 2):
        for x in range(img.width):
            upper = img.getpixel((x,y))
            lower = img.getpixel((x,y+1))
            print_tc("▀", upper, lower)
        print("\x1b[0m")
    if(img.height % 2 == 1):
        print("\x1b[0m", end="")
        for x in range(img.width):
            upper = img.getpixel((x, img.height-1))
            print_tc("▀", upper, "none")
        print("\x1b[0m")

def print_fitting(path):
    img      = Image.open(path)
    termsize = shutil.get_terminal_size((9001, 9001))
    scale    = min(1, termsize[0]/img.size[0], 2*(termsize[1]-2)/(img.size[1]))
    newsize  = (int(scale*img.size[0]), int(scale*img.size[1]))
    newimg   = img.convert("RGBA").resize(newsize, Image.LANCZOS)
    
    print_image(newimg)

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
parser.add_argument('--quiet', '-q', help ='Don\'t print any errors.', action='store_true')
args = parser.parse_args()
main()
