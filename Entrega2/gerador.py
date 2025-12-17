import random

def generate_input(
    num_vertices=7,
    num_trucks=4,
    truck_min=2,
    truck_max=4,
    num_edges=10
):
    assert 1 <= truck_min <= truck_max <= num_trucks

    # Create a random topological order
    topo = list(range(1, num_vertices + 1))
    random.shuffle(topo)

    # All possible DAG-safe edges
    possible_edges = []
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            possible_edges.append((topo[i], topo[j]))

    if num_edges > len(possible_edges):
        raise ValueError("Too many edges for a DAG")

    edges = random.sample(possible_edges, num_edges)

    # Output
    print(num_vertices)
    print(num_trucks)
    print(truck_min, truck_max)
    print(num_edges)
    for a, b in edges:
        print(a, b)


# Example
if __name__ == "__main__":
    generate_input(
        num_vertices=10000,
        num_trucks=123456789,
        truck_min=1,
        truck_max=23,
        num_edges=123410 #kid named num
    )
