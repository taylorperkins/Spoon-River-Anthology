from collections import Counter

from pprint import pprint

from nltk import word_tokenize, pos_tag

from utils import read_cleaned_text


class ProNounTagging:
    def __init__(self, poem_dir):
        self._poem_dir = poem_dir

    @staticmethod
    def tag_pro_nouns(tokens):
        proper_nouns = list()

        tags = pos_tag(tokens)

        i = 0
        while i < len(tags):
            if tags[i][1] == 'NNP':
                if tags[i + 1][1] == 'NNP':
                    proper_nouns.append(' '.join([
                        tags[i][0].lower(), tags[i + 1][0].lower()
                    ]))
                    i += 1

                else:
                    proper_nouns.append(tags[i][0].lower())
            i += 1

        return proper_nouns

    @staticmethod
    def summarize_text(proper_nouns, top_num=100):
        return dict(Counter(proper_nouns).most_common(top_num))

    def main(self):
        poems = read_cleaned_text(self._poem_dir)

        characters_set = list()
        for poem in poems:
            tokenized = word_tokenize(' '.join(poem))
            pos_tagged = self.tag_pro_nouns(tokenized)

            characters_set.extend(pos_tagged)

        summarized = self.summarize_text(characters_set)
        pprint(summarized)


if __name__ == '__main__':
    pro_nouns = ProNounTagging(poem_dir="../data/poems/")

    pro_nouns.main()



