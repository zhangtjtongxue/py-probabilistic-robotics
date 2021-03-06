import math
import numpy as np
from robots import transforms

def test_hom():
    a = np.array([[2, 3, 5], [3, 4, 6]])

    np.testing.assert_allclose(
        transforms.h(a, n=1., axis=0), 
        np.array([[2, 3, 5], [3, 4, 6], [1, 1, 1]]))

    np.testing.assert_allclose(
        transforms.h(a, n=1., axis=1), 
        np.array([[2, 3, 5, 1], [3, 4, 6, 1]]))

def test_hnorm():
    a = np.array([[2, 4, 6], [8, 4, 6]])
    b = transforms.h(a, n=2., axis=0)

    np.testing.assert_allclose(
        transforms.hnorm(b, axis=0), 
        np.array([[1, 2, 3], [4, 2, 3]]))

    np.testing.assert_allclose(
        transforms.hnorm(b, axis=0, skip_division=True), 
        np.array([[2, 4, 6], [8, 4, 6]]))

    b = transforms.h(a, n=1., axis=1)
    np.testing.assert_allclose(
        transforms.hnorm(b, axis=1, skip_division=False), 
        np.array([[2, 4, 6], [8, 4, 6]]))

    b = transforms.h(a, n=2., axis=1)
    np.testing.assert_allclose(
        transforms.hnorm(b, axis=1, skip_division=True), 
        np.array([[2, 4, 6], [8, 4, 6]]))

def test_pose_transforms():   
    k = transforms.transform_from_pose([10, 0, math.pi/2])
    np.testing.assert_allclose(
        k,
        np.array([
            [0, -1, 10],
            [1, 0, 0],
            [0, 0, 1],
        ]),
        atol=1e-4
    )

def test_transform_points_vectors():
    m = transforms.transform_from_pose([10, 0, math.pi/2])
    points = np.array([
        [0, -5],
        [0, -5]
    ], dtype=float)

    np.testing.assert_allclose(transforms.transform(m, points), np.array([[10, 15.], [0, -5]]))
    np.testing.assert_allclose(transforms.transform(m, points, hvalue=0.), np.array([[0, 5], [0, -5]]))

    points = np.array([
        [0, -5],
        [0, -5],
        [1, 1]
    ], dtype=float)
    np.testing.assert_allclose(transforms.transform(m, points), np.array([[10, 15], [0, -5], [1,1]]))


def test_rigid_inverse():
    m = transforms.transform_from_pose([10, 0, math.pi/2])
    i = transforms.rigid_inverse(m)
    np.testing.assert_allclose(np.dot(m, i), np.eye(3), atol=1e-4)

def test_pose_from_transform():
    m = transforms.transform_from_pose([10, 0, math.pi/2])
    p = transforms.pose_from_transform(m)
    np.testing.assert_allclose(p, [10, 0, math.pi/2], atol=1e-4)
