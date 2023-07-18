import sys
import pandas

frame_filename = sys.argv[1]
valid_topic_ids_filename = sys.argv[2]
output_filename = sys.argv[3]

group_columns = ["method", "argument.id"]

def read_frame(filename):
    return pandas.read_csv(filename, dtype={"argument.id":object,"topic.id":object})

def read_valid_topic_ids(valid_topic_ids_filename):
    with open(valid_topic_ids_filename, "r") as ifile:
        return set(ifile.read().splitlines())

def filter_rows(frame, valid_topic_ids):
    valid_rows = [topic_id in valid_topic_ids for topic_id in frame['topic.id'].values]
    return frame[valid_rows]

frame = read_frame(frame_filename)
valid_topic_ids = read_valid_topic_ids(valid_topic_ids_filename)
frame = filter_rows(frame, valid_topic_ids)
frame.to_csv(output_filename, index=False)

