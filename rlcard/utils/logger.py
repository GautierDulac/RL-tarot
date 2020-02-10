import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class Logger(object):
    """
    Logger saves the running results and helps make plots from the results
    """

    def __init__(self, xlabel: str = '', ylabel: str = '', zlabel: str = None, label_list: List[str] = None,
                 legend: str = '', legend_hist: str = '',
                 log_path: str = None,
                 csv_path: str = None):
        """
        Initialize the labels, legend and paths of the plot and log file.
        :param xlabel: (string): label of x axis of the plot
        :param ylabel: (string): label of y axis of the plot
        :param zlabel: (string): if provided, create a third column in the csv record
        :param label_list: (List[str]): if provided, erase x,y,z labels and used as multi columns input
        :param legend: (string): name of the curve
        :param log_path: (string): where to store the log file
        :param csv_path: (string): where to store the csv file
        1. log_path must be provided to use the log() method. If the log file already exists, it will be deleted when Logger is initialized.
        2. If csv_path is provided, then one record will be write to the file everytime add_point() method is called.
        """
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.zlabel = zlabel
        self.label_list = label_list
        self.legend = legend
        self.legend_hist = legend_hist
        self.xs = []
        self.ys = []
        self.zs = []
        self.log_path = log_path
        self.csv_path = csv_path
        self.log_file = None
        self.csv_file = None
        if log_path is not None:
            log_dir = os.path.dirname(log_path)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            self.log_file = open(log_path, 'w')
        if csv_path is not None:
            csv_dir = os.path.dirname(csv_path)
            if not os.path.exists(csv_dir):
                os.makedirs(csv_dir)
            self.csv_file = open(csv_path, 'w')
            if label_list is not None:
                first_line = ''
                for name in label_list[:-1]:
                    first_line = first_line + name + ','
                first_line = first_line + label_list[-1] + '\n'
                self.csv_file.write(first_line)
            else:
                if zlabel is not None:
                    self.csv_file.write(xlabel + ',' + ylabel + ',' + zlabel + '\n')
                else:
                    self.csv_file.write(xlabel + ',' + ylabel + '\n')
            self.csv_file.flush()

    def log(self, text: str) -> None:
        """
        Write the text to log file then print it.
        :param text: text(string): text to log
        :return: None
        """
        self.log_file.write(text + '\n')
        self.log_file.flush()
        print(text)

    def add_point(self, x=None, y=None, z=None, write_list=None) -> None:
        """
        Add a point to the plot
        :param write_list: list of coordinate to save when multiples
        :param x: x coordinate value
        :param y: y coordinate value
        :param z: z coordinate value if given
        :return:
        """
        if write_list is not None:
            if len(write_list) != len(self.label_list):
                raise ValueError('List of parameters to add should be the same length as the label list')
            else:
                line = ''
                for value in write_list[:-1]:
                    line = line + str(value) + ','
                line = line + str(write_list[-1]) + '\n'
        else:
            if x is not None and y is not None:
                self.xs.append(x)
                self.ys.append(y)
                if z is not None:
                    self.zs.append(z)
                    line = str(x) + ',' + str(y) + ',' + str(z) + '\n'
                else:
                    line = str(x) + ',' + str(y) + '\n'
            else:
                raise ValueError('x and y should not be None.')

        # If csv_path is not None then write x and y to file
        if self.csv_path is not None:
            self.csv_file.write(line)
            self.csv_file.flush()

    def make_plot(self, save_path: str = '') -> None:
        """
        Make plot using all stored points
        :param save_path: (string): where to store the plot
        :return:
        """
        fig, ax = plt.subplots()
        ax.plot(self.xs, self.ys, label=self.legend)
        ax.set(xlabel=self.xlabel, ylabel=self.ylabel)
        ax.legend()
        ax.grid()

        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        fig.savefig(save_path)
        fig.clf()

    def make_plot_hist(self, save_path_1: str = '', save_path_2: str = '', reward_list=List[int]) -> None:
        """
        Make plot using last reward list
        :param save_path_1: (string): where to save the hist
        :param save_path_2: (string): where to save the density
        :param reward_list: (list of int): list of last rewards during the evaluation round
        :return:
        """
        fig, ax = plt.subplots()
        min_bin = np.min(np.array(reward_list))
        max_bin = np.max(np.array(reward_list))
        ax.hist(reward_list, label=self.legend_hist, bins=np.linspace(min_bin, max_bin, max_bin - min_bin + 1))
        plt.xlim((-24, 24))
        plt.ylim((0, int(len(reward_list) * 0.3)))
        ax.set(xlabel='Points won', ylabel='Frenquency')
        ax.legend()
        ax.grid()

        save_dir = os.path.dirname(save_path_1)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        fig.savefig(save_path_1)
        fig.clf()

        sns.set_style('whitegrid')
        ax = sns.kdeplot(reward_list, label=self.legend_hist, bw=0.5)
        plt.xlim((-24, 24))
        plt.ylim((0, 0.3))
        ax.set(xlabel='Points won', ylabel='Frenquency')
        ax.legend()
        ax.grid()

        save_dir = os.path.dirname(save_path_2)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        plt.savefig(save_path_2)
        plt.clf()

    def close_file(self) -> None:
        """
        Close the created file objects
        :return: None
        """
        if self.log_path is not None:
            self.log_file.close()
        if self.csv_path is not None:
            self.csv_file.close()
