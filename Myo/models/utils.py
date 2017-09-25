from sklearn.model_selection import RandomizedSearchCV, GridSearchCV


def get_parameters(parameter_search_space, classifier, x_train, y_train):
    try:
        randomised = RandomizedSearchCV(classifier, parameter_search_space)
        return randomised.fit(x_train, y_train), 'RandomizedSearchCV'

    except ValueError:
        grid = GridSearchCV(classifier, parameter_search_space)
        return grid.fit(x_train, y_train), 'GridSearchCV'
