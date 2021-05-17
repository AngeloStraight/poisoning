import sys, math, numpy as np 
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

class Poison():
    """ class for poison """
    def __init__(self, m, points, corners):
        self.m = m
        self.points = points        # my goal is to poison these points
        self.vor = None             # we use voronoi to find furtheset point
        self.vertices = []
        self.corners = corners
        self.poison_points = []

    def show_points(self):
        for p in self.points:
            print(p)

    def get_poison(self):
        return self.poison_points
        
    def show_poison_points(self):
        for p in self.poison_points:
            print(p)

    def get_points(self):
        return self.points

    def create_voronoi(self):
        """ creates and returns a voronoi diagram """
        v_points = np.array(self.points)
        self.vor = Voronoi(v_points)
       
    def show_voronoi(self):
        voronoi_plot_2d(self.vor)
        plt.show()

    def set_vertices(self):
        """ exclude the vertices with negative x,y values """
        vertices_n = self.vor.vertices.tolist()
        self.vertices = []
        for i in range(len(vertices_n)):
            """ only consider vertices in range 0-100"""
            #if not (vertices_n[i][0] < 0 or vertices_n[i][1] < 0 or vertices_n[i][0] > 100 or vertices_n[i][1] > 100):
                #self.vertices.append(vertices_n[i])
            print("vertices: ", vertices_n[i])
            self.vertices.append(vertices_n[i])

    def anti_gonzalaz(self):
        for i in range(self.m):
            self.create_voronoi()
            self.place_poison()


    def remove_corner(self):
        for i in range(len(self.corners)):
            if self.corners[i] in self.points:
                self.corners.pop(i)

    def place_poison(self):
        min_dis_v = []
        min_d = sys.maxsize
        self.set_vertices()
        if (len(self.corners) > 0):
            self.vertices = self.vertices + self.corners # when looking for poison position, consider the vertices and corners of space

        """ find the min distance between all points and vertices """
        for i in range(len(self.vertices)):
            for j in range(len(self.points)):
                dist_p_v = math.dist(self.points[j], self.vertices[i])
                if  dist_p_v < min_d:
                    min_d = dist_p_v
            min_dis_v.append(min_d)
            min_d = sys.maxsize

        """ get the max between all the min distances """
        max_dist = -1
        index = -1
        for i in range(len(min_dis_v)):
            if min_dis_v[i] > max_dist:
                max_dist = min_dis_v[i]
                index = i
        self.points.append(self.vertices[index])
        self.poison_points.append(self.vertices[index])
        #self.remove_corner()
