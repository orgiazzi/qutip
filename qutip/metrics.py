# This file is part of QuTiP.
#
#    QuTiP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    QuTiP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with QuTiP.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2011 and later, Paul D. Nation & Robert J. Johansson
#
###########################################################################

"""
A Module containing a collection of metrics
(distance measures) between density matrices..
"""

from qutip.qobj import *
import scipy.linalg as la
import numpy as np
from qutip.sparse import sp_eigs


def fidelity(A, B):
    """
    Calculates the fidelity (pseudo-metric) between two density matrices..
    See: Nielsen & Chuang, "Quantum Computation and Quantum Information"

    Parameters
    ----------
    A : qobj
        Density matrix or state vector.
    B : qobj
        Density matrix or state vector with same dimensions as A.

    Returns
    -------
    fid : float
        Fidelity pseudo-metric between A and B.

    Examples
    --------
    >>> x=fock_dm(5,3)
    >>> y=coherent_dm(5,1)
    >>> fidelity(x,y)
    0.24104350624628332

    """
    if A.type != 'oper':
        A = ket2dm(A)
    if B.type != 'oper':
        B = ket2dm(B)
    if A.dims != B.dims:
        raise TypeError('Density matrices do not have same dimensions.')
    else:
        A = A.sqrtm()
        return float(np.real((A * (B * A)).sqrtm().tr()))


def tracedist(A, B, sparse=False, tol=0):
    """
    Calculates the trace distance between two density matrices..
    See: Nielsen & Chuang, "Quantum Computation and Quantum Information"

    Parameters
    ----------
    A : qobj
        Density matrix or state vector.
    B : qobj
        Density matrix or state vector with same dimensions as A.
    tol : float
        Tolerance used by sparse eigensolver, if used. (0=Machine precision)
    sparse : {False, True}
        Use sparse eigensolver.

    Returns
    -------
    tracedist : float
        Trace distance between A and B.

    Examples
    --------
    >>> x=fock_dm(5,3)
    >>> y=coherent_dm(5,1)
    >>> tracedist(x,y)
    0.9705143161472971

    """
    if A.type != 'oper':
        A = ket2dm(A)
    if B.type != 'oper':
        B = ket2dm(B)
    if A.dims != B.dims:
        raise TypeError('Density matrices. do not have same dimensions.')
    else:
        diff = A - B
        diff = diff.dag() * diff
        vals = sp_eigs(diff, vecs=False, sparse=sparse, tol=tol)
        return float(np.real(0.5 * np.sum(np.sqrt(np.abs(vals)))))


def hilbert_dist(A, B):
    """
    Returns the Hilbert-Schmidt distance between two density matrices A & B.

    Parameters
    ----------
    A : qobj
        Density matrix or state vector.
    B : qobj
        Density matrix or state vector with same dimensions as A.

    Returns
    -------
    dist : float
        Hilbert-Schmidt distance between density matrices.

    """
    if A.type != 'oper':
        A = ket2dm(A)
    if B.type != 'oper':
        B = ket2dm(B)
    if A.dims != B.dims:
        raise TypeError('Density matrices do not have same dimensions.')
    return (A - B).norm('fro')


def bures_dist(A, B):
    """
    Returns the Bures distance between two density matrices A & B.

    The Bures distance ranges from 0, for states with unit fidelity,
    to sqrt(2).

    Parameters
    ----------
    A : qobj
        Density matrix or state vector.
    B : qobj
        Density matrix or state vector with same dimensions as A.

    Returns
    -------
    dist : float
        Bures distance between density matrices.

    """

    if A.type != 'oper':
        A = ket2dm(A)
    if B.type != 'oper':
        B = ket2dm(B)
    if A.dims != B.dims:
        raise TypeError('Density matrices do not have same dimensions.')
    dist = np.sqrt(2.0 * (1.0 - np.sqrt(fidelity(A, B))))
    return dist


def bures_angle(A, B):
    """
    Returns the Bures Angle between two density matrices A & B.

    The Bures angle ranges from 0, for states with unit fidelity, to pi/2.

    Parameters
    ----------
    A : qobj
        Density matrix or state vector.
    B : qobj
        Density matrix or state vector with same dimensions as A.

    Returns
    -------
    angle : float
        Bures angle between density matrices.

    """

    if A.type != 'oper':
        A = ket2dm(A)
    if B.type != 'oper':
        B = ket2dm(B)
    if A.dims != B.dims:
        raise TypeError('Density matrices do not have same dimensions.')
    return np.arccos(np.sqrt(fidelity(A, B)))
