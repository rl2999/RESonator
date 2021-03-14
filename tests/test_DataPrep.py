import resonator.data.DataIO as ld
from resonator.data.DataPrep import DataPrep
import pandas as pd
from pathlib import Path
import logging


class TestLMSPrep:
    """
    Unit tests for preparing the LMS data
    """

    TARGET_COLUMNS = [
        "International Status",
        "Last Name",
        "First Name",
        "City",
        "Primary Phone",
        "Discipline",
        "Job Title",
        "Street Address",
        "State/Province",
        "Postal Code",
        "Email",
        "Government Level",
    ]

    def test_data_lms(self):
        """Should properly subset the fields"""
        test_users = ["jld2225"]
        loader = ld.DataIO()
        lms_data = loader.load_file_disk(Path("tests/sampledata/lms_sample.csv"))
        output = DataPrep.prep_data_lms(
            input_lms=lms_data,
            course="Preparedness Actions to Promote Economic Resilience and Recovery  (#10268)",
            remove_users=test_users,
        )

        target_columns = pd.Index(
            data=self.TARGET_COLUMNS,
            dtype="object",
        )
        # Check if
        assert (
            output.columns.array == target_columns.array
        ), "Output columns don't match expected"
        assert isinstance(output, pd.DataFrame), "output not a DataFrame"


class TestEvalPrep:
    """
    Unit tests for preparing the LMS data
    """

    def test_data_eval(self):
        """Should properly subset the fields"""
        loader = ld.DataIO()
        lms_data = loader.load_file_disk(Path("tests/sampledata/qualtrics_output.xlsx"))
        output = DataPrep.prep_data_eval(lms_data)
        assert output.shape[1] == 27, "Output should have 27 columns"
        assert isinstance(output, pd.DataFrame), "Output should be a DataFrame"


class TestDataPrepSchedule:
    """
    Unit test for successfully generating schedule XML data
    """

    def test_training_provider(self):
        # tpid
        # tpphone
        # tpemail
        pass

    def test_schedule(self):
        pass


class TestDataPrepSubmission:
    """
    Unit test for generating final RES submission.xml
    """

    def test_submission(self):
        pass
