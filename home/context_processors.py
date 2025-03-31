from datetime import datetime
"""
Context processors for handle current year in the copyright block.
I used Chat-GPT.
"""


def current_year(request):
    return {
        'current_year': datetime.now().year,
    }
