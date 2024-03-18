import spotpy as spt
import numpy as np

class objective_functions(object):

    def __init__(self, method, metrics, **kwargs):
        
        self.method = method
        self.metrics = metrics
        if method == 'NSGAII':
            self.n_obj = kwargs['n_obj']
            self.n_pop = kwargs['n_pop']
            self.generations = kwargs['generations']
            if self.metrics == 'rmse_rp':
                self.obj_func = multi_obj_func_rmse_rp
            elif self.metrics == 'mss_rmse':
                self.obj_func = multi_obj_func_mss_rmse
            elif self.metrics == 'mss_rp':
                self.obj_func = multi_obj_func_mss_rp
            elif self.metrics == 'mss_nsse':
                self.obj_func = multi_obj_func_mss_nsse
            elif self.metrics == 'rp_nsse':
                self.obj_func = multi_obj_func_rp_nsse
            elif self.metrics == 'rmse_nsse':
                self.obj_func = multi_obj_func_rmse_nsse
        else:
            self.repetitions = kwargs['repetitions']
            if self.metrics == 'mss':
                self.obj_func = obj_func_mss
            elif self.metrics == 'rmse':
                self.obj_func = obj_func_rmse
            elif self.metrics == 'rp':
                self.obj_func = obj_func_rp
            elif self.metrics == 'nsse':
                self.obj_func = obj_func_nsse

def multi_obj_func_rmse_rp(evaluation, simulation):
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
    like1 = spt.objectivefunctions.rmse(evaluation, simulation)/5
    like2 = spt.objectivefunctions.rsquared(evaluation, simulation) * -1
    return [ like1, like2]

def multi_obj_func_mss_rmse(evaluation, simulation):
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
    like1 = spt.objectivefunctions.rmse(evaluation, simulation)/5
    like2 = np.sum((simulation - evaluation)**2)/len(simulation)/(np.var(simulation)+np.var(evaluation)+(np.mean(simulation)-np.mean(evaluation))**2)

    return [like1, like2]

def multi_obj_func_mss_rp(evaluation, simulation):
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

    like1 = spt.objectivefunctions.rsquared(evaluation, simulation) * -1
    like2 = np.sum((simulation - evaluation)**2)/len(simulation)/(np.var(simulation)+np.var(evaluation)+(np.mean(simulation)-np.mean(evaluation))**2)

    return [like1, like2]

def multi_obj_func_mss_nsse(evaluation, simulation):
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
    like1 = 1 - spt.objectivefunctions.nashsutcliffe(evaluation, simulation)
    like2 = np.sum((simulation - evaluation)**2)/len(simulation)/(np.var(simulation)+np.var(evaluation)+(np.mean(simulation)-np.mean(evaluation))**2)

    return [like1, like2]

def multi_obj_func_rp_nsse(evaluation, simulation):
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
    like1 = spt.objectivefunctions.rsquared(evaluation, simulation) * -1
    like2 = 1 - spt.objectivefunctions.nashsutcliffe(evaluation, simulation)

    return [like1, like2]

def multi_obj_func_rmse_nsse(evaluation, simulation):
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
    like1 = spt.objectivefunctions.rmse(evaluation, simulation)/5
    like2 = 1 - spt.objectivefunctions.nashsutcliffe(evaluation, simulation)

    return [like1, like2]

def obj_func_mss(evaluation, simulation):
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
    like = np.sum((simulation - evaluation)**2)/len(simulation)/(np.var(simulation)+np.var(evaluation)+(np.mean(simulation)-np.mean(evaluation))**2)
    return [like]

def obj_func_rmse(evaluation, simulation):
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
    like = spt.objectivefunctions.rmse(evaluation, simulation)/5
    return [like]

def obj_func_rp(evaluation, simulation):
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
    like = spt.objectivefunctions.rsquared(evaluation, simulation) * -1
    return [like]

def obj_func_nsse(evaluation, simulation):
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
    like = 1 - spt.objectivefunctions.nashsutcliffe(evaluation, simulation)
    return [like]
