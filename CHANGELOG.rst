Release History
===============

v1.0.6
------
* Allowing usage of custom word and sentence tokenizers.

v1.0.5
------
* Adding python typing for better/clear interfaces.
* Found a bug in phrase list which was being returned as a set causing it to drop repeated
phrases and consider only the first one. Provided control over this as a flag that Rake takes
so that users can control the behaviour.

v1.0.4
------
* Adding support for min and max words (inclusive) limits for ranked phrases.


v1.0.3
------
* Adding support for various metrics mentioned in the paper.


v1.0.2
------
* Minor fixes.


v1.0.1
------
* Adding support for other languages.


v1.0.0
------
* First release.
