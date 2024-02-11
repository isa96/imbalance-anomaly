import errno
import os
import pickle
import random
import shutil
import sys
from math import floor


class Split(object):
    def __init__(self, dataset):
        self.dataset = dataset
        self.random_seed = 101
        self.train_size = 0.7

    @staticmethod
    def __check_path(path):
        # check a path is exist or not. if not exist, then create it
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def __set_datapath(self):
        # set data path for output files
        current_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'datasets', self.dataset))
        train_test_path = os.path.join(current_path, 'train-test')

        # remove output directory
        if os.path.isdir(train_test_path):
            shutil.rmtree(train_test_path)

        self.__check_path(train_test_path)

        self.groundtruth_file = os.path.join(current_path, 'auth.all.pickle')
        self.train_file = os.path.join(train_test_path, self.dataset + '.train.pickle')
        self.test_file = os.path.join(train_test_path, self.dataset + '.test.pickle')

    def __save_groundtruth(self, train_data, test_data):
        # save train data
        with open(self.train_file, 'wb') as handle:
            pickle.dump(train_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # save test data
        with open(self.test_file, 'wb') as handle:
            pickle.dump(test_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def split(self):
        # get path
        self.__set_datapath()

        # groundtruth is a dictionary. key: line id, value: message, label
        with open(self.groundtruth_file, 'rb') as f_pickle:
            groundtruth = pickle.load(f_pickle)

        # check normal and anomaly
        normal = []
        anomaly = []
        for line_id, element in groundtruth.items():
            if element['label'] == 1:
                normal.append(line_id)
            elif element['label'] == 0:
                anomaly.append(line_id)

        # initialize train and test
        train_data = []
        test_data = []

        # random sequence for normal
        list_len = len(normal)
        random.Random(self.random_seed).shuffle(normal)

        train_length = floor(self.train_size * list_len)
        for index in normal[:train_length]:
            train_data.append(groundtruth[index])

        for index in normal[train_length:]:
            test_data.append(groundtruth[index])

        # random sequence for anomaly
        negative_len = len(anomaly)
        if negative_len > 0:
            random.Random(self.random_seed).shuffle(anomaly)

            train_length = floor(self.train_size * negative_len)
            for index in anomaly[:train_length]:
                train_data.append(groundtruth[index])

            for index in anomaly[train_length:]:
                test_data.append(groundtruth[index])

        self.__save_groundtruth(train_data, test_data)


if __name__ == '__main__':
    dataset_list = ['dfrws-2009', 'hofstede', 'secrepo']
    if len(sys.argv) < 2:
        print('Please input dataset name.')
        print('python split.py dataset_name ')
        print('Supported datasets:', dataset_list)
        sys.exit(1)

    else:
        dataset_name = sys.argv[1]
        s = Split(dataset_name)
        s.split()
