import os
import os.path

for dirpath, dirnames, filenames in os.walk('./Dataset'):
    for filename in [f for f in filenames if f.endswith('.txt')]:
        print(os.path.join(dirpath, filename))

