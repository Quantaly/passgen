# passgen

A program for generating passwords in the style of https://xkcd.com/936/ ("correct horse battery staple"). Basically a blown-up version of one of [the examples in the documentation for Python's `secrets` module](https://docs.python.org/3/library/secrets.html#recipes-and-best-practices).

## Installation

Clone the repository:

```sh
git clone https://github.com/Quantaly/passgen
```

If you do not have a /usr/share/dict/words, you will need a word list to provide to the program. A couple of English lists I found:

- [ENABLE](https://www.wordgamedictionary.com/enable/download/enable.txt) is apparently public domain and is used in Words with Friends.
- [www.wordfrequency.info](https://www.wordfrequency.info/samples.asp) provides a freely downloadable spreadsheet of their top 5000 English words. The column must be copy-pasted into a text file for use with this application, but the words are generally more recognizable than the ENABLE list.

## Usage

```
$ python3 passgen.py --help
usage: passgen.py [-h] [-w WORD_LIST] [-m MIN_WORD_LENGTH] [-M MAX_WORD_LENGTH] [-c WORD_COUNT] [-r] [-n PASSWORD_COUNT] [-v]

Generate a password in the style of https://xkcd.com/936/

options:
  -h, --help            show this help message and exit
  -w WORD_LIST, --word-list WORD_LIST
                        file to read words from (default: /usr/share/dict/words)
  -m MIN_WORD_LENGTH, --min-word-length MIN_WORD_LENGTH
                        minimum word length (default: 4)
  -M MAX_WORD_LENGTH, --max-word-length MAX_WORD_LENGTH
                        maximum word length (default: 10) (ignored if less than the minimum)
  -c WORD_COUNT, --word-count WORD_COUNT
                        number of words in the password (default: 4)
  -r, --requirements    include capitals, a symbol, and a digit to satisfy arbitrary requirements
  -n PASSWORD_COUNT, --password-count PASSWORD_COUNT
                        generate multiple passwords to choose from
  -v, --verbose         increase output verbosity

The word list file should contain one word on each line, consisting only of lowercase ASCII letters. Lines containing other characters are discarded.
```

## A note about word lists

The program will default to looking for a word list at /usr/share/dict/words. If the file does not exist (for example, on Windows machines where that isn't a file path), you must specify a custom word list file using the `-w` option.

For best results, the word list should be comprised entirely or mostly of words that you actually know. In particular, because /usr/share/dict/words is different on different Linux distributions, I cannot make any guarantees about the default experience. A very small but illustrative sample:

|                                              | Ubuntu 20.04                              | Fedora 39                                  |
| -------------------------------------------- | ----------------------------------------- | ------------------------------------------ |
| total word count                             | 102,401 words                             | 479,826 words                              |
| filtered word count (4-10 lowercase letters) | 51,147 words                              | 234,842 words                              |
| example output                               | `upholsters derelict biochemist handpick` | `polybranch haematitic tentable propionyl` |

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate. <!-- is what this template says, imagine having tests lol -->

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/) or later
