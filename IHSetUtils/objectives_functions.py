import spotpy
import numpy as np


def multi_obj_func(evaluation, simulation):
    """
    Parameters
    ----------
    evaluation : array
        The observation data.
    simulation : array
        The model input

    Returns
    -------
    list
        Three different kinds of objective functions.

    """
    like1 = np.abs(spotpy.objectivefunctions.pbias(evaluation, simulation))
    like2 = spotpy.objectivefunctions.rmse(evaluation, simulation)
    like3 = spotpy.objectivefunctions.rsquared(evaluation, simulation) * -1
    return [like1, like2, like3]