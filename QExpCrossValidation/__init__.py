'''
cross validation for query expansion.
unsupervised methods:
    K folds. K-1 selected best parameter, test on left 1
supervised methods:
    K folds.
        K-1: a K-1 folds train/test, given a parameter set, train on K-2, test on left 1, record best
            choose best on in K-1
        1: train model with best parameter in the K-1 fold, and test on 1
'''


'''
current methods:
    Unsupervised:
        IndriExp (3/9/2014). para: # of prf documents, DirMu, # of feedback terms, original query weight 


'''




'''
General Design. put together the common part.
A Parameter set class (in GeekTools.CV package):
    read conf and general list of parameters, (combination of parameters)
    stored in a {parameter name:value}
a general pipeline class:
    read parameter file, general parameter sets
    process (unsupervised now):
        K-folding:
            train:
                a class (UnsupervisedExpPipeline) that call expansion, re-ranking, and evaluation
                call the class for each parameter set, record the best one.
            test:
                call UnsupervisedExpPipeline for evaluation performance.
    output final per query performance                                        
'''