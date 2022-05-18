from unittest import TestCase

import casadi as ca
import numpy as np

from hilo_mpc import Kernel


# TODO: Align function arguments for kernels with function arguments for means (hyperprior, ...)
class TestConstantKernel(TestCase):
    """"""
    def test_constant_kernel_no_hyperprior(self) -> None:
        """

        :return:
        """
        kernel = Kernel.constant()

        self.assertIsNone(kernel.active_dims)
        self.assertTrue(hasattr(kernel.bias, 'log'))
        np.testing.assert_equal(kernel.bias.value, np.ones((1, 1)))
        np.testing.assert_equal(kernel.bias.log, np.zeros((1, 1)))
        self.assertEqual(len(kernel.hyperparameters), 1)
        self.assertEqual(kernel.hyperparameter_names, ['Const.bias'])

    def test_constant_kernel_fixed(self) -> None:
        """

        :return:
        """
        # TODO: Change according to test_means.py when first TODO is finished
        kernel = Kernel.constant()
        kernel.bias.fixed = True

        self.assertTrue(kernel.bias.fixed)

    # def test_constant_kernel_hyperprior_gaussian(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     # TODO: Create according to test_means.py when first TODO is finished

    def test_constant_kernel_symbolic_call_sx(self) -> None:
        """

        :return:
        """
        kernel = Kernel.constant()

        x = ca.SX.sym('x')
        cov = kernel(x)

        self.assertIsInstance(cov, ca.SX)
        self.assertTrue(ca.depends_on(cov, kernel.bias.SX))
        self.assertFalse(ca.depends_on(cov, x))

    # def test_constant_kernel_symbolic_call_mx(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.constant()
    #
    #     x = ca.MX.sym('x')
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     self.assertTrue(ca.depends_on(cov, kernel.bias.MX))
    #     self.assertFalse(ca.depends_on(cov, x))

    def test_constant_kernel_numeric_call(self) -> None:
        """

        :return:
        """
        kernel = Kernel.constant()

        x = np.array([[1., 2., 3., 4., 5.]])
        cov = kernel(x)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_equal(cov, np.ones((5, 5)))

        kernel.bias.value = 2.
        cov = kernel(x)
        np.testing.assert_equal(cov, 4. * np.ones((5, 5)))

    def test_constant_kernel_symbolic_call_x_x_bar_wrong_type(self) -> None:
        """

        :return:
        """
        kernel = Kernel.constant()

        x = ca.SX.sym('x')
        y = np.array([[2.]])
        # FIXME: Convert to TypeError
        with self.assertRaises(ValueError) as context:
            kernel(x, y)
        self.assertEqual(str(context.exception), "X and X_bar need to have the same type")

    def test_constant_kernel_symbolic_call_x_x_bar_sx(self) -> None:
        """

        :return:
        """
        kernel = Kernel.constant()

        x = ca.SX.sym('x')
        y = ca.SX.sym('y')
        cov = kernel(x, y)

        self.assertIsInstance(cov, ca.SX)
        self.assertTrue(ca.depends_on(cov, kernel.bias.SX))
        self.assertFalse(ca.depends_on(cov, x))
        self.assertFalse(ca.depends_on(cov, y))

    # def test_constant_kernel_symbolic_call_x_x_bar_mx(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.constant()
    #
    #     x = ca.MX.sym('x')
    #     y = ca.MX.sym('y')
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x, y)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     self.assertTrue(ca.depends_on(cov, kernel.bias.MX))
    #     self.assertFalse(ca.depends_on(cov, x))
    #     self.assertFalse(ca.depends_on(cov, y))

    def test_constant_kernel_numeric_call_x_x_bar_wrong_type(self) -> None:
        """

        :return:
        """
        kernel = Kernel.constant()

        x = np.array([[2.]])
        y = ca.SX.sym('y')
        # FIXME: Convert to TypeError
        with self.assertRaises(ValueError) as context:
            kernel(x, y)
        self.assertEqual(str(context.exception), "X and X_bar need to have the same type")

    def test_constant_kernel_numeric_call_x_x_bar(self) -> None:
        """

        :return:
        """
        kernel = Kernel.constant()

        x = np.array([[1., 2., 3., 4., 5.]])
        y = np.array([[1., 2., 3., 4., 5.]])
        cov = kernel(x, y)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_equal(cov, np.ones((5, 5)))

        kernel.bias.value = 2.
        cov = kernel(x, y)
        np.testing.assert_equal(cov, 4. * np.ones((5, 5)))


class TestSquaredExponentialKernel(TestCase):
    """"""
    def test_squared_exponential_kernel_no_hyperprior(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential()

        self.assertIsNone(kernel.active_dims)
        np.testing.assert_equal(kernel.alpha, .5)
        np.testing.assert_equal(kernel.gamma, 2.)
        self.assertEqual(len(kernel.hyperparameters), 2)
        self.assertEqual(kernel.hyperparameter_names, ['SE.length_scales', 'SE.signal_variance'])
        self.assertTrue(hasattr(kernel.length_scales, 'log'))
        np.testing.assert_equal(kernel.length_scales.value, np.ones((1, 1)))
        np.testing.assert_equal(kernel.length_scales.log, np.zeros((1, 1)))
        self.assertTrue(hasattr(kernel.signal_variance, 'log'))
        np.testing.assert_equal(kernel.signal_variance.value, np.ones((1, 1)))
        np.testing.assert_equal(kernel.signal_variance.log, np.zeros((1, 1)))

    def test_squared_exponential_kernel_fixed(self) -> None:
        """

        :return:
        """
        # TODO: Change according to test_means.py when first TODO is finished
        kernel = Kernel.squared_exponential()
        kernel.length_scales.fixed = True
        kernel.signal_variance.fixed = True

        self.assertTrue(kernel.length_scales.fixed)
        self.assertTrue(kernel.signal_variance.fixed)

    # def test_squared_exponential_kernel_hyperprior_gaussian(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     # TODO: Create according to test_means.py when first TODO is finished

    def test_squared_exponential_kernel_ard_no_active_dims(self) -> None:
        """

        :return:
        """
        with self.assertRaises(ValueError) as context:
            Kernel.squared_exponential(ard=True)
        self.assertEqual(str(context.exception),
                         "The key word 'ard' can only be set to True if the key word 'active_dims' was supplied")

    def test_squared_exponential_kernel_ard_dimension_mismatch(self) -> None:
        """

        :return:
        """
        with self.assertRaises(ValueError) as context:
            Kernel.squared_exponential(active_dims=[0, 1], length_scales=[1., 1., 1.])
        self.assertEqual(str(context.exception),
                         "Dimension mismatch between 'active_dims' (2) and the number of length_scales (3)")

    def test_squared_exponential_kernel_symbolic_call_sx(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential()

        x = ca.SX.sym('x')
        cov = kernel(x)

        self.assertIsInstance(cov, ca.SX)
        self.assertFalse(ca.depends_on(cov, kernel.length_scales.SX))
        self.assertTrue(ca.depends_on(cov, kernel.signal_variance.SX))
        self.assertFalse(ca.depends_on(cov, x))

    # def test_squared_exponential_kernel_symbolic_call_mx(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.squared_exponential()
    #
    #     x = ca.MX.sym('x')
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     self.assertFalse(ca.depends_on(cov, kernel.length_scales.MX))
    #     self.assertTrue(ca.depends_on(cov, kernel.signal_variance.MX))
    #     self.assertFalse(ca.depends_on(cov, x))

    def test_squared_exponential_kernel_numeric_call(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential()

        x = np.array([[1., 2., 3., 4., 5.]])
        cov = kernel(x)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_allclose(cov, np.array([[1., .60653066, .135335283, .0111089965, .000335462628],
                                                  [.60653066, 1., .60653066, .135335283, .0111089965],
                                                  [.135335283, .60653066, 1., .60653066, .135335283],
                                                  [.0111089965, .135335283, .60653066, 1., .60653066],
                                                  [.000335462628, .0111089965, .135335283, .60653066, 1.]]))

    def test_squared_exponential_kernel_symbolic_call_x_x_bar_wrong_type(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential()

        x = ca.SX.sym('x')
        y = np.array([[2.]])
        # FIXME: Convert to TypeError
        with self.assertRaises(ValueError) as context:
            kernel(x, y)
        self.assertEqual(str(context.exception), "X and X_bar need to have the same type")

    def test_squared_exponential_kernel_symbolic_call_x_x_bar_dimension_mismatch(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential()

        x = ca.SX.sym('x', 2)
        y = ca.SX.sym('y')
        # FIXME: Convert to ValueError
        with self.assertRaises(AssertionError) as context:
            kernel(x, y)
        self.assertEqual(str(context.exception), "X and X_bar do not have the same input space dimensions")

    def test_squared_exponential_kernel_symbolic_call_x_x_bar_sx(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential()

        x = ca.SX.sym('x')
        y = ca.SX.sym('y')
        cov = kernel(x, y)

        self.assertIsInstance(cov, ca.SX)
        self.assertTrue(ca.depends_on(cov, kernel.length_scales.SX))
        self.assertTrue(ca.depends_on(cov, kernel.signal_variance.SX))
        self.assertTrue(ca.depends_on(cov, x))
        self.assertTrue(ca.depends_on(cov, y))

    # def test_squared_exponential_kernel_symbolic_call_x_x_bar_mx(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.squared_exponential()
    #
    #     x = ca.MX.sym('x')
    #     y = ca.MX.sym('y')
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x, y)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     self.assertTrue(ca.depends_on(cov, kernel.length_scales.MX))
    #     self.assertTrue(ca.depends_on(cov, kernel.signal_variance.MX))
    #     self.assertTrue(ca.depends_on(cov, x))
    #     self.assertTrue(ca.depends_on(cov, y))

    def test_squared_exponential_kernel_numeric_call_x_x_bar_wrong_type(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential()

        x = np.array([[2.]])
        y = ca.SX.sym('y')
        # FIXME: Convert to TypeError
        with self.assertRaises(ValueError) as context:
            kernel(x, y)
        self.assertEqual(str(context.exception), "X and X_bar need to have the same type")

    def test_squared_exponential_kernel_numeric_call_x_x_bar_dimension_mismatch(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential()

        x = np.array([[1.], [2.]])
        y = np.array([[1.]])
        # FIXME: Convert to ValueError
        with self.assertRaises(AssertionError) as context:
            kernel(x, y)
        self.assertEqual(str(context.exception), "X and X_bar do not have the same input space dimensions")

    def test_squared_exponential_kernel_numeric_call_x_x_bar(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential()

        x = np.array([[1., 2., 3., 4., 5.]])
        y = np.array([[1., 2., 3., 4., 5.]]) / 2.
        cov = kernel(x, y)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_allclose(
            cov,
            np.array([[.8824969, 1., .8824969, .60653066, .32465247],
                      [.32465247, .60653066, .8824969, 1., .8824969],
                      [.04393693, .13533528, .32465247, .60653066, .8824969],
                      [.0021874911, .0111089965, .04393693, .13533528, .32465247],
                      [.0000400652974, .000335462628, .0021874911, .0111089965, .04393693]])
                                   )

    def test_squared_exponential_kernel_ard(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential(active_dims=[0, 1], length_scales=[1., 1.])

        self.assertEqual(kernel.active_dims, [0, 1])
        np.testing.assert_equal(kernel.length_scales.value, np.ones((2, 1)))

        kernel = Kernel.squared_exponential(active_dims=[0, 1, 2], ard=True)

        self.assertEqual(kernel.active_dims, [0, 1, 2])
        np.testing.assert_equal(kernel.length_scales.value, np.ones((3, 1)))

    # def test_squared_exponential_kernel_ard_call_dimension_mismatch(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     # TODO: Create similar test for means
    #     kernel = Kernel.squared_exponential(active_dims=[0, 1], length_scales=[1., 1.])
    #
    #     x = ca.SX.sym('x')
    #     # FIXME: This will result in another error that could be unclear to the user. We should probably catch it and
    #     #  return a more informative error message.
    #     cov = kernel(x)

    def test_squared_exponential_kernel_ard_call_dimension_mismatch(self) -> None:
        """

        :return:
        """
        # TODO: Create similar test for means
        kernel = Kernel.squared_exponential(length_scales=[1., 1.])

        x = ca.SX.sym('x')
        with self.assertRaises(ValueError) as context:
            kernel(x)
        self.assertEqual(str(context.exception), "Length scales vector dimension does not equal input space dimension.")

    def test_squared_exponential_kernel_ard_symbolic_call_sx(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential(length_scales=[1., 1.])

        x = ca.SX.sym('x', 2)
        cov = kernel(x)

        self.assertIsInstance(cov, ca.SX)
        self.assertFalse(ca.depends_on(cov, kernel.length_scales.SX))
        self.assertTrue(ca.depends_on(cov, kernel.signal_variance.SX))
        self.assertFalse(ca.depends_on(cov, x))

    def test_squared_exponential_kernel_ard_symbolic_call_sx_not_all_active(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential(active_dims=[0, 2], length_scales=[1., 1.])

        x = ca.SX.sym('x', 3)
        cov = kernel(x)

        self.assertIsInstance(cov, ca.SX)
        self.assertFalse(ca.depends_on(cov, kernel.length_scales.SX))
        self.assertTrue(ca.depends_on(cov, kernel.signal_variance.SX))
        self.assertFalse(ca.depends_on(cov, x))

    # def test_squared_exponential_kernel_ard_symbolic_call_mx(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.squared_exponential(length_scales=[1., 1.])
    #
    #     x = ca.MX.sym('x', 2)
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     self.assertFalse(ca.depends_on(cov, kernel.length_scales.MX))
    #     self.assertTrue(ca.depends_on(cov, kernel.signal_variance.MX))
    #     self.assertFalse(ca.depends_on(cov, x))

    # def test_squared_exponential_kernel_ard_symbolic_call_mx_not_all_active(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.squared_exponential(active_dims=[0, 2], length_scales=[1., 1.])
    #
    #     x = ca.MX.sym('x', 3)
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     self.assertFalse(ca.depends_on(cov, kernel.length_scales.MX))
    #     self.assertTrue(ca.depends_on(cov, kernel.signal_variance.MX))
    #     self.assertFalse(ca.depends_on(cov, x))

    def test_squared_exponential_kernel_ard_numeric_call(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential(length_scales=[1., 1.])

        x = np.array([[1., 2., 3., 4., 5.], [.1, .2, .3, .4, .5]])
        cov = kernel(x)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_allclose(cov, np.array([[1., .603505575, .132655465, .010620173, .00030967104],
                                                  [.603505575, 1., .603505575, .132655465, .010620173],
                                                  [.132655465, .603505575, 1., .603505575, .132655465],
                                                  [.010620173, .132655465, .603505575, 1., .603505575],
                                                  [.00030967104, .010620173, .132655465, .603505575, 1.]
                                                  ]))

    def test_squared_exponential_kernel_ard_numeric_call_not_all_active(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential(active_dims=[0, 2], length_scales=[1., 1.])

        x = np.array([[1., 2., 3., 4., 5.], [6., 7., 8., 9., 0.], [.1, .2, .3, .4, .5]])
        cov = kernel(x)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_allclose(cov, np.array([[1., .603505575, .132655465, .010620173, .00030967104],
                                                  [.603505575, 1., .603505575, .132655465, .010620173],
                                                  [.132655465, .603505575, 1., .603505575, .132655465],
                                                  [.010620173, .132655465, .603505575, 1., .603505575],
                                                  [.00030967104, .010620173, .132655465, .603505575, 1.]
                                                  ]))

    def test_squared_exponential_kernel_ard_symbolic_call_sx_x_x_bar(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential(length_scales=[1., 1.])

        x = ca.SX.sym('x', 2)
        y = ca.SX.sym('y', 2)
        cov = kernel(x, y)

        self.assertIsInstance(cov, ca.SX)
        for length_scale in kernel.length_scales.SX.elements():
            self.assertTrue(ca.depends_on(cov, length_scale))
        self.assertTrue(ca.depends_on(cov, kernel.signal_variance.SX))
        for xk in x.elements():
            self.assertTrue(ca.depends_on(cov, xk))
        for yk in y.elements():
            self.assertTrue(ca.depends_on(cov, yk))

    def test_squared_exponential_kernel_ard_symbolic_call_sx_x_x_bar_not_all_active(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential(active_dims=[0, 2], length_scales=[1., 1.])

        x = ca.SX.sym('x', 3)
        y = ca.SX.sym('y', 3)
        cov = kernel(x, y)

        self.assertIsInstance(cov, ca.SX)
        for length_scale in kernel.length_scales.SX.elements():
            self.assertTrue(ca.depends_on(cov, length_scale))
        self.assertTrue(ca.depends_on(cov, kernel.signal_variance.SX))
        for k, xk in enumerate(x.elements()):
            if k == 1:
                self.assertFalse(ca.depends_on(cov, xk))
            else:
                self.assertTrue(ca.depends_on(cov, xk))
        for k, yk in enumerate(y.elements()):
            if k == 1:
                self.assertFalse(ca.depends_on(cov, yk))
            else:
                self.assertTrue(ca.depends_on(cov, yk))

    # def test_squared_exponential_kernel_ard_symbolic_call_mx_x_x_bar(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.squared_exponential(length_scales=[1., 1.])
    #
    #     x = ca.MX.sym('x', 2)
    #     y = ca.MX.sym('y', 2)
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x, y)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     for length_scale in kernel.length_scales.MX.elements():
    #         self.assertTrue(ca.depends_on(cov, length_scale))
    #     self.assertTrue(ca.depends_on(cov, kernel.signal_variance.MX))
    #     for xk in x.elements():
    #         self.assertTrue(ca.depends_on(cov, xk))
    #     for yk in y.elements():
    #         self.assertTrue(ca.depends_on(cov, yk))

    # def test_squared_exponential_kernel_ard_symbolic_call_mx_x_x_bar_not_all_active(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.squared_exponential(active_dims=[0, 2], length_scales=[1., 1.])
    #
    #     x = ca.MX.sym('x', 3)
    #     y = ca.MX.sym('y', 3)
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x, y)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     for length_scale in kernel.length_scales.MX.elements():
    #         self.assertTrue(ca.depends_on(cov, length_scale))
    #     self.assertTrue(ca.depends_on(cov, kernel.signal_variance.MX))
    #     for k, xk in enumerate(x.elements()):
    #         if k == 1:
    #             self.assertFalse(ca.depends_on(cov, xk))
    #         else:
    #             self.assertTrue(ca.depends_on(cov, xk))
    #     for k, yk in enumerate(y.elements()):
    #         if k == 1:
    #             self.assertFalse(ca.depends_on(cov, yk))
    #         else:
    #             self.assertTrue(ca.depends_on(cov, yk))

    def test_squared_exponential_kernel_ard_numeric_call_x_x_bar(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential(length_scales=[1., 1.])

        x = np.array([[1., 1.1, 1.2], [1.3, 1.4, 1.5]])
        y = np.array([[1.6, 1.7, 1.8], [1.9, 2., 2.1]])
        cov = kernel(x, y)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_allclose(cov, np.array([[.69767633, .61262639, .52729242],
                                                  [.77880078, .69767633, .61262639],
                                                  [.85214379, .77880078, .69767633]]))

    def test_squared_exponential_kernel_ard_numeric_call_x_x_bar_not_all_active(self) -> None:
        """

        :return:
        """
        kernel = Kernel.squared_exponential(active_dims=[0, 2], length_scales=[1., 1.])

        x = np.array([[1., 1.1, 1.2], [1.3, 1.4, 1.5], [1.6, 1.7, 1.8]])
        y = np.array([[1.9, 2., 2.1], [2.2, 2.3, 2.4], [2.5, 2.6, 2.7]])
        cov = kernel(x, y)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_allclose(cov, np.array([[.44485807, .36787944, .29819728],
                                                  [.52729242, .44485807, .36787944],
                                                  [.61262639, .52729242, .44485807]]))


class TestExponentialKernel(TestCase):
    """"""
    def test_exponential_kernel_no_hyperprior(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential()

        self.assertIsNone(kernel.active_dims)
        self.assertEqual(len(kernel.hyperparameters), 2)
        self.assertEqual(kernel.hyperparameter_names, ['E.length_scales', 'E.signal_variance'])
        self.assertTrue(hasattr(kernel.length_scales, 'log'))
        np.testing.assert_equal(kernel.length_scales.value, np.ones((1, 1)))
        np.testing.assert_equal(kernel.length_scales.log, np.zeros((1, 1)))
        self.assertTrue(hasattr(kernel.signal_variance, 'log'))
        np.testing.assert_equal(kernel.signal_variance.value, np.ones((1, 1)))
        np.testing.assert_equal(kernel.signal_variance.log, np.zeros((1, 1)))

    def test_exponential_kernel_fixed(self) -> None:
        """

        :return:
        """
        # TODO: Change according to test_means.py when first TODO is finished
        kernel = Kernel.exponential()
        kernel.length_scales.fixed = True
        kernel.signal_variance.fixed = True

        self.assertTrue(kernel.length_scales.fixed)
        self.assertTrue(kernel.signal_variance.fixed)

    # def test_exponential_kernel_hyperprior_gaussian(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     # TODO: Create according to test_means.py when first TODO is finished

    def test_exponential_kernel_ard_no_active_dims(self) -> None:
        """

        :return:
        """
        with self.assertRaises(ValueError) as context:
            Kernel.exponential(ard=True)
        self.assertEqual(str(context.exception),
                         "The key word 'ard' can only be set to True if the key word 'active_dims' was supplied")

    def test_exponential_kernel_ard_dimension_mismatch(self) -> None:
        """

        :return:
        """
        with self.assertRaises(ValueError) as context:
            Kernel.exponential(active_dims=[0, 1], length_scales=[1., 1., 1.])
        self.assertEqual(str(context.exception),
                         "Dimension mismatch between 'active_dims' (2) and the number of length_scales (3)")

    def test_exponential_kernel_symbolic_call_sx(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential()

        x = ca.SX.sym('x')
        cov = kernel(x)

        self.assertIsInstance(cov, ca.SX)
        self.assertFalse(ca.depends_on(cov, kernel.length_scales.SX))
        self.assertTrue(ca.depends_on(cov, kernel.signal_variance.SX))
        self.assertFalse(ca.depends_on(cov, x))

    # def test_exponential_kernel_symbolic_call_mx(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.exponential()
    #
    #     x = ca.MX.sym('x')
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     self.assertFalse(ca.depends_on(cov, kernel.length_scales.MX))
    #     self.assertTrue(ca.depends_on(cov, kernel.signal_variance.MX))
    #     self.assertFalse(ca.depends_on(cov, x))

    def test_exponential_kernel_numeric_call(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential()

        x = np.array([[1., 2., 3., 4., 5.]])
        cov = kernel(x)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_allclose(cov, np.array([[1., .36787944, .13533528, .04978707, .01831564],
                                                  [.36787944, 1., .36787944, .13533528, .04978707],
                                                  [.13533528, .36787944, 1., .36787944, .13533528],
                                                  [.04978707, .13533528, .36787944, 1., .36787944],
                                                  [.01831564, .04978707, .13533528, .36787944, 1.]]))

    def test_exponential_kernel_symbolic_call_x_x_bar_wrong_type(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential()

        x = ca.SX.sym('x')
        y = np.array([[2.]])
        # FIXME: Convert to TypeError
        with self.assertRaises(ValueError) as context:
            kernel(x, y)
        self.assertEqual(str(context.exception), "X and X_bar need to have the same type")

    def test_exponential_kernel_symbolic_call_x_x_bar_dimension_mismatch(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential()

        x = ca.SX.sym('x', 2)
        y = ca.SX.sym('y')
        # FIXME: Convert to ValueError
        with self.assertRaises(AssertionError) as context:
            kernel(x, y)
        self.assertEqual(str(context.exception), "X and X_bar do not have the same input space dimensions")

    def test_exponential_kernel_symbolic_call_x_x_bar_sx(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential()

        x = ca.SX.sym('x')
        y = ca.SX.sym('y')
        cov = kernel(x, y)

        self.assertIsInstance(cov, ca.SX)
        self.assertTrue(ca.depends_on(cov, kernel.length_scales.SX))
        self.assertTrue(ca.depends_on(cov, kernel.signal_variance.SX))
        self.assertTrue(ca.depends_on(cov, x))
        self.assertTrue(ca.depends_on(cov, y))

    # def test_exponential_kernel_symbolic_call_x_x_bar_mx(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.exponential()
    #
    #     x = ca.MX.sym('x')
    #     y = ca.MX.sym('y')
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x, y)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     self.assertTrue(ca.depends_on(cov, kernel.length_scales.MX))
    #     self.assertTrue(ca.depends_on(cov, kernel.signal_variance.MX))
    #     self.assertTrue(ca.depends_on(cov, x))
    #     self.assertTrue(ca.depends_on(cov, y))

    def test_exponential_kernel_numeric_call_x_x_bar_wrong_type(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential()

        x = np.array([[2.]])
        y = ca.SX.sym('y')
        # FIXME: Convert to TypeError
        with self.assertRaises(ValueError) as context:
            kernel(x, y)
        self.assertEqual(str(context.exception), "X and X_bar need to have the same type")

    def test_exponential_kernel_numeric_call_x_x_bar_dimension_mismatch(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential()

        x = np.array([[1.], [2.]])
        y = np.array([[1.]])
        # FIXME: Convert to ValueError
        with self.assertRaises(AssertionError) as context:
            kernel(x, y)
        self.assertEqual(str(context.exception), "X and X_bar do not have the same input space dimensions")

    def test_exponential_kernel_numeric_call_x_x_bar(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential()

        x = np.array([[1., 2., 3., 4., 5.]])
        y = np.array([[1., 2., 3., 4., 5.]]) / 2.
        cov = kernel(x, y)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_allclose(
            cov,
            np.array([[.60653066, 1., .60653066, .36787944, .22313016],
                      [.22313016, .36787944, .60653066, 1., .60653066],
                      [.082085, .13533528, .22313016, .36787944, .60653066],
                      [.030197383, .04978707, .082085, .13533528, .22313016],
                      [.011108997, .01831564, .030197383, .04978707, .082085]])
                                   )

    def test_exponential_kernel_ard(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential(active_dims=[0, 1], length_scales=[1., 1.])

        self.assertEqual(kernel.active_dims, [0, 1])
        np.testing.assert_equal(kernel.length_scales.value, np.ones((2, 1)))

        kernel = Kernel.exponential(active_dims=[0, 1, 2], ard=True)

        self.assertEqual(kernel.active_dims, [0, 1, 2])
        np.testing.assert_equal(kernel.length_scales.value, np.ones((3, 1)))

    # def test_exponential_kernel_ard_call_dimension_mismatch(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     # TODO: Create similar test for means
    #     kernel = Kernel.exponential(active_dims=[0, 1], length_scales=[1., 1.])
    #
    #     x = ca.SX.sym('x')
    #     # FIXME: This will result in another error that could be unclear to the user. We should probably catch it and
    #     #  return a more informative error message.
    #     cov = kernel(x)

    def test_exponential_kernel_ard_call_dimension_mismatch(self) -> None:
        """

        :return:
        """
        # TODO: Create similar test for means
        kernel = Kernel.exponential(length_scales=[1., 1.])

        x = ca.SX.sym('x')
        with self.assertRaises(ValueError) as context:
            kernel(x)
        self.assertEqual(str(context.exception), "Length scales vector dimension does not equal input space dimension.")

    def test_exponential_kernel_ard_symbolic_call_sx(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential(length_scales=[1., 1.])

        x = ca.SX.sym('x', 2)
        cov = kernel(x)

        self.assertIsInstance(cov, ca.SX)
        self.assertFalse(ca.depends_on(cov, kernel.length_scales.SX))
        self.assertTrue(ca.depends_on(cov, kernel.signal_variance.SX))
        self.assertFalse(ca.depends_on(cov, x))

    def test_exponential_kernel_ard_symbolic_call_sx_not_all_active(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential(active_dims=[0, 2], length_scales=[1., 1.])

        x = ca.SX.sym('x', 3)
        cov = kernel(x)

        self.assertIsInstance(cov, ca.SX)
        self.assertFalse(ca.depends_on(cov, kernel.length_scales.SX))
        self.assertTrue(ca.depends_on(cov, kernel.signal_variance.SX))
        self.assertFalse(ca.depends_on(cov, x))

    # def test_exponential_kernel_ard_symbolic_call_mx(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.exponential(length_scales=[1., 1.])
    #
    #     x = ca.MX.sym('x', 2)
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     self.assertFalse(ca.depends_on(cov, kernel.length_scales.MX))
    #     self.assertTrue(ca.depends_on(cov, kernel.signal_variance.MX))
    #     self.assertFalse(ca.depends_on(cov, x))

    # def test_exponential_kernel_ard_symbolic_call_mx_not_all_active(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.exponential(active_dims=[0, 2], length_scales=[1., 1.])
    #
    #     x = ca.MX.sym('x', 3)
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     self.assertFalse(ca.depends_on(cov, kernel.length_scales.MX))
    #     self.assertTrue(ca.depends_on(cov, kernel.signal_variance.MX))
    #     self.assertFalse(ca.depends_on(cov, x))

    def test_exponential_kernel_ard_numeric_call(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential(length_scales=[1., 1.])

        x = np.array([[1., 2., 3., 4., 5.], [.1, .2, .3, .4, .5]])
        cov = kernel(x)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_allclose(cov, np.array([[1., .36604919, .13399201, .04904767, .017953858],
                                                  [.36604919, 1., .36604919, .13399201, .04904767],
                                                  [.13399201, .36604919, 1., .36604919, .13399201],
                                                  [.04904767, .13399201, .36604919, 1., .36604919],
                                                  [.017953858, .04904767, .13399201, .36604919, 1.]
                                                  ]))

    def test_exponential_kernel_ard_numeric_call_not_all_active(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential(active_dims=[0, 2], length_scales=[1., 1.])

        x = np.array([[1., 2., 3., 4., 5.], [6., 7., 8., 9., 0.], [.1, .2, .3, .4, .5]])
        cov = kernel(x)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_allclose(cov, np.array([[1., .36604919, .13399201, .04904767, .017953858],
                                                  [.36604919, 1., .36604919, .13399201, .04904767],
                                                  [.13399201, .36604919, 1., .36604919, .13399201],
                                                  [.04904767, .13399201, .36604919, 1., .36604919],
                                                  [.017953858, .04904767, .13399201, .36604919, 1.]
                                                  ]))

    def test_exponential_kernel_ard_symbolic_call_sx_x_x_bar(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential(length_scales=[1., 1.])

        x = ca.SX.sym('x', 2)
        y = ca.SX.sym('y', 2)
        cov = kernel(x, y)

        self.assertIsInstance(cov, ca.SX)
        for length_scale in kernel.length_scales.SX.elements():
            self.assertTrue(ca.depends_on(cov, length_scale))
        self.assertTrue(ca.depends_on(cov, kernel.signal_variance.SX))
        for xk in x.elements():
            self.assertTrue(ca.depends_on(cov, xk))
        for yk in y.elements():
            self.assertTrue(ca.depends_on(cov, yk))

    def test_exponential_kernel_ard_symbolic_call_sx_x_x_bar_not_all_active(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential(active_dims=[0, 2], length_scales=[1., 1.])

        x = ca.SX.sym('x', 3)
        y = ca.SX.sym('y', 3)
        cov = kernel(x, y)

        self.assertIsInstance(cov, ca.SX)
        for length_scale in kernel.length_scales.SX.elements():
            self.assertTrue(ca.depends_on(cov, length_scale))
        self.assertTrue(ca.depends_on(cov, kernel.signal_variance.SX))
        for k, xk in enumerate(x.elements()):
            if k == 1:
                self.assertFalse(ca.depends_on(cov, xk))
            else:
                self.assertTrue(ca.depends_on(cov, xk))
        for k, yk in enumerate(y.elements()):
            if k == 1:
                self.assertFalse(ca.depends_on(cov, yk))
            else:
                self.assertTrue(ca.depends_on(cov, yk))

    # def test_exponential_kernel_ard_symbolic_call_mx_x_x_bar(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.exponential(length_scales=[1., 1.])
    #
    #     x = ca.MX.sym('x', 2)
    #     y = ca.MX.sym('y', 2)
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x, y)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     for length_scale in kernel.length_scales.MX.elements():
    #         self.assertTrue(ca.depends_on(cov, length_scale))
    #     self.assertTrue(ca.depends_on(cov, kernel.signal_variance.MX))
    #     for xk in x.elements():
    #         self.assertTrue(ca.depends_on(cov, xk))
    #     for yk in y.elements():
    #         self.assertTrue(ca.depends_on(cov, yk))

    # def test_exponential_kernel_ard_symbolic_call_mx_x_x_bar_not_all_active(self) -> None:
    #     """
    #
    #     :return:
    #     """
    #     kernel = Kernel.exponential(active_dims=[0, 2], length_scales=[1., 1.])
    #
    #     x = ca.MX.sym('x', 3)
    #     y = ca.MX.sym('y', 3)
    #     # FIXME: This will result in a mixture of SX and MX (should we remove MX completely?)
    #     cov = kernel(x, y)
    #
    #     self.assertIsInstance(cov, ca.MX)
    #     for length_scale in kernel.length_scales.MX.elements():
    #         self.assertTrue(ca.depends_on(cov, length_scale))
    #     self.assertTrue(ca.depends_on(cov, kernel.signal_variance.MX))
    #     for k, xk in enumerate(x.elements()):
    #         if k == 1:
    #             self.assertFalse(ca.depends_on(cov, xk))
    #         else:
    #             self.assertTrue(ca.depends_on(cov, xk))
    #     for k, yk in enumerate(y.elements()):
    #         if k == 1:
    #             self.assertFalse(ca.depends_on(cov, yk))
    #         else:
    #             self.assertTrue(ca.depends_on(cov, yk))

    def test_exponential_kernel_ard_numeric_call_x_x_bar(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential(length_scales=[1., 1.])

        x = np.array([[1., 1.1, 1.2], [1.3, 1.4, 1.5]])
        y = np.array([[1.6, 1.7, 1.8], [1.9, 2., 2.1]])
        cov = kernel(x, y)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_allclose(cov, np.array([[.42804449, .37159546, .32259073],
                                                  [.49306869, .42804449, .37159546],
                                                  [.56797071, .49306869, .42804449]]))

    def test_exponential_kernel_ard_numeric_call_x_x_bar_not_all_active(self) -> None:
        """

        :return:
        """
        kernel = Kernel.exponential(active_dims=[0, 2], length_scales=[1., 1.])

        x = np.array([[1., 1.1, 1.2], [1.3, 1.4, 1.5], [1.6, 1.7, 1.8]])
        y = np.array([[1.9, 2., 2.1], [2.2, 2.3, 2.4], [2.5, 2.6, 2.7]])
        cov = kernel(x, y)

        self.assertIsInstance(cov, np.ndarray)
        np.testing.assert_allclose(cov, np.array([[.28004858, .24311673, .21105534],
                                                  [.32259073, .28004858, .24311673],
                                                  [.37159546, .32259073, .28004858]]))