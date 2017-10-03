import numpy as np
import itertools
from random import shuffle

def compile_datafiles(data_range):
    X0_list = list([])
    X1_list = list([])

    for i, j in itertools.product(range(data_range[0]), range(data_range[1])):
        file = str(i) + str(j)
        X0_file = 'classified_arrays/'+file+'_X0.npy'
        X1_file = 'classified_arrays/'+file+'_X1.npy'

        X0_list.append(np.load(X0_file))
        X1_list.append(np.load(X1_file))

    X0 = np.concatenate(X0_list, axis=0)
    X1 = np.concatenate(X1_list, axis=0)

    return (X0, X1)

def split_data(X, test_size=0.25, do_shuffle=True):
    n_samples = X.shape[0]
    index = [i for i in range(n_samples)]
    if do_shuffle:
        shuffle(index)
    split_at = int(round(n_samples*test_size))
    test_index = index[:split_at]
    train_index = index[split_at:]

    X_test = X[test_index]
    X_train = X[train_index]

    return X_train, X_test

def join_data(X0, X1):
    Y0 = np.zeros((X0.shape[0],1))
    Y1 = np.ones((X1.shape[0],1))

    X = np.concatenate((X0,X1), axis=0)
    Y = np.concatenate((Y0,Y1), axis=0)

    return X, Y

def save_data(X_train, X_test, Y_train, Y_test):
    np.save('data/X_train.npy', X_train)
    np.save('data/X_test.npy', X_test)
    np.save('data/Y_train.npy', Y_train)
    np.save('data/Y_test.npy', Y_test)

def main():
    (X0, X1) = compile_datafiles((10,10))

    X1_train, X1_test = split_data(X1, test_size=0.2, do_shuffle=True)
    X0_train, X0_test = split_data(X0, test_size=0.2, do_shuffle=True)

    X_train, Y_train = join_data(X0=X0_train, X1=X1_train)
    X_test, Y_test = join_data(X0=X0_test, X1=X1_test)

    save_data(X_train, X_test, Y_train, Y_test)

if __name__ == "__main__":
    # execute only if run as a script
    main()