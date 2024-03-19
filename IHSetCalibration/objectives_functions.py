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
    like2 = 1 - mielke_skill_score(evaluation, simulation)

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
    like2 = 1 - mielke_skill_score(evaluation, simulation)

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
    like2 = 1 - mielke_skill_score(evaluation, simulation)

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
    like = 1 - mielke_skill_score(evaluation, simulation)

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

def mielke_skill_score(evaluation, simulation):
    """ Mielke index 
    if pearson coefficient (r) is zero or positive use kappa=0
    otherwise see Duveiller et al. 2015
    """
    x = evaluation
    y = simulation
    mx = np.mean(x)
    my = np.mean(y)
    xm, ym = x-mx, y-my

    diff= (evaluation - simulation) ** 2 
    d1= np.sum(diff)
    d2= np.var(evaluation)+np.var(simulation)+ (np.mean(evaluation)-np.mean(simulation))**2
    
    if correlation_coefficient_loss(evaluation, simulation) < 0:
        kappa = np.abs( np.sum(xm*ym)) * 2
        mss= 1-(  ( d1* (1/len(evaluation))  ) / (d2 +kappa))
    else:
        mss= 1-(  ( d1* (1/len(evaluation))  ) / d2 )

    return mss

def correlation_coefficient_loss(evaluation, simulation):
    x = evaluation
    y = simulation
    mx = np.mean(x)
    my = np.mean(y)
    xm, ym = x-mx, y-my
    r_num = np.sum(xm*ym)
    r_den = np.sqrt(np.sum(np.square(xm)) * np.sum(np.square(ym)))
    r = r_num / r_den
    r = np.maximum(np.minimum(r, 1.0), -1.0)

    return 1- np.square(r)

 