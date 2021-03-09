import argparse

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--query', '-q',
        type=str,
        required=True,
        help='query sequence to align w.r.t reference')
    parser.add_argument(
        '--reference', '-r',
        type=str,
        required=True,
        help='reference sequence for the alignment')
    parser.add_argument(
        '--match', '-m',
        default=1,
        type=int,
        help='score for a match')
    parser.add_argument(
        '--mismatch', '-mm',
        default= -1,
        type=int,
        help='score for a mismatch')
    parser.add_argument(
        '--gap', '-g',
        default= -2,
        type=int,
        help='score for a gap')

    return parser.parse_args()