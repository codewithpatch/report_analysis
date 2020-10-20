import logging

from pipelines.exception_records import ExceptionRecordsPipeline
from pipelines.matched import MatchedPipeline
from pipelines.mismatch import MismatchPipeline
from pipelines.mx import MissingInMXPipeline
from pipelines.saa import MissingInSaaPipeline
from pipelines.unclassified_exception import UnclassifiedExceptionPipeline
from settings import REPORTS, RUN_ALL

if __name__ == '__main__':
    pipes = [
        ExceptionRecordsPipeline,
        MismatchPipeline,
        UnclassifiedExceptionPipeline,
        MatchedPipeline,
        MissingInSaaPipeline,
        MissingInMXPipeline
    ]
    # reader = ReportReader('ExceptionRecords')

    for PipeClass in pipes:
        if not RUN_ALL and not REPORTS[PipeClass.report]:
            logging.info(f"Skipping Report analysis for {PipeClass.report}...")
            continue

        logging.info(f"Running Report analysis for {PipeClass.report}...")

        pipeline = PipeClass()
        pipeline.process_df()
        pipeline.end_process()
