import math, random, sys
import numpy as np
import matplotlib.pyplot as plt

class Cluster:
    def __init__(self, center):
        self.center = center
        self.c_points = []
        self.radius = 0

    def set_radius(self):
        if len(self.c_points) == 0: self.radius = 0
        else:
            f_radius = -1     # keep track of the furthest point
            for point in self.c_points:
                curr_radius = math.dist(self.center, point)
                if curr_radius > f_radius:
                    f_radius = curr_radius
            self.radius = f_radius



class KCenter():

    def __init__(self, points, k, poison):
        self.points = points
        self.centers = []
        self.clusters = []
        self.k = k
        self.poison_points = poison

    def show_points(self):
        print("size of points gonzalaz: ", len(self.points))
        for p in self.points:
            print(p)

    def show_centers(self):
        print("size of centers: ", len(self.centers))
        for c in self.centers:
            print(c)

    def set_radius(self):
        for cl in self.clusters:
            cl.set_radius()
            print("Center: ",cl.center, " With Radius: ", cl.radius)

    def init_clusters(self):
        """ create the clusters """
        for i in range(len(self.centers)):
            self.clusters.append(Cluster(self.centers[i]))

    def assign_points(self):
        """ assign points to clusters """
        self.init_clusters()
        index = None
        for k in range(len(self.points)):
            min_cluster_dist = sys.maxsize
            for j in range(len(self.clusters)):
                curr_dist = math.dist(self.points[k], self.clusters[j].center)
                if curr_dist < min_cluster_dist:
                    min_cluster_dist = curr_dist
                    index = j
            self.clusters[index].c_points.append(self.points[k])
        self.set_radius()

    def furthest_point(self, p1):
        """ Return the index of the furthest """
        index = 0
        max_dist = math.dist(self.points[0], p1)
        for i in range(1,len(self.points)):
            new_dist = math.dist(self.points[i], p1)
            if (new_dist > max_dist):
                max_dist = new_dist
                index = i
        return index

    def show(self):
        """ put x coordinates and y coordinates into arrays to plot the points """
        dev_x = []
        dev_y = []
        for point in self.points:
            dev_x.append(point[0])
            dev_y.append(point[1])

        """ make arrays for centers and plot on scatter plot """
        c_x = []
        c_y = []
        for cluster in self.clusters:
            c_x.append(cluster.center[0])
            c_y.append(cluster.center[1])

        """ make array for poison points"""
        p_x = []
        p_y = []
        for poison in self.poison_points:
            p_x.append(poison[0])
            p_y.append(poison[1])

        plt.scatter(dev_x, dev_y)            # plot all the points.
        plt.scatter(p_x, p_y, color='g')     # plot the poison points. color them green.
        plt.scatter(c_x, c_y, color='r')     # plot the centers. color them red.
        plt.show()


    def gonzalez(self):
        """ gonzalez"""
        p = self.points.pop(random.randint(0, len(self.points)-1))    # first point is random
        self.centers.append(p)
        index = self.furthest_point(p)                        # second point is point furthest from first point
        sec_pt = self.points.pop(index)
        self.centers.append(sec_pt)
        dist_arr = []
        while len(self.centers) < self.k:
            for i in range(len(self.centers)):
                min_dist = (sys.maxsize, -1)              # tuple (distance, index)
                for j in range(len(self.points)):
                    curr_dist = math.dist(self.centers[i], self.points[j])
                    if curr_dist < min_dist[0]:
                        min_dist = (curr_dist, j)        # set smallest distance and the index
                dist_arr.append(min_dist)
            max_dist = (-1, -1)
            for i in range(len(dist_arr)):               # now find the max of all the min distance. min-max problem
                if dist_arr[i][0] > max_dist[0]:
                    max_dist = dist_arr[i]
            new_center = self.points.pop(max_dist[1])    # add the new center
            self.centers.append(new_center)
            self.assign_points()