from flask import Flask, request, jsonify
import gzip
from numpy import median


''' Anagrams API
    Author: Adam Hicks
    Date: 11-14-2016

    There are several endpoints in this api:
        -/word.json
            supports POST which takes a json array named 'words' and adds them
            to the dictionary/corpus

            supports DELETE which completely dumps the dictionary/corpus

            supports GET which returns a json dictionary of statistics for the
            dictionary/corpus including size/min/max/median/average

        -/anagrams/<word>.json
            supports DELETE which deletes all anagrams of the supplied word in
            the url.  Optional query params ignorecase=yes deletes proper nouns.

            supports GET which returns json array of all anagrams for the
            supplied word in the url.  Optional query params ignorecase=yes
            will return proper nouns as well.  Optional query params limit=x
            where x is an integer will limit the results to the number specified.


        -/words/<word>.json
            supports DELETE which deletes just the word supplied in the url.

            supports GET as a maintenance verification utility which returns
            either True or False regarding word's existence in the dictionary/
            corpus.

'''


#: Initiate the app with config
app = Flask(__name__)
app.config.from_object(__name__)


#: This is our database - an inmemory set from the compressed file
f = gzip.open('dictionary.txt.gz', 'rb')
file_content = f.read()
dictionary_words = []

for word in file_content.split('\n'):
    dictionary_words.append(word)

dictionary_words = filter(None, dictionary_words)

# test
@app.endpoint('words.json')
@app.route('/words.json', methods=['POST', 'DELETE', 'GET'])
def bouncer():
    global dictionary_words
    if request.method == 'POST':
        input_words = request.get_json(force=True)
        for in_word in input_words['words']:
            if in_word not in dictionary_words:
                dictionary_words.append(in_word)
        return '', 201

    elif request.method == 'DELETE':
        dictionary_words = []
        return '', 204

    elif request.method == 'GET':
        size = len(dictionary_words)
        smallest = min(dictionary_words, key=len)
        size_of = len(smallest)
        biggest = max(dictionary_words, key=len)
        size_of_biggest = len(biggest)
        length_list = [(x, len(x))[1] for x in dictionary_words]
        middle_size = median(length_list)
        average = reduce(lambda x, y: x + y, length_list) / len(length_list)
        counts = {
            'word count': size,
            'min': smallest,
            'size of min': size_of,
            'max': biggest,
            'size of max': size_of_biggest,
            'median': middle_size,
            'average': average
        }
        return jsonify({"counts": counts}), 200


@app.route('/anagrams/<word>', methods=['GET', 'DELETE'])
def gramanas(word):
    global dictionary_words
    if request.method == 'DELETE':
        real_word = word.split('.')[0]
        lower_case = request.args.get('ignorecase')
        deletes = []
        for dict_word in dictionary_words:
            if str(lower_case) == 'yes':
                if sorted(dict_word.lower()) == sorted(real_word.lower()):
                    deletes.append(dict_word)
            else:
                if sorted(dict_word) == sorted(real_word):
                    deletes.append(dict_word)
        for i in deletes:
            dictionary_words.remove(i)
        return '', 204

    else:
        how_many = request.args.get('limit')
        lower_case = request.args.get('ignorecase')
        real_word = word.split('.')[0]
        anagrams = []
        for dict_word in dictionary_words:
            if str(lower_case) == 'yes':
                if sorted(dict_word.lower()) == sorted(real_word.lower()):
                    anagrams.append(dict_word)
            else:
                if sorted(dict_word) == sorted(real_word):
                    anagrams.append(dict_word)
        if real_word in anagrams:
            anagrams.remove(real_word)
        if how_many is not None:
            anagrams = anagrams[0:int(how_many)]
        return jsonify({'anagrams': anagrams}), 200


@app.route('/words/<word>', methods=['DELETE', 'GET'])
def deleteOne(word):
    global dictionary_words
    if request.method == 'DELETE':
        real_word = word.split('.')[0]
        dictionary_words.remove(real_word)
        return '', 200

    elif request.method == 'GET':
        if word.split('.')[0] in dictionary_words:
            result = "True"
        else:
            result = "False"
        return jsonify(result), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
