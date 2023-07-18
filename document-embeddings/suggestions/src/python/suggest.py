import sys
import numpy

def read_ids(filename):
    with open(filename, "r") as ids_file:
        return [line.strip("\n") for line in ids_file.readlines()]

def parse_embedding(line):
    parsed = numpy.fromstring(line.strip("[]"), dtype=float, sep=",")
    return parsed

def parse_embeddings(lines):
    return numpy.array([parse_embedding(line) for line in lines])

def read_embeddings(filename):
    with open(filename, "r") as embeddings_file:
        return parse_embeddings(embeddings_file.readlines())

def suggest(argument_ids, argument_embeddings, topic_ids, topic_embeddings, method_name):
    argument_norms = numpy.linalg.norm(argument_embeddings, axis=1)
    topic_norms = numpy.linalg.norm(topic_embeddings, axis=1)
    scores = numpy.matmul(argument_embeddings, numpy.transpose(topic_embeddings))
    for i in range(len(scores)):
        for j in range(len(scores[i])):
            norm = (argument_norms[i] * topic_norms[j])
            score = 0
            if norm != 0:
                score = scores[i][j] / norm
            print("{},{},{},{}".format(argument_ids[i], topic_ids[j], method_name, score))

argument_ids = read_ids(sys.argv[1])
argument_embeddings = read_embeddings(sys.argv[2])
topic_ids = read_ids(sys.argv[3])
topic_embeddings = read_embeddings(sys.argv[4])
method_name = sys.argv[5]

print("argument.id,topic.id,method,score")
suggest(argument_ids, argument_embeddings, topic_ids, topic_embeddings, method_name)

