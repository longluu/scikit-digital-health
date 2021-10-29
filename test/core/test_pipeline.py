import json
from tempfile import TemporaryDirectory
from pathlib import Path

import pytest

from skdh.pipeline import Pipeline, NotAProcessError, ProcessNotFoundError
from skdh.gait import Gait
from skdh import __version__ as skdh_vers


class TestPipeline:
    @staticmethod
    def setup_lgr():
        class Lgr:
            msgs = []

            def info(self, msg):
                self.msgs.append(msg)

        return Lgr()

    def test_run(self, testprocess, testprocess2):
        p = Pipeline()

        tp1 = testprocess(kw1=1)
        tp1.logger = self.setup_lgr()
        tp2 = testprocess2(kwa=5)
        tp2.logger = self.setup_lgr()

        p.add(tp1)
        p.add(tp2)

        res = p.run()

        assert "kw1=1" in tp1.logger.msgs
        assert "kwa=5" in tp2.logger.msgs

        exp_res = {"TestProcess": {"kw1": 1}, "TestProcess2": {"kwa": 5}}

        assert res == exp_res

    def test_str_repr(self, testprocess):
        p = Pipeline()

        assert repr(p) == "IMUAnalysisPipeline[\n]"

        p.add(testprocess(kw1=2))
        p.add(testprocess(kw1=1))

        assert str(p) == "IMUAnalysisPipeline"
        assert (
            repr(p)
            == "IMUAnalysisPipeline[\n\tTestProcess(kw1=2),\n\tTestProcess(kw1=1),\n]"
        )

    def test_add(self, testprocess):
        p = Pipeline()

        tp = testprocess(kw1=500)
        p.add(tp, save_file="test_saver.csv")

        assert p._steps == [testprocess(kw1=500)]
        assert tp._in_pipeline
        assert tp.pipe_save_file == "test_saver.csv"

        with pytest.raises(NotAProcessError):
            p.add(list())

    def test_save(self, testprocess):
        p = Pipeline()

        tp = testprocess(kw1=2)
        # overwrite this for saving
        tp.__class__.__module__ = "skdh.test.testmodule"

        p.add(tp)

        with TemporaryDirectory() as tdir:
            fname = Path(tdir) / "file.json"

            p.save(str(fname))
            with fname.open() as f:
                res = json.load(f)

        exp = {
            "Steps": [
                {
                    "TestProcess": {
                        "package": "skdh",
                        "module": "test.testmodule",
                        "parameters": {"kw1": 2},
                        "save_file": None,
                        "plot_file": None,
                    }
                }
            ],
            "Version": skdh_vers,
        }

        assert res == exp

    def test_load_through_init(self, dummy_pipeline):
        with TemporaryDirectory() as tdir:
            fname = Path(tdir) / "file.json"

            with fname.open(mode="w") as f:
                json.dump(dummy_pipeline, f)

            with pytest.warns(UserWarning):
                p = Pipeline(str(fname))

        assert p._steps == [Gait()]

    def test_load_function(self, dummy_pipeline):
        p = Pipeline()

        with TemporaryDirectory() as tdir:
            fname = Path(tdir) / "file.json"

            with fname.open(mode="w") as f:
                # save only the steps to trigger version warning
                json.dump(dummy_pipeline["Steps"], f)

            with pytest.warns(
                UserWarning, match="Pipeline created by an unknown older version"
            ):
                p.load(str(fname))

        assert p._steps == [Gait()]

    def test_load_version_warning(self, dummy_pipeline):
        p = Pipeline()
        p._min_vers = "100.0.0"

        with TemporaryDirectory() as tdir:
            fname = Path(tdir) / "file.json"

            with fname.open(mode="w") as f:
                json.dump(dummy_pipeline, f)

            with pytest.warns(
                UserWarning, match="Pipeline was created by an older version of skdh"
            ):
                p.load(str(fname))