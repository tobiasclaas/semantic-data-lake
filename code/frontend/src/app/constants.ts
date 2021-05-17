const none = { label: '--', value: null };
const mongodb = { label: 'MongoDB', value: 'MongoDB' };
const postrgesql = { label: 'PostgreSQL', value: 'PostgreSQL' };
const file = { label: 'File', value: 'File' };

export const SOURCES = {
    none: none.value,
    mongodb: mongodb.value,
    postgresql: postrgesql.value,
    file: file.value,
    options: [none, mongodb, postrgesql, file],
};

const sas = { label: 'Same as Source', value: null };
const hdfs = { label: 'HDFS', value: 'HDFS' };

export const TARGETS = {
    sameAsSource: sas.value,
    mongodb: mongodb.value,
    postgresql: postrgesql.value,
    hdfs: hdfs.value,
    options: [sas, mongodb, postrgesql, hdfs],
};

export const FILE_TYPE = {
    csv: 'text/csv',
    json: 'application/json',
    xml: 'application/xml'
};
