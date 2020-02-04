import os

import matplotlib.pyplot as plt


class Logger(object):
    """
    Logger saves the running results and helps make plots from the results
    """

    def __init__(self, xlabel: str = '', ylabel: str = '', zlabel: str = None, legend: str = '', log_path: str = None,
                 csv_path: str = None):
        """
        Initialize the labels, legend and paths of the plot and log file.
        :param xlabel: (string): label of x axis of the plot
        :param ylabel: (string): label of y axis of the plot
        :param zlabel: (string): if provided, create a third column in the csv record
        :param legend: (string): name of the curve
        :param log_path: (string): where to store the log file
        :param csv_path: (string): where to store the csv file
        1. log_path must be provided to use the log() method. If the log file already exists, it will be deleted when Logger is initialized.
        2. If csv_path is provided, then one record will be write to the file everytime add_point() method is called.
        """
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.zlabel = zlabel
        self.legend = legend
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

    def add_point(self, x=None, y=None, z=None) -> None:
        """
        Add a point to the plot
        :param x: x coordinate value
        :param y: y coordinate value
        :param z: z coordinate value if given
        :return:
        """
        if x is not None and y is not None:
            self.xs.append(x)
            self.ys.append(y)
            if z is not None:
                self.zs.append(z)
        else:
            raise ValueError('x and y should not be None.')

        # If csv_path is not None then write x and y to file
        if self.csv_path is not None:
            self.csv_file.write(str(x) + ',' + str(y) + ',' + str(z) + '\n')
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

    def close_file(self) -> None:
        """
        Close the created file objects
        :return: None
        """
        if self.log_path is not None:
            self.log_file.close()
        if self.csv_path is not None:
            self.csv_file.close()
