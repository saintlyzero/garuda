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
SELECT
    srvc.id,
    srvc.name,
    srvc_sts.cpu_utilization,
    srvc_sts.memory_utilization,
    srvc_sts.created_at
FROM
    service AS srvc
    LEFT JOIN (
        SELECT
            service_id,
            cpu_utilization,
            memory_utilization,
            created_at,
            ROW_NUMBER() OVER(
                PARTITION BY service_id
                ORDER BY
                    created_at DESC
            ) AS RowNo
        FROM
            service_status
    ) AS srvc_sts ON srvc.id = srvc_sts.service_id
    AND srvc_sts.RowNo = 1;

-- 
WITH srvc_sts as (
    SELECT
        service_id,
        cpu_utilization,
        memory_utilization,
        created_at,
        ROW_NUMBER() OVER(
            PARTITION BY service_id
            ORDER BY
                created_at DESC
        ) AS RowNo
    FROM
        service_status
)
SELECT
    srvc.id,
    srvc.name,
    srvc_sts.cpu_utilization,
    srvc_sts.memory_utilization,
    srvc_sts.created_at
FROM
    service srvc
    LEFT JOIN srvc_sts ON srvc.id = srvc_sts.service_id
    AND srvc_sts.RowNo = 1;