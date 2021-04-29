from typing import Callable, Optional

import pysam

from .fastq import Fastq, Read


class BamError(Exception):
    pass


def apply_bam(
    bam_path: str,
    apply_func: Callable[[pysam.AlignedSegment],
                         Optional[pysam.AlignedSegment]],
    out_path: str,
    n_threads: int = 1,
):
    """Apply an arbitrary function to every read in a BAM. Reads for which the
    function returns `None` are not written to the output BAM.
    """
    with pysam.AlignmentFile(bam_path, 'rb', threads=n_threads,
                             check_sq=False) as f_in:
        with pysam.AlignmentFile(out_path, 'wb', template=f_in,
                                 threads=n_threads) as f_out:
            for read in f_in.fetch(until_eof=True):
                result = apply_func(read)
                if result is not None:
                    f_out.write(read)


def tag_bam_with_fastq(
    bam_path: str,
    fastq_path: str,
    tag_func: Callable[[Read], dict],
    out_path: str,
    check_name: bool = True,
    n_threads: int = 1,
):
    """Add tags to BAM entries using sequences from a FASTQ file.
    """
    tags = {read.name: tag_func(read) for read in Fastq(fastq_path).reads()}

    def apply_func(al: pysam.AlignedSegment):
        if al.query_name in tags:
            al.set_tags(list(tags[al.query_name].items()))
        elif check_name:
            raise BamError(f'Missing read `{al.query_name}` in FASTQ')
        return al

    return apply_bam(bam_path, apply_func, out_path, n_threads)


def filter_bam(
    bam_path: str,
    filter_func: Callable[[pysam.AlignedSegment], bool],
    out_path: str,
    n_threads: int = 1,
):
    """Filter a BAM by applying the given function to each pysam.AlignedSegment
    object. When the function returns False, the read is not written to the output
    BAM.
    """
    return apply_bam(
        bam_path, lambda al: None
        if filter_func(al) is False else al, out_path, n_threads
    )