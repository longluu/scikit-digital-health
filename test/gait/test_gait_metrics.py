"""
Testing of gait metrics

Lukas Adamowicz
2020, Pfizer DMTI
"""
import pytest
import numpy as np
from numpy import nan
import h5py

from ..base_conftest import *

from skimu.gait.gait_metrics import *
from skimu.gait.gait_metrics.gait_metrics import _autocovariancefunction, _autocovariance


class BaseTestMetric:
    @classmethod
    def setup_class(cls):
        cls.metric = None

        cls.num_nan = 2
        cls.res_bout1 = None

        cls.event_metric = True

    def test(self, sample_gait, sample_gait_aux):
        self.metric.predict(1/50, 1.0, sample_gait, sample_gait_aux)

        assert np.isnan(sample_gait[self.metric.k_]).sum() == 2 * self.num_nan

        if self.event_metric:
            assert np.allclose(
                sample_gait[self.metric.k_][:5], sample_gait[self.metric.k_][5:],
                equal_nan=True
            )
        else:
            assert all(sample_gait[self.metric.k_] == sample_gait[self.metric.k_][0])

        if self.res_bout1 is not None:
            assert np.allclose(sample_gait[self.metric.k_][:5], self.res_bout1, equal_nan=True)


"""
gait = {
    'IC': np.tile(np.array([10, 35, 62, 86, 111]), 2),
    'FC opp foot': np.tile(np.array([15, 41, 68, 90, 116]), 2),
    'FC': np.tile(np.array([40, 65, 90, 115, 140]), 2),
    'delta h': np.tile(np.array([0.05, 0.055, 0.05, 0.045, nan]), 2),
    'Bout N': np.repeat([1, 2], 5)
}
"""


class TestStrideTime(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = StrideTime()

        cls.num_nan = 2
        cls.res_bout1 = np.array([52, 51, 49, nan, nan]) / 50


class TestStanceTime(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = StanceTime()

        cls.num_nan = 0
        cls.res_bout1 = np.array([30, 30, 28, 29, 29]) / 50


class TestSwingTime(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = SwingTime()

        cls.num_nan = 2
        cls.res_bout1 = np.array([22, 21, 21, nan, nan]) / 50


class TestStepTime(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = StepTime()

        cls.num_nan = 1
        cls.res_bout1 = np.array([25, 27, 24, 25, nan]) / 50


class TestInitialDoubleSupport(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = InitialDoubleSupport()

        cls.num_nan = 0
        cls.res_bout1 = np.array([5, 6, 6, 4, 5]) / 50


class TestTerminalDoubleSupport(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = TerminalDoubleSupport()

        cls.num_nan = 1
        cls.res_bout1 = np.array([6, 6, 4, 5, nan]) / 50


class TestDoubleSupport(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = DoubleSupport()

        cls.num_nan = 1
        cls.res_bout1 = np.array([11, 12, 10, 9, nan]) / 50


class TestSingleSupport(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = SingleSupport()

        cls.num_nan = 1
        cls.res_bout1 = np.array([20, 21, 18, 21, nan]) / 50


class TestStepLength(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = StepLength()

        cls.num_nan = 1
        cls.res_bout1 = 2 * np.sqrt(
            2 * np.array([0.05, 0.055, 0.05, 0.045, nan])
            - np.array([0.05, 0.055, 0.05, 0.045, nan])**2
        )

    def test_no_leg_length(self, sample_gait):
        self.metric.predict(1/50, None, sample_gait, None)

        assert np.isnan(sample_gait[self.metric.k_]).sum() == 10


class TestStrideLength(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = StrideLength()

        cls.num_nan = 2

        tmp = 2 * np.sqrt(
            2 * np.array([0.05, 0.055, 0.05, 0.045, nan])
            - np.array([0.05, 0.055, 0.05, 0.045, nan])**2
        )
        cls.res_bout1 = tmp
        cls.res_bout1[:-1] += tmp[1:]

    def test_no_leg_length(self, sample_gait):
        self.metric.predict(1/50, None, sample_gait, None)

        assert np.isnan(sample_gait[self.metric.k_]).sum() == 10


class TestGaitSpeed(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = GaitSpeed()

        cls.num_nan = 2

        tmp_l = 2 * np.sqrt(
            2 * np.array([0.05, 0.055, 0.05, 0.045, nan])
            - np.array([0.05, 0.055, 0.05, 0.045, nan])**2
        )
        tmp_t = np.array([52, 51, 49, nan, nan]) / 50

        cls.res_bout1 = tmp_l
        cls.res_bout1[:-1] += tmp_l[1:]
        cls.res_bout1 /= tmp_t

    def test_no_leg_length(self, sample_gait):
        self.metric.predict(1/50, None, sample_gait, None)

        assert np.isnan(sample_gait[self.metric.k_]).sum() == 10


class TestCadence(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = Cadence()

        cls.num_nan = 1
        cls.res_bout1 = 60 * 50 / np.array([25, 27, 24, 25, nan])


# TODO should probably check actual values here not just through running Gait
class TestIntraStrideCovarianceV(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = IntraStrideCovarianceV()

        cls.num_nan = 2


# TODO should probably check actual values here not just through running Gait
class TestIntraStepCovarianceV(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = IntraStepCovarianceV()
        cls.num_nan = 1


# TODO should probably check actual values here not just through running Gait
class TestHarmonicRatioV(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = HarmonicRatioV()
        cls.num_nan = 2


# TODO should probably check actual values here not just through running Gait
class TestStrideSPARC(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = StrideSPARC()
        cls.num_nan = 2


# TODO should probably check actual values here not just through running Gait
class TestPhaseCoordinationIndex(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = PhaseCoordinationIndex()
        cls.num_nan = 0

        cls.event_metric = False


# TODO should probably check actual values here not just through running Gait
class TestGaitSymmetryIndex(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = GaitSymmetryIndex()
        cls.num_nan = 0

        cls.event_metric = False


# TODO should probably check actual values here not just through running Gait
class TestStrideRegularityV(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = StrideRegularityV()
        cls.num_nan = 0

        cls.event_metric = False


# TODO should probably check actual values here not just through running Gait
class TestStepRegularityV(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = StepRegularityV()
        cls.num_nan = 0

        cls.event_metric = False


# TODO should probably check actual values here not just through running Gait
class TestAutocovarianceSymmetryV(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = AutocovarianceSymmetryV()
        cls.num_nan = 0

        cls.event_metric = False


# TODO should probably check actual values here not just through running Gait
class TestRegularityIndexV(BaseTestMetric):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        cls.metric = RegularityIndexV()
        cls.num_nan = 0

        cls.event_metric = False
