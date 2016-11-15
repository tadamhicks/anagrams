# anagrams
REST API for dictionary interaction.  This guide assumes you are using a mac or linux and are running Docker.

## download
```
$ git clone https://github.com/tadamhicks/anagrams.git
```

## build
You need to be in the directory where the code is, so
```
$ cd anagrams
```

Then you can build with
```
$ docker build -t anagrams .
```

## run
Running will expose the API on the localhost listening on port 3000.

```
docker run -p 3000:3000 anagrams
```

## what's inside
There are several endpoints in this api:

#### /word.json
Supports POST which takes a json array named 'words' and adds them to the dictionary/corpus.

Supports DELETE which completely dumps the dictionary/corpus.

Supports GET which returns a json dictionary of statistics for the dictionary/corpus including size/min/max/median/average.

#### /anagrams/<word>.json
Supports DELETE which deletes all anagrams of the supplied word in the url.  Optional query param ignorecase=yes deletes proper nouns.

Supports GET which returns json array of all anagrams for the supplied word in the url.  Optional query param ignorecase=yes will return proper nouns as well.  Optional query param limit=x where x is an integer will limit the results to the number specified.

#### /words/<word>.json
Supports DELETE which deletes just the word supplied in the url.

Supports GET as a maintenance verification utility which returns either True or False regarding word's existence in the dictionary/ corpus.

## technical stuff about the backend
There are some assumptions that are made regarding the dictionary.  For instance, I assume that having an empty character in the dictionary is superluous, so I remove it at runtime.  All calculations like word count, median, average and especially the minimum reflect this.

A set is used for the dictionary, so adding a word that already exists in the dictionary/corpus will not add additional content.

There is tons of room for improvement in this small api.
