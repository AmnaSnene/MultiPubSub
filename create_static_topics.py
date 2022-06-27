import sys
# create n topic to publish on / subscribe to.
nb_static_topic = int(sys.argv[1])
f = open("topics_file", "a")
for i in range(nb_static_topic):
    f.write(f"topic{i}\n")
