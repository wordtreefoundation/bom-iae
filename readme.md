The Book of Mormon: Internet-Annotated Edition
-----

The Internet-Annotated Edition of the Book of Mormon is a public resource curated by volunteer editors from around the world. It is a critical examination of the origins of the book, with sources and references.

This github repository is the static-site generator for http://annotate.wordtree.org. It does not contain any annotations, although it does contain the raw Book of Mormon data in JSON format, which may be useful for other projects (see data/bom.json).

Installation
-----

If you'd like to host your own annotated Book of Mormon, you'll need these components on your server:

- elasticsearch
- python
- annotator-store (backend to JS-annotator)
- nginx or apache

And you'll need these on your development box (laptop, what have you):

- ruby (and bundler)


Once the above prerequisites are installed on your server, you can build and deploy BoM:IAE like so:

```
bundle install
```

```
middleman build
```

```
middleman deploy
```

(See http://middlemanapp.com/basics/getting-started/ for Middleman documentation)