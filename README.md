# rake-nltk

[![Build Status](https://travis-ci.org/csurfer/rake-nltk.svg?branch=master)](https://travis-ci.org/csurfer/rake-nltk)
[![Licence](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/csurfer/rake-nltk/master/LICENSE)

RAKE short for Rapid Automatic Keyword Extraction algorithm, is a domain independent keyword extraction algorithm which tries to determine key phrases in a body of text by analyzing the frequency of word appearance and its co-occurance with other words in the text.

![Demo](http://i.imgur.com/wVOzU7y.gif)

## References

This is a python implementation of the algorithm as mentioned in paper [Automatic keyword extraction from individual documents by Stuart Rose, Dave Engel, Nick Cramer and Wendy Cowley](https://www.researchgate.net/profile/Stuart_Rose/publication/227988510_Automatic_Keyword_Extraction_from_Individual_Documents/links/55071c570cf27e990e04c8bb.pdf)

## Why I chose to implement it myself?

- It is extremely fun to implement algorithms by reading papers. It is the digital equivalent of DIY kits.
- There are some rather popular implementations out there, in python([aneesha/RAKE](https://github.com/aneesha/RAKE)) and node([waseem18/node-rake](https://github.com/waseem18/node-rake)) but neither seemed to use the power of [NLTK](http://www.nltk.org/). By making NLTK an integral part of the implementation I get the flexibility and power to extend it in other creative ways, if I see fit later, without having to implement everything myself.
- I plan to use it in my other pet projects to come and wanted it to be modular and tunable and this way I have complete control.

## Versions of python this code is tested against

- 2.7
- 3.4
- 3.5
- 3.6

## Contributing

### Bug Reports and Feature Requests
Please use [issue tracker](https://github.com/csurfer/rake-nltk/issues) for reporting bugs or feature requests.

### Development
Pull requests are most welcome.
