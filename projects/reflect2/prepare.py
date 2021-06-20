import sys, os
import argparse
import glob
import json
import uuid


def main(argv):
    print("prepare image")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in", action="store", required=True, dest="indir", help="image input directory")

    parser.add_argument("-o", "--out", action="store", required=True, dest="out", help="image output directory")

    parser.add_argument("-c", "--colors", action="store", required=True, dest="colors", help="colors file")

    parser.add_argument("--generate_id", help="generate new id", action="store_true")

    args = parser.parse_args()


if __name__ == "__main__":
    main(sys.argv[1:])
