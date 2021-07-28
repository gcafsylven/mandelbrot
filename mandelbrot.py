import matplotlib.pyplot as plt

import numpy as np


from decimal import *
getcontext().prec = 25 #Sets the precision of digits


class Matrix:


    res = 500 #Resolution nxn

    colormap = 'twilight_shifted' #A matshow supported colormap

    range = Decimal('2.8') #Sets range +/-  in X and Y
    max_n=200 #Number of max iterations. Higher number is needed for deeper zoom in, but increases computation time.



    x_center = Decimal(0)
    y_center = Decimal(0)

    x_arr = []
    y_arr = []

    x_min=0
    x_max=0
    y_min=0
    y_max=0

    def update_max_n(self):
        self.max_n = self.max_n+10

    def update_x_y_center(self,x,y):
        self.x_center = Decimal(str(x))
        self.y_center = Decimal(str(y))


    def update_current_coordinates(self):
        self.x_min = self.x_center - self.range/2
        self.x_max = self.x_center + self.range/2

        self.y_min = self.y_center - self.range/2
        self.y_max = self.y_center + self.range/2

        x_delta = self.x_max - self.x_min
        y_delta = self.y_max - self.y_min

        self.x_arr = [self.x_min + ((i * x_delta) / self.res) for i in range(0, self.res)]
        self.y_arr = [self.y_max - ((i * y_delta) / self.res) for i in range(0, self.res)]

        self.range =  self.range / 10



    def get_matrix(self):
        matrix = []

        #TODO: divide the vertical part of the matrix with threading to improve performance
        for y0 in self.y_arr:

            columns = []
            for x0 in self.x_arr:

                x=0
                y=0
                for n in range(0, self.max_n):

                    xnew = x * x - y * y + x0;
                    ynew = 2 * x * y + y0;


                    refval = xnew * xnew + ynew * ynew

                    if (refval > 4):
                        break;
                    x = xnew;
                    y = ynew;

                columns.append(n)
            matrix.append(columns)

        return matrix

    def get_range(self):
        #print([self.x_min,self.x_max,self.y_min,self.y_max])
        return [float(self.x_min),float(self.x_max),float(self.y_min),float(self.y_max)]


def zoom(ax, matrix):
    def get_matrix():
        ax.matshow(matrix.get_matrix(), extent=matrix.get_range(), vmin=0, vmax=200, cmap=matrix.colormap,
                   interpolation='nearest')

    def zoom_fun(event):
        xdata = event.xdata  # get event x location
        ydata = event.ydata  # get event y location

        matrix.update_x_y_center(xdata, ydata)

        matrix.update_current_coordinates()

        ax.clear()

        get_matrix()

        ax.figure.canvas.draw_idle()  # force re-draw the next time the GUI refreshes

    matrix.update_current_coordinates()
    get_matrix()

    fig = ax.get_figure()  # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('button_press_event', zoom_fun)

    # return the function
    return zoom_fun


matrix = Matrix()


fig = plt.figure()

plot = fig.add_subplot(111)


zf = zoom(plot,matrix)
plt.show()
