Readability
===========

An implementation of traditional readability measures based on simple surface
characteristics. These measures are basically linear regressions based on the
number of words, syllables, and sentences.

The functionality is modeled after the UNIX ``style(1)`` command. Compared to the
implementation as part of `GNU diction <http://www.moria.de/~michael/diction/>`_,
this version supports UTF-8 encoded text, but expects sentence-segmented and
tokenized text. The syllabification and word type recognition is based on
simple heuristics and only provides a rough measure. The supported languages
are English, German, and Dutch. Adding support for a new language involves the
addition of heuristics for the aforementioned syllabification and word type
recognition; see ``langdata.py``.

NB: all readability formulas were developed for English, so the scales of the
outcomes are only meaningful for English texts. The Dale-Chall measure uses the
original word list for English, but for Dutch and German lists of frequent
words are used that were not specifically selected for recognizability by
school children.

Installation
------------
::

    $ pip install https://github.com/andreasvc/readability/tarball/master

Usage
-----
::

    $ readability --help
    Simple readability measures.

    Usage: readability [--lang=<x>] [FILE]
    or: readability [--lang=<x>] --csv FILES...

    By default, input is read from standard input.
    Text should be encoded with UTF-8,
    one sentence per line, tokens space-separated.

    Options:
      -L, --lang=<x>   Set language (available: de, nl, en).
      --csv            Produce a table in comma separated value format on
                       standard output given one or more filenames.
      --tokenizer=<x>  Specify a tokenizer including options that will be given
                       each text on stdin and should return tokenized output on
                       stdout. Not applicable when reading from stdin.

For proper results, the text should be tokenized.

- For English, I recommend "tokenizer",
  cf. http://moin.delph-in.net/WeSearch/DocumentParsing
- For Dutch, I recommend the tokenizer that is part of the Alpino parser:
  http://www.let.rug.nl/vannoord/alp/Alpino/.
- ``ucto`` is a  general multilingual tokenizer: http://ilk.uvt.nl/ucto

Example using ``ucto``::

    $ ucto -L en -n -s '' "CONRAD, Joseph - Lord Jim.txt" | readability
    [...]
    readability grades:
        Kincaid:                          5.44
        ARI:                              6.39
        Coleman-Liau:                     6.91
        FleschReadingEase:               85.17
        GunningFogIndex:                  9.86
        LIX:                             31.98
        SMOGIndex:                        9.39
        RIX:                              2.56
        DaleChallIndex:                   8.02
    sentence info:
        characters_per_word:              4.17
        syll_per_word:                    1.24
        words_per_sentence:              16.35
        sentences_per_paragraph:         11.5
        type_token_ratio:                 0.09
        characters:                  551335
        syllables:                   164205
        words:                       132211
        wordtypes:                    12071
        sentences:                     8087
        paragraphs:                     703
        long_words:                   20670
        complex_words:                10990
        complex_words_dc:             29908
    word usage:
        tobeverb:                      3907
        auxverb:                       1630
        conjunction:                   4398
        pronoun:                      18092
        preposition:                  19290
        nominalization:                1167
    sentence beginnings:
        pronoun:                       2578
        interrogative:                  217
        article:                        629
        subordination:                  120
        conjunction:                    236
        preposition:                    397

The option ``--csv`` collects readability measures for a number of texts in
a table. To tokenize documents on-the-fly when using this option, use
the ``--tokenizer`` option. Example with the "tokenize" tool::

    $ readability --csv --tokenizer='tokenizer -L en-u8 -P -S -E "" -N' */*.txt >readabilitymeasures.csv

References
----------
The following readability metrics are included:

1. http://en.wikipedia.org/wiki/Automated_Readability_Index
2. http://en.wikipedia.org/wiki/SMOG
3. http://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_Grade_Level#Flesch.E2.80.93Kincaid_Grade_Level
4. http://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_test#Flesch_Reading_Ease
5. http://en.wikipedia.org/wiki/Coleman-Liau_Index
6. http://en.wikipedia.org/wiki/Gunning-Fog_Index
7. https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula

For better readability measures, consider the following:

- Collins-Thompson & Callan (2004). A language modeling approach to predicting reading difficulty.
  In Proc. of HLT/NAACL, pp. 193-200. http://aclweb.org/anthology/N04-1025.pdf
- Schwarm & Ostendorf (2005). Reading level assessment using SVM and statistical language models.
  Proc. of ACL, pp. 523-530. http://www.aclweb.org/anthology/P05-1065.pdf
- The Lexile framework for reading. http://www.lexile.com
- Coh-Metrix. http://cohmetrix.memphis.edu/
- Stylene: http://www.clips.ua.ac.be/category/projects/stylene
- T-Scan: http://languagelink.let.uu.nl/tscan

Acknowledgments
---------------
The code is based on: https://github.com/mmautner/readability

Which in turn was based on: https://github.com/nltk/nltk_contrib/tree/master/nltk_contrib/readability
