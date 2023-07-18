# coding=utf-8

import argparse
import pandas

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", type=argparse.FileType('r'), nargs="+", help="One or more CSV files that contain the following columns: 'document.id', 'topic.id', 'method', and 'score'.")
    parser.add_argument("--k", default=10, type=int, required=False, help="The maximum number of topic suggestions to get for each document and method. If more suggestions exist, the ones with the highest 'score' are used. Default is 10.")
    parser.add_argument("--output-file", dest="output_file", default=None, type=argparse.FileType('w'), required=True, help="The output will be written to this file in the same CSV format.")
    return parser.parse_args()

def read_frames(args):
    return [pandas.read_csv(filename, dtype={"document.id":str,"topic.id":str}) for filename in args.files]

def get_top_k(frame, k):
    return frame.sort_values("score", ascending=False).head(k)

def get_top_k_each(frames, k):
    return [get_top_k(frame, k) for frame in frames]

def get_top_k_each_group(base_frame, group_columns, k):
    sub_frame_indices = base_frame.groupby(group_columns).groups
    sub_frames = [base_frame.loc[indices] for indices in sub_frame_indices.values()]
    return get_top_k_each(sub_frames, k)


group_columns = ["method", "document.id"]
args = parse_args()

frames = read_frames(args)

top_k_frames = [pandas.concat(get_top_k_each_group(frame, group_columns, args.k)) for frame in frames]
pandas.concat(top_k_frames, ignore_index=True).to_csv(args.output_file, index=False)

