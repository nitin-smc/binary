import os
import glob
import random

def run(path, limit=150000):
    annotationDir = path.rstrip("/")
    os.makedirs(annotationDir, exist_ok=True)

    # clear directory
    for i in glob.glob(annotationDir+"/*.txt"):
        os.remove(i)

    # generate random imbalanced class distribution
    distribution = [0.60, 0.02, 0.10, 0.23, 0.05]
    random.shuffle(distribution)
    classes = dict(zip(["car", "van", "motorcycle", "truck", "bus"], distribution))
    classes = {k:v*int(limit) for (k,v) in classes.items()}
    random.shuffle(distribution)

    # generate files in first loop while skipping some
    idx = 0
    skipped = {}

    def generateAnnotation(label, path, mode="w"):
        with open(path, mode) as f:
            f.write("{} 0.00 0 0.00 {} {} {} {} 0.00 0.00 0.00 0.00 0.00 0.00 0.00\n".format(
                name,
                random.randint(1, 100),
                random.randint(1, 100),
                random.randint(1, 100),
                random.randint(1, 100)
            ))

    for name, qty in classes.items():
        skip = random.choice([0.01, 0.02, 0.05, 0.001])
        skip, left = int(skip*qty), int((1-skip)*qty)
        skipped[name] = skip
        for i in range(left):
            generateAnnotation(name, os.path.join(annotationDir, "SAMPLE%s.txt"%idx), mode="w")
            idx += 1

    # mix skipped files annotation into already generated files
    annotations = glob.glob(annotationDir+"/*.txt")
    while sum(skipped.values()):
        # class name which will be mixed
        name = random.choice(list(skipped.keys()))
        random_file = random.choice(annotations)
        
        if skipped[name] > 0:
            # mix this class annotation to some other file
            generateAnnotation(name, random_file, mode="a")

            # decrement class name annotation count
            skipped[name] -= 1
