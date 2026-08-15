import json


import json
import os


class RecursiveJsonGenerator:

    def __init__(
            self,
            depth=5,
            members_per_object=5,
            array_size=5,
            recursive_ratio=0.9
    ):
        self.depth = depth
        self.members_per_object = members_per_object
        self.array_size = array_size
        self.recursive_ratio = recursive_ratio

        self.counter = 0


    def new_key(self):
        self.counter += 1
        return f"key_{self.counter}"


    # V -> value()
    def value(self):

        return "value"



    # O -> object(M*)
    def object(self, depth):

        if depth == 0:
            return self.value()


        obj = {}

        for _ in range(self.members_per_object):

            obj[self.new_key()] = self.member(depth-1)

        return obj



    # A -> array(O*)
    def array(self, depth):

        if depth == 0:
            return []


        return [
            self.object(depth-1)
            for _ in range(self.array_size)
        ]



    # M -> object | array | value
    def member(self, depth):

        if depth == 0:
            return self.value()


        # force recursion most of the time
        import random

        if random.random() < self.recursive_ratio:

            if random.random() < 0.5:
                return self.object(depth)

            else:
                return self.array(depth)

        else:

            return self.value()



    # D -> document(O)
    def document(self):

        self.counter = 0

        return {
            "document":
                self.object(self.depth)
        }


def generate_file(
        filename,
        depth,
        members,
        arrays
):

    generator = RecursiveJsonGenerator(
        depth,
        members,
        arrays
    )


    data = generator.document()


    with open(filename,"w") as f:

        json.dump(
            data,
            f
        )


    size = os.path.getsize(filename)


    print(
        filename,
        size,
        "bytes"
    )

if __name__ == "__main__":
    os.makedirs(
        "json_dataset",
        exist_ok=True
    )


    tests = [

        ("small.json",5,5,5),

        ("medium.json",8,5,5),

        ("large.json",10,5,5),

        ("huge.json",11,5,5),

    ]


    for name,d,m,a in tests:

        generate_file(
            "json_dataset/"+name,
            d,
            m,
            a
        )

 