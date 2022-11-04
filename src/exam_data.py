"""
exam_data.py

This module contains classes for manipulating exam data as a part of an analysis
on the use of artistic representations in organic chemistry problems.

Classes:
-------
Response(id):
    Contains all data and metadata surrounding a given reponse to a question
    from one of several organic chemistry exams.

    Attributes include:
    exam, q_number, exam_id, correct, drawing (and types of drawing),
    redrawing (and types of redrawing)

Question(id):
    Contains all data and metadata surrounding a given question from one of
    several organic chemistry exams.

    Attributes include:
    exam, q_number, type, drawing (and types of drawings), responses_list, 
    number_responses, fraction_correct, fraction_with_drawing, 
    fraction_with_redrawing

"""
import pandas as pd

class Response:
    """
    This class contains all data and metadata surrounding a given response
    to a question from one of several organic chemistry exams.

    The attributes of each Response object include:

    exam, q_number, exam_id, correct, drawing (and types of drawing),
    redrawing (and types of redrawing)

    """
    def __init__(self, r_id, responses_file_path):
        """Initialize Response object and link the related data

        Parameters
        ----------
        r_id : int
            Response ID found in the first column of the response_config.csv
            file
        responses_file_path : str
            Contains the path to the response_config.csv file
        """
        # Get response data
        response_config = pd.read_csv(
            responses_file_path,
            index_col=0
            )
        response_data = response_config.iloc[r_id]

        response_attrs = response_config.columns
        for attr in response_attrs:
            setattr(self, attr, response_data[attr])

        # Ensure that "drawing", and "redrawing" columns exist in the 
        # response_config file
        assert "drawing" in response_attrs, \
            "'drawing' must be an entry in response_config"
        assert "redrawing" in response_attrs, \
            "'redrawing' must be an entry in response_config"

class Question:
    """
    This class contains all data and metadata surrounding a given question
    from one of several organic chemistry exams.

    The attributes of each Question object include:

    exam, q_number, type, drawing (and types of drawings), responses_list, 
    number_responses, fraction_correct, fraction_with_drawing, 
    fraction_with_redrawing

    """
    def __init__(self, q_id, questions_file_path, responses_file_path):
        """Initialize Question object and link the related data

        Parameters
        ----------
        q_id : int
            Question ID found in the first column of the question_config.csv
            file
        questions_file_path : str
            Contains the path to the question_config.csv file
        responses_file_path : str
            Contains the path to the response_config.csv file
        """
        # Get question data
        question_config = pd.read_csv(
            questions_file_path,
            index_col=0
            )
        question_data = question_config.iloc[q_id]

        for attr in question_config.columns:
            setattr(self, attr, question_data[attr])

        # Get corresponding responses data
        response_config = pd.read_csv(
            responses_file_path,
            index_col=0
            )

        question_attrs = question_config.columns
        response_attrs = response_config.columns

        # Ensure that "exam" and "q_number" columns exist in the 
        # question_config and response_config files
        assert "exam" in question_attrs and "exam" in response_attrs, \
            "'exam' must be an entry in both question_config and response_config"
        assert "q_number" in question_attrs and "q_number" in response_attrs, \
            "'q_number' must be an entry in both question_config and response_config"

        # Gather list of responses for the desired question
        response_filter = list(response_config["exam"] == question_data["exam"]) and \
           list(response_config["q_number"] == question_data["q_number"])
        response_data = response_config[response_filter]

        responses_list = []
        for r_id in response_data.index:
            responses_list.append(Response(r_id, responses_file_path))

        self.responses_list = responses_list

        # Perform data summary calculations
        num_responses = len(responses_list)
        num_drawings = 0
        num_redrawings = 0
        for response_object in responses_list:
            if response_object.drawing:
                num_drawings += 1
            if response_object.redrawing:
                num_redrawings += 1

        self.number_responses = num_responses
        self.fraction_with_drawing = num_drawings / num_responses
        self.fraction_with_redrawing = num_redrawings / num_responses
