CREATE TABLE Node(
    NAME VARCHAR PRIMARY KEY NOT NULL,
    CPU int,
    Memory int
);

CREATE TABLE Edge(
    from_node VARCHAR NOT NULL,
    to_node VARCHAR NOT NULL,
    CONSTRAINT fk_from_node FOREIGN KEY(from_node) REFERENCES node(name),
    CONSTRAINT fk_to_node FOREIGN KEY(to_node) REFERENCES node(name)
);

INSERT INTO
    node(name)
VALUES
    ('A');

INSERT INTO
    edge(from_node, to_node)
VALUES
    ('A', 'B'),
    ('A', 'C');

-- Make adjacency List;
Select
    name,
    to_node
from
    node
    LEFT JOIN edge ON node.name = edge.from_node;