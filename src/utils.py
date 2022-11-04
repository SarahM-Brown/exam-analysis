"""
utils.py

get_q_objs_from_q_ids(q_id_list, q_file_path, r_file_path):
    Get question objects, given a list of question ids

"""

from src.exam_data import Question

def get_q_objs_from_q_ids(q_id_list, q_file_path, r_file_path):
    """Get question objects, given a list of question ids.

    Parameters
    ----------
    q_id_list : list of ints
        
    q_file_path : str
        Contains the path to the question_config.csv file
    r_file_path : str
        Contains the path to the response_config.csv file

    Returns
    -------
    list of Question objects
        Contains the Question objects corresponding to the input question ids
    """
    q_objs = []
    for q_id in q_id_list:
        q_obj = Question(q_id, q_file_path, r_file_path)
        q_objs.append(q_obj)

    return q_objs