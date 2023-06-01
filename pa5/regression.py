'''
Linear regression

YOUR NAME HERE

Main file for linear regression and model selection.
'''

import numpy as np
from sklearn.model_selection import train_test_split
import util


class DataSet(object):
    '''
    Class for representing a data set.
    '''

    def __init__(self, dir_path):
        '''
        Constructor
        Inputs:
            dir_path: (string) path to the directory that contains the
              file
        '''

        self.column_labels, self.data = util.load_numpy_array(dir_path, "data.csv")
        self.parameters = util.load_json_file(dir_path, "parameters.json")
        self.dataset_name = self.parameters["name"]
        self.predictor_vars = self.parameters["predictor_vars"]
        self.dependent_var = self.parameters["dependent_var"]
        self.training_data, self.testing_data = train_test_split(self.data, 
            test_size = None, train_size = self.parameters["training_fraction"],
            random_state = self.parameters["seed"])


class Model(object):
    '''
    Class for representing a model.
    '''

    def __init__(self, dataset, pred_vars):
        '''
        Construct a data structure to hold the model.
        Inputs:
            dataset: an dataset instance
            pred_vars: a list of the indices for the columns (of the
              original data array) used in the model.
        '''
        self.col_labels = dataset.column_labels
        self.pred_vars = pred_vars
        self.dep_var = dataset.dependent_var

        self.x_array = util.prepend_ones_column(dataset.training_data[:, 
            self.pred_vars])
        self.y_array = dataset.training_data[:, self.dep_var]
        self.beta = util.linear_regression(self.x_array, self.y_array)
        self.yhat_array = util.apply_beta(self.beta, self.x_array)

        #R2 and adj_R2 values are from training data only
        self.R2 = 1 - sum(np.square(self.y_array - self.yhat_array)) / sum(
            np.square(self.y_array - np.mean(self.y_array)))
        N = len(dataset.training_data)
        K = len(pred_vars)
        self.adj_R2 = self.R2 - (1 - self.R2) * K / (N - K - 1)
       

    def __repr__(self):
        '''
        Format model as a string.
        '''
        out_str = ""
        for var in self.pred_vars:
            out_str += " + {:.6f} * {}".format(self.beta[var + 1], 
                self.col_labels[var])

        return "{} ~ {} + {}".format(self.dep_var, self.beta[0], out_str), 
        "R2: {}".format(self.R2)

    def test_R2(self, dataset):
        '''
        Calculates the R2 value from applying the training data regression model
        to a new dataset.
        Inputs:
            dataset: must be an ARRAY
        '''
        self.x = util.prepend_ones_column(dataset[:, self.pred_vars])
        self.y = dataset[:, self.dep_var]
        self.yhat_array = util.apply_beta(self.beta, self.x)
        self.test_R2 = 1 - sum(np.square(self.y - self.yhat_array)) / sum(
            np.square(self.y - np.mean(self.y)))

        return self.test_R2


def compute_single_var_models(dataset):
    '''
    Computes all the single-variable models for a dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        List of Model objects, each representing a single-variable model
    '''
    rv = []
    for var in dataset.predictor_vars:
        var = [var]
        rv.append(Model(dataset, var))
    return rv


def compute_all_vars_model(dataset):
    '''
    Computes a model that uses all the predictor variables in the dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object that uses all the predictor variables
    '''

    return Model(dataset, dataset.predictor_vars)


def compute_best_pair(dataset):
    '''
    Find the bivariate model with the best R2 value

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object for the best bivariate model
    '''

    rv = Model(dataset, [1, 2])

    for i, var in enumerate(dataset.predictor_vars):
        while i + 1 < len(dataset.predictor_vars):
            var2 = dataset.predictor_vars[i + 1]
            if Model(dataset, [var, var2]).R2 > rv.R2:
                rv = Model(dataset, [var, var2])
            i += 1

    return rv


def backward_elimination(dataset):
    '''
    Given a dataset with P predictor variables, uses backward elimination to
    select models for every value of K between 1 and P.

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A list (of length P) of Model objects. The first element is the
        model where K=1, the second element is the model where K=2, and so on.
    '''

    rv = []

    rv.append(Model(dataset, dataset.predictor_vars))

    while len(rv[-1].pred_vars) > 1:
        best_R2 = 0
        for i, var in enumerate(dataset.predictor_vars):
            popped_pred_vars = dataset.predictor_vars[:i] + \
            dataset.predictor_vars[i+1:]
            if Model(dataset, popped_pred_vars).R2 > best_R2:
                best_model = Model(dataset, popped_pred_vars)
                best_R2 = Model(dataset, popped_pred_vars).R2
        rv.append(best_model)
        dataset.predictor_vars = best_model.pred_vars

    return rv



def choose_best_model(dataset):
    '''
    Given a dataset, choose the best model produced
    by backwards elimination (i.e., the model with the highest
    adjusted R2)

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object
    '''

    model_list = backward_elimination(dataset)
    best_adj_R2 = 0

    for model in model_list:
        if model.adj_R2 > best_adj_R2:
            best_model = model
            best_adj_R2 = model.adj_R2
    
    return best_model


def validate_model(dataset, model):
    '''
    Given a dataset and a model trained on the training data,
    compute the R2 of applying that model to the testing data.

    Inputs:
        dataset: (DataSet object) a dataset
        model: (Model object) A model that must have been trained
           on the dataset's training data.

    Returns:
        (float) An R2 value
    '''

    return model.test_R2(dataset.testing_data)
