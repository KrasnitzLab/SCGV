'''
Created on Dec 2, 2016

@author: lubo
'''
import matplotlib.colors as col


class ColorMap(object):

    def __init__(self):
        self.colors = []
        self.bounds = []
        self.norm = None

    @staticmethod
    def make_cmap01():
        cmap01 = ColorMap()
        cmap01.colors = col.ListedColormap(
            ['#DDDD00', '#0000DD', 'white', 'orange', '#DD0000', 'magenta'],
            'indexed')
        cmap01.bounds = [0, 0.5, 1.5, 2.5, 3.5, 4.5, 999999]
        cmap01.norm = col.BoundaryNorm(cmap01.bounds, cmap01.colors.N)
        return cmap01

    @staticmethod
    def make_cmap08():
        cmap08 = ColorMap()
        # VZ - colormap for features map visualization
        cmap08.colors = col.ListedColormap(
            ['#000066', '#0000FF', '#FFFFFF', '#EE0000', '#660000'],
            'indexed')
        cmap08.bounds = [-2, -1, 0, 1, 2, 999999999.9]
        cmap08.norm = col.BoundaryNorm(
            cmap08.bounds, cmap08.colors.N)
        return cmap08

    @staticmethod
    def make_cmap02():
        cmap02 = ColorMap()
        cmap02.colors = col.ListedColormap(
            ['#EEEE00', '#000066', '#0000FF', '#FFFFFF', '#EE0000', '#660000'],
            'indexed')
        cmap02.bounds = [0.0, 0.5, 1.5, 2.5, 3.5, 4.5, 999999999.9]
        cmap02.norm = col.BoundaryNorm(
            cmap02.bounds, cmap02.colors.N)
        return cmap02

    @staticmethod
    def make_cmap03():
        cmap03 = ColorMap()
        cmap03.colors = col.ListedColormap(
            ['#BF3EFF', '#8B0000', '#FF0000', '#FFB90F', '#838B8B', '#000000',
             '#7CFC00', '#006400', '#6E8B3D', '#00FFFF', '#6495ED', '#0000FF',
             '#FFFF00', '#EEDFCC'],
            'indexed')
        cmap03.bounds = [0.0, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5,
                         6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5]
        cmap03.norm = col.BoundaryNorm(
            cmap03.bounds, cmap03.colors.N)

        return cmap03

    @staticmethod
    def make_cmap04():
        # cmap04 = col.ListedColormap(['#e8e8e8', '#505050'], 'indexed')
        # cmap04_bounds = [0.0, 0.5, 1.5]
        # cmap04_norm = col.BoundaryNorm(cmap04_bounds, cmap04.N)
        cmap04 = ColorMap()
        cmap04.colors = col.ListedColormap(
            ['#F0F0F0', '#DDDDDD', '#999999', '#777777', '#333333'],
            'indexed')
        cmap04.bounds = [0.0, 0.5, 1.5, 2.5, 3.5, 4.5]
        cmap04.norm = col.BoundaryNorm(cmap04.bounds, cmap04.colors.N)
        return cmap04

    @staticmethod
    def make_cmap05():
        cmap05 = ColorMap()
        cmap05.colors = col.ListedColormap(
            ['#FFFFFF', '#EEEEEE', '#DDDDDD', '#CCCCCC', '#BBBBBB', '#AAAAAA',
             '#999999',
             '#888888', '#777777', '#666666', '#555555', '#444444', '#333333',
             '#222222', '#111111', '#000000'], 'indexed')
        cmap05.bounds = [0, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5,
                         12.0, 13.5, 15.0, 16.5, 18.0, 19.5, 21.0, 22.5,
                         999999999]
        cmap05.norm = col.BoundaryNorm(
            cmap05.bounds, cmap05.colors.N)

        return cmap05

    @staticmethod
    def make_cmap06():
        cmap06 = ColorMap()
        cmap06.colors = col.ListedColormap(
            ['#FFFFFF', '#CCCCCC', '#999999', '#666666', '#333333'], 'indexed')
        cmap06.bounds = [0, 2.5, 3.5, 4.5, 5.5, 999999999]
        cmap06.norm = col.BoundaryNorm(cmap06.bounds, cmap06.colors.N)

        return cmap06

    @staticmethod
    def make_cmap07():
        cmap07 = ColorMap()
        cmap07.colors = col.ListedColormap(
            ['white', '#CC0000', 'gold', 'blue', 'orange', 'green', 'violet'],
            'indexed')
        cmap07.bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 999999999]
        cmap07.norm = col.BoundaryNorm(cmap07.bounds, cmap07.colors.N)
        return cmap07

    @staticmethod
    def make_diverging11():
        cmap = ColorMap()
        cmap.colors = col.ListedColormap(
            ['#67001f', '#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#f7f7f7',
             '#d1e5f0', '#92c5de', '#4393c3', '#2166ac', '#053061'])

        return cmap

    @staticmethod
    def make_deverging09():
        """
        0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4; centered at 2;
        """
        cmap = ColorMap()
        colors = ['#b2182b', '#d6604d', '#f4a582', '#fddbc7', '#f7f7f7',
                  '#d1e5f0', '#92c5de', '#4393c3', '#2166ac']
        cmap.colors = col.ListedColormap(colors[::-1])
        return cmap

    @staticmethod
    def make_qualitative12():
        cmap = ColorMap()
        colors = [
            '#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99',
            '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a',
            '#ffff99', '#b15928']
        cmap.colors = col.ListedColormap(colors[::-1])
        return cmap

    @staticmethod
    def make_qualitative(N=6):
        cmap = ColorMap()
        colors = [
            '#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33'
        ]
        cmap.colors = col.ListedColormap(colors, N=N)
        return cmap

    @staticmethod
    def make_qualitative06_with_white():
        cmap = ColorMap()
        colors = [
            'white',
            '#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33'
        ]
        cmap.colors = col.ListedColormap(colors)
        cmap.bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 999999999]
        cmap.norm = col.BoundaryNorm(cmap.bounds, cmap.colors.N)

        return cmap

    @staticmethod
    def make_diverging05():
        cmap = ColorMap()
        N = 5
        colors = ['#0571b0', '#92c5de', '#f7f7f7', '#f4a582', '#ca0020', ]
        cmap.colors = col.ListedColormap(colors, N=N)
        return cmap
