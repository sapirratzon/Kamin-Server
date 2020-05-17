class SentimentAnalyzer:
    def __init__(self):
        self.he_positive_words = set()
        self.he_negative_words = set()
        with open("negative_words_he.txt", encoding='utf-8') as nw_file:
            lines = nw_file.readlines()
            for line in lines:
                word = line.replace('\n', '')
                self.he_negative_words.add(word)
        with open("positive_words_he.txt", encoding='utf-8') as nw_file:
            lines = nw_file.readlines()
            for line in lines:
                word = line.replace('\n', '')
                self.he_positive_words.add(word)

    def simple_analysis(self, text, language="Hebrew"):
        positive_words = None
        negative_words = None
        if language == "Hebrew":
            positive_words = self.he_positive_words
            negative_words = self.he_negative_words
        else:
            # TODO: for now we have just hebrew - when adding english need to add lists of english sentiment words
            positive_words = self.he_positive_words
            negative_words = self.he_negative_words
        grade = 0
        for word in positive_words:
            if word in text:
                grade += 1
        for word in negative_words:
            if word in text:
                grade -= 1

        if grade > 0:
            return "positive"
        elif grade < 0:
            return "negative"
        else:
            return "neutral"


# analyzer = SentimentAnalyzer()
# print(analyzer.simple_analysis("זה טוב", "Hebrew"))
# print(analyzer.simple_analysis("זה רע", "Hebrew"))
