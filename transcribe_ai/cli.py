import sys
import argparse

from transcribe_ai.main import process_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    # print(args)
    process_files(args.path)


if __name__ == "__main__":
    sys.exit(main())

