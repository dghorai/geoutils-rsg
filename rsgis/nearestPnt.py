# %%
"""
Created on Sun Apr 24 2022

@author: Debabrata Ghorai, Ph.D.

Closest point identification on a line from given point.
"""

# %%
import sys

from .utility import CommonUtils

comt = CommonUtils()

# %%
def find_closest_point(point, inline):
    _, nodes = comt.reading_polyline(inline)
    # generate node pairs for close distance calculation
    node_pair = []
    for node in nodes:
        for i in range(len(node)-1):
            node_pair.append((node[i], node[i+1]))
    # near point identification
    min_dist = sys.maxsize  # a number that is bigger than all others
    nearest_pnt = None
    for i in node_pair:
        ln_start = i[0]
        ln_end = i[1]
        intersect_pnt = comt.intersect_point_to_line(point, ln_start, ln_end)
        cur_dist = comt.dist_calc(point, intersect_pnt)
        if cur_dist < min_dist:
            min_dist = cur_dist
            nearest_pnt = intersect_pnt
    return nearest_pnt


