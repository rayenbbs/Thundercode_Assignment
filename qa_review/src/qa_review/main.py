#!/usr/bin/env python
import sys
import warnings

from qa_review.crew import QaReview

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

#these are functions for 

def run():
    """
    Run the crew.
    """
    inputs = {"website_url": "https://www.jeinsat.com/","topic":"Quality Assurance"
    }
    QaReview().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "Quality Assurance "
    }
    try:
        QaReview().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        QaReview().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "Quality Assurance"
    }
    try:
        QaReview().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
