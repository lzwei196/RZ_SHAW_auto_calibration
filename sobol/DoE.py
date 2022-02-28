##generate the sample points first through sobol sequence
import torch
import numpy

def sobol(dimension, draw, seed=None):
    soboleng = torch.quasirandom.SobolEngine(dimension=dimension)
    n = numpy.array(soboleng.draw(draw))
    return n


