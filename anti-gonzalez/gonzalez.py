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

    def get_radius(self):
        return self.radius

    def get_center(self):
        return self.center



class KCenter():

    def __init__(self, points, k, poison):
        self.points = points
        self.centers = []
        self.clusters = []
        self.k = k
        self.poison_points = poison

    def show_points(self):
        for p in self.points:
            print(p)

    def show_centers(self):
        for c in self.centers:
            print(c)

    def set_radius(self):
        for cl in self.clusters:
            cl.set_radius()

    def get_radius(self):
        radius = sys.maxsize
        for cl in self.clusters:
            if cl.radius > 0 and cl.radius < radius:
                radius = cl.radius
        return radius

    def init_clusters(self):
        """ create the clusters """
        for i in range(len(self.centers)):
            self.clusters.append(Cluster(self.centers[i]))

    def get_clusters(self):
        return self.clusters

    def get_centers(self):
        return self.centers

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
        for i in range(len(self.points)):
            new_dist = math.dist(self.points[i], p1)
            if (new_dist > max_dist):
                max_dist = new_dist
                index = i
        return index

    def show(self):

        fig, ax = plt.subplots()
        
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
        plt.scatter(p_x, p_y, color='g')    # plot the poison points. color them green.

       # for cluster in self.clusters:
        #     ax.add_patch(plt.Circle(cluster.center, radius=0.3, color=(0.1,0.5,0.1,0.3)))
         #   plt.scatter(cluster.center[0], cluster.center[1], marker = "o", s = 1000*cluster.radius, alpha = 0.25)     # plot the centers. color them red.

        # to color the centers red
        plt.scatter(c_x, c_y, color='r')

        colors = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

        for c in self.clusters:
            ax.add_patch(plt.Circle(c.center, radius=c.radius, color=(colors[random.randint(0, 9)] ,colors[random.randint(0, 9)],colors[random.randint(0, 9)],0.3)))
        ax.axis('equal')
        ax.margins(0)
    
        plt.show()
        #fname = str(random.randint(0, 100000)) + ".png"
        #fig.savefig(fname, dpi=fig.dpi)


    def gonzalez(self):
        """ gonzalez"""
        if (self.k < 1):
            return

        p = self.points.pop(random.randint(0, len(self.points)-1))    # first point is random
        self.centers.append(p)
        if (self.k == 1):
            print("only one point: ", self.k, self.centers[0])
            self.assign_points()
            return
            
        index = self.furthest_point(p)                        # second point is point furthest from first point
        sec_pt = self.points.pop(index)
        self.centers.append(sec_pt)
        
        while len(self.centers) < self.k:
            dist_arr = [0] * len(self.points)
            for i in range(len(self.centers)):
                for j in range(len(self.points)):
                    dist_arr[j] = dist_arr[j] + math.dist(self.centers[i], self.points[j])
            max_dist = (-1, -1)
            for i in range(len(dist_arr)):
                if dist_arr[i] > max_dist[0]:
                    max_dist = (dist_arr[i], i)
            new_center = self.points.pop(max_dist[1])    # add the new center
            self.centers.append(new_center)
        self.assign_points()