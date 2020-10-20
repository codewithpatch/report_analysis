from pipelines.exception_records import ExceptionRecordsPipeline
from pipelines.matched import MatchedPipeline
from pipelines.mismatch import MismatchPipeline
from pipelines.mx import MissingInMXPipeline
from pipelines.saa import MissingInSaaPipeline
from pipelines.unclassified_exception import UnclassifiedExceptionPipeline

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
        if PipeClass.report != 'MissingInMX':
            continue

        pipeline = PipeClass()
        pipeline.process_df()
        pipeline.end_process()
