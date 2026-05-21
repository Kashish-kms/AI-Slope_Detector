import re
from collections import Counter
import textstat

class SlopMetrics:
    @staticmethod
    def calculate_repetition(text):
        words = re.findall(r'\w+', text.lower())
        if not words: return 0
        word_counts = Counter(words)
        duplicates = sum(1 for count in word_counts.values() if count > 1)
        return (duplicates / len(words)) * 100

    @staticmethod
    def get_readability_scores(text):
        return {
            "flesch_reading_ease": textstat.flesch_reading_ease(text),
            "lexicon_count": textstat.lexicon_count(text),
            "sentence_count": textstat.sentence_count(text)
        }

    @staticmethod
    def keyword_stuffing_score(text):
        # High density of specific keywords often indicates SEO slop
        words = re.findall(r'\w+', text.lower())
        if len(words) < 10: return 0
        counts = Counter(words).most_common(5)
        max_density = (counts[0][1] / len(words)) * 100
        return max_density # Values > 5% usually indicate stuffing