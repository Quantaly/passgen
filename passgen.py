#!/usr/bin/python3
import argparse
import math
import re
import secrets
import string
import sys


DEFAULT_WORD_LIST = "/usr/share/dict/words"
SIMPLE_SYMBOLS = "!@#$%^&*"  # only from the number row and not parentheses


def print_err(*args, **kwargs):
    "Prints to stderr."
    print(*args, file=sys.stderr, **kwargs)


def load_word_list(path: str, min_word_length: int, max_word_length: int) -> list[str]:
    """
    Loads a word list from the provided path.
    Each word should be on its own line
    and consist only of lowercase ASCII letters;
    any line containing characters outside the range [a-z] is discarded.

    If max_word_length is less than min_word_length, it is ignored.
    Both bounds are inclusive.
    """
    if min_word_length < 1:
        min_word_length = 1

    if max_word_length > min_word_length:
        regex = f"[a-z]{{{min_word_length},{max_word_length}}}"
    elif max_word_length == min_word_length:
        regex = f"[a-z]{{{min_word_length}}}"
    else:
        regex = f"[a-z]{{{min_word_length},}}"

    with open(path) as word_list:
        return list(
            set(  # merge duplicates
                filter(
                    lambda w: re.fullmatch(regex, w),
                    map(str.strip, word_list),
                )
            )
        )


def generate_password(word_list: list[str], word_count: int) -> str:
    """
    Generates a password of the form "correct horse battery staple"
    using the provided word list.
    """
    return " ".join(secrets.choice(word_list) for _ in range(word_count))


def generate_password_requirements(word_list: list[str], word_count: int) -> str:
    """
    Generates a password of the form "CorrectHorseBatteryStaple!1"
    using the provided word list.
    """
    return (
        "".join(str.title(secrets.choice(word_list)) for _ in range(word_count))
        + secrets.choice(SIMPLE_SYMBOLS)
        + secrets.choice(string.digits)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a password in the style of https://xkcd.com/936/",
        epilog="The word list file should contain one word on each line, "
        "consisting only of lowercase ASCII letters. "
        "Lines containing other characters are discarded.",
    )
    parser.add_argument(
        "-w",
        "--word-list",
        help=f"file to read words from (default: {DEFAULT_WORD_LIST})",
    )
    parser.add_argument(
        "-m",
        "--min-word-length",
        default=4,
        type=int,
        help="minimum word length (default: 4)",
    )
    parser.add_argument(
        "-M",
        "--max-word-length",
        default=10,
        type=int,
        help="maximum word length (default: 10) (ignored if less than the minimum)",
    )
    parser.add_argument(
        "-c",
        "--word-count",
        default=4,
        type=int,
        help="number of words in the password (default: 4)",
    )
    parser.add_argument(
        "-r",
        "--requirements",
        action="store_true",
        help="include capitals, a symbol, and a digit to satisfy arbitrary requirements",
    )
    parser.add_argument(
        "-n",
        "--password-count",
        default=1,
        type=int,
        help="generate multiple passwords to choose from",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="increase output verbosity",
    )
    args = parser.parse_args()

    if args.word_list:
        word_list = load_word_list(
            args.word_list,
            args.min_word_length,
            args.max_word_length,
        )
    else:
        try:
            word_list = load_word_list(
                DEFAULT_WORD_LIST,
                args.min_word_length,
                args.max_word_length,
            )
        except FileNotFoundError:
            print_err(
                f"Could not open default word list ({DEFAULT_WORD_LIST}). Please specify a word list file with -w",
            )
            sys.exit(1)
    if len(word_list) == 0:
        print_err(
            "No words loaded. Try specifying a wider range of allowable word lengths."
        )
        sys.exit(1)
    if args.verbose:
        print_err(f"{len(word_list)} words loaded.")

    if args.requirements:
        if args.verbose:
            print_err(
                f"Password has ~{args.word_count * math.log2(len(word_list)) + math.log2(len(SIMPLE_SYMBOLS)) + math.log2(len(string.digits)):.2f} bits of entropy."
            )
        for _ in range(args.password_count):
            print(generate_password_requirements(word_list, args.word_count))
    else:
        if args.verbose:
            print_err(
                f"Password has ~{args.word_count * math.log2(len(word_list)):.2f} bits of entropy."
            )
        for _ in range(args.password_count):
            print(generate_password(word_list, args.word_count))
