import rdflib
from rdflib.graph import Graph


if __name__ == "__main__":
    """
    This is a program to extract the property of attribute subset of the NCIT-Ontology using rdflib.
    """
    filename = "owlapi.xrdf"

    g = Graph()
    g.parse(filename, format=rdflib.util.guess_format(filename))
    qres = g.query("""
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX ncid: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
                    CONSTRUCT {
                        ?poa ?a ?b .
                        ?a rdfs:label ?l1 .
                        ?b rdfs:label ?l2 .
                    } WHERE {
                        {
                            ?poa (rdfs:subClassOf)* ?x ;
                                ?a ?b .
                            OPTIONAL {?a rdfs:label ?l1 .}
                            OPTIONAL {?b rdfs:label ?l2 .}
                            FILTER(?x = ncid:C20189)
                        }
                    }""")

    gnew = Graph()
    gnew.parse(data=qres.serialize(format='xml'))
    gnew.serialize(destination='file.n3', format='n3')
