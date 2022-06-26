## <span style="color:blue">Bible verses from any language </span>
---
jw.org has translated the bible in several languages. 
For some of these languages it is the most consistent source of text freely available on the internet.
This project scrapes all bible verses of any language from their website.

You can download text from 2 different languages, create sentence pairs (from verses numbering) and build a translation algorithm.

Of course  you can perform other NLP tasks like masked language modeling.

### <span style="color:blue">**Usage**</span>
---

#### <span style="color:blue">*- Command Line*</span>
To collect the text you must first identify the page of your desired language.

go to the english page https://www.jw.org/en/library/bible/bi12/books
change the language and select your target language. Then grab the link on the browser.

use the command:

ex:
```
python get_verses.py --lang-url=/en/library/bible/bi12/books --save-dir=./ 
```
This will download and organize the english texts entirely.


```
python get_verses.py --lang-url=/en/library/bible/bi12/books --save-dir=./ --min-chapter-num=40
```
This will download and organize the english texts starting from chapter 40, i.e the so called new testament.

You can handle parallel jobs using argument *--n-jobs*.

* Note: This is not a recommendation to read or believe what's in the text. Everyone is free to do what they want. This is just to extract the value from an NLP world perspective.*

