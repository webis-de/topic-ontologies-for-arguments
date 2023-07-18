import sys
import pandas

frame_filenames = sys.argv[1:-2]
k = int(sys.argv[-2])
output_file = sys.argv[-1]

group_columns = ["method", "argument.id"]

def read_frames(filenames):
    return [pandas.read_csv(filename, dtype={"argument.id":object,"topic.id":object}) for filename in filenames]

def get_top_k(frame, k):
    return frame.sort_values("score", ascending=False).head(k)

def get_top_k_each(frames, k):
    return [get_top_k(frame, k) for frame in frames]

def get_top_k_each_group(base_frame, group_columns, k):
    sub_frame_indices = base_frame.groupby(group_columns).groups
    sub_frames = [base_frame.loc[indices] for indices in sub_frame_indices.values()]
    return get_top_k_each(sub_frames, k)

frames = read_frames(frame_filenames)
top_k_frames = [pandas.concat(get_top_k_each_group(frame, ["method", "argument.id"], k)) for frame in frames]
pandas.concat(top_k_frames, ignore_index=True).to_csv(output_file, index=False)

