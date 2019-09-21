from Entities.analysis_data import AnalysisData
from Entities.discussion import Discussion


# TODO: implement reading discussion from file
def get_discussion(id=0):
    return Discussion()


# TODO: understand how to analyze data
def analyze_discussion(discussion, comment):
    return AnalysisData(0, comment)


def add_comment(discussion, comment):
    discussion.add_comment(comment)
    analysis_data = analyze_discussion(discussion, comment)
    return analysis_data
