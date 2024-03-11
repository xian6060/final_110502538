import miniLisp
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='miniLisp interpreter') # python .\main.py -h 
    parser.add_argument('-f', '--file', type=str, help='Input file') # -f --file
    args = parser.parse_args()

    miniLisp.MiniLisp().interprete(args.file)