clustalo-python
===============

This is just a simple Python wrapper around Clustal Omega
(http://www.clustal.org/omega/), used internally at Benchling, then modified
for easier building by Cyrus Biotechnology.

Support for OSX requires the libomp library, and automake from brew. You may install it via:

```
brew install libomp automake

```

Usage
-----
::

  from clustalo import clustalo
  input = {
      'seq1': 'AAATCGGAAA',
      'seq2': 'CGGA'
  }
  aligned = clustalo(input)
  # aligned is a dict of aligned sequences:
  #   seq1: AAATCGGAAA
  #   seq2: ----CGGA--

At the moment, input sequences are assumed to not be aligned (i.e. there is no
dealign option). See ``clustalo.clustalo.__doc__`` or file ``clustaslo/clustalo.c``
for documentation.
