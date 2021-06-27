import rdflib
import time
from rdflib.graph import Graph

if __name__ == "__main__":
    filename = "propertyorattribute.n3"

    g = Graph()
    g.parse(filename, format= rdflib.util.guess_format(filename))

    t = time.time()
    qres = g.query("""
                    SELECT ?x ?y ?z
                    WHERE {
                        ?x ?y ?z
                        FILTER (?x = ns1:A30 ||
                            ?y = ns1:A30 ||
                            ?z = ns1:A30)
                    }    
                    LIMIT 10
                    """)

    print("time: {}", time.time() - t)

    for row in qres:
        print(row)
