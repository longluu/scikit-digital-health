from tempfile import NamedTemporaryFile

import pytest
from numpy import allclose, random
import pandas as pd

from skimu.features import *
from skimu.features.core import NoFeaturesError, NotAFeatureError


class TestBank:
    def set_up(self):
        bank = Bank()

        bank.add([
            Mean(),
            Range()[[0, 2]],
            JerkMetric(),
            Range()[1]
        ])

        return bank

    def test_2d_ndarray(self, fs, acc, bank_2d_truth):
        feat_bank = self.set_up()

        _ = feat_bank.compute(acc, 20.0, columns=['x', 'y', 'z'], axis=0)
        pred = feat_bank.compute(acc, 20.0, axis=0)  # run 2x to catch any bugs with multiple runs on same data

        # check that values match truth values (ie doing correct computations)
        assert allclose(pred, bank_2d_truth)

    def test_dataframe(self, fs, acc, bank_2d_truth):
        feat_bank = self.set_up()

        acc_df = pd.DataFrame(data=acc, columns=['x', 'y', 'z'])

        _ = feat_bank.compute(acc_df, 20.0)
        pred, cols = feat_bank.compute(acc_df, 20.0)  # run 2x to catch any bugs with multiple runs on same data

        # check that values match truth values (ie doing correct computations)
        assert allclose(pred, bank_2d_truth)

    def test_save_load(self, fs, acc, bank_2d_truth):
        feat_bank = self.set_up()

        ntf = NamedTemporaryFile('r+')

        feat_bank.save(ntf.name)

        feat_bank = None
        feat_bank = Bank()
        feat_bank.load(ntf.name)
        ntf.close()

        pred = feat_bank.compute(acc, 20.0, axis=0)

        assert allclose(pred, bank_2d_truth)

    # def test_no_features_error(self):
    #     feat_bank = Bank()
    #
    #     with pytest.raises(NoFeaturesError):
    #         feat_bank.compute(None, None)

    def test_columns_size_error(self):
        feat_bank = self.set_up()

        with pytest.raises(ValueError):
            feat_bank.compute(random.rand(150, 10, 3), 50.0, columns=['x', 'y'])

    @pytest.mark.parametrize('non_feat', (lambda x: x**2, 5))
    def test_non_feature_add_error(self, non_feat):
        feat_bank = Bank()

        with pytest.raises(NotAFeatureError):
            feat_bank.add(non_feat)

