import copy, math

class Robust:
    """ Robust Clustering for Arbitrary Metrics
        points is the point set, r is the radius, k is 
        the number of clusters and m is the number of outliers(poison) """
    def __init__(self, points, r, k, m):
        self.points = points
        self.disks_g = []
        self.disks_c = []
        self.radius = r
        self.k = k
        self.m = m

    def construct_disks_g(self):
        """ function to construct disk of radius r """
        for i in range(len(self.points)):
            temp = []
            for j in range(len(self.points)):
                if (i != j) and ( math.dist(self.points[i], self.points[j]) <= self.radius ):
                    temp.append(self.points[j])

            if len(temp) > 0:
                self.disks_g.append(temp)

    def construct_disks_e(self):
        """ function to construct disk of radius 3r """
        r_3 = 3 * self.radius
        for i in range(len(self.points)):
            temp = []
            for j in range(len(self.points)):
                if (i != j) and ( math.dist(self.points[i], self.points[j]) <= r_3 ):
                    temp.append(self.points[j])

            if len(temp) > 0:
                self.disks_c.append(temp)

    def show_points(self):
        print(self.points)

    def robust_clustering(self):
        """ 
        Algorithm for robust clustering 

        • Construct all disks and corresponding expanded disks.
        • Repeat the following k times:
            – Let Gj be the heaviest disk, i.e. contains the most uncovered points.
            – Mark as covered all points in the correspond- ing expanded disk Ej .
            – Update all the disks and expanded disks, i.e., remove from them all covered points.
        • If at least p points of V are marked as covered, then answer YES, else answer NO.
        """
        self.construct_disks_e()
        for i in range(self.k):
            self.remove_heaviest()

        if len(self.points) > self.m:
            return 'Yes'
        else:
            return 'No'


    def remove_heaviest(self):
        """ remove the disk with the most points. mark points as covered """
        index = 0
        heaviest = len(self.disks_c[0])
        for i in range(1, len(self.disks_c)):
            if len(self.disks_c[i]) > heaviest:
                heaviest = len(self.disks_c[i])
                index = i
        for i in range(len(self.disks_c[index])):
            if self.disks_c[index][i] in self.points:
                self.points.remove(self.disks_c[index][i])

        self.disks_c.pop(index)


    def show_disks_g(self):
        for p in self.disks_g:
            print(p)

    def show_disks_c(self):
        for p in self.disks_c:
            print(p)
