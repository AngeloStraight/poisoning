import sys, copy
from anti_gonzalez import Poison
from gonzalez import KCenter

def poison_data(m):
    """ read in the data """
    arr_corners = process_data()

    """ run gonzalaz on the point befor we poison the data """ 
    points = copy.deepcopy(arr_corners[0])
    clusters = KCenter(points, 3, [])        # here 3 is the number of clusters
    clusters.gonzalez()
    clusters.show()

    """ poison the data """
    myPoison = Poison(6, arr_corners[0], arr_corners[1])
    myPoison.show_points()
    myPoison.anti_gonzalaz()
    print("\n--------------------------\n")
    myPoison.show_points()
    myPoison.show_poison_points()
    clusters = KCenter(myPoison.get_points(), 3, myPoison.get_poison())
    clusters.gonzalez()
    clusters.show_points()
    clusters.show_centers()
    clusters.show()

def main():
    poison_data(3)
    

def process_data():
    if (len(sys.argv) != 2):
        print("usage: python anti_gonzales.py <filename>.txt")
        exit()

    f = open(sys.argv[1], "r")
    data = f.readlines()

    """ process the data"""
    strip_data = []
    for d in range(len(data)):
        data[d] = data[d].rstrip()
        strip_data.append(data[d].split(" "))

    """ push the points into an array """
    arr = []
    corners = []
    for p in range(len(strip_data)):
        new_point = float(strip_data[p][0]), float(strip_data[p][1])
        if p < 4:
            corners.append(list( new_point))
        else:
            arr.append(list( new_point))
    return arr, corners

if __name__ == "__main__":
    main()