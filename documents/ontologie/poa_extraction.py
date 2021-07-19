import rdflib
from rdflib.graph import Graph


if __name__ == "__main__":
    """
    This is a program to extract the property of attribute subset of the NCIT-Ontology using rdflib.
    """
    filename = "owlapi.xrdf"

    g = Graph()
    g.parse(filename, format=rdflib.util.guess_format(filename))
    q_res = g.query("""
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX ncid: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
                    CONSTRUCT {
                        ?x ?a ?b .
                        ?a rdfs:label ?l1 .
                        ?b rdfs:label ?l2 .
                    } WHERE {
                        {
                            ?x (rdfs:subClassOf)* ?poa ;
                                ?a ?b .
                            OPTIONAL {?a rdfs:label ?l1 .}
                            OPTIONAL {?b rdfs:label ?l2 .}
                            FILTER(?poa = ncid:C20189)
                        }
                    }""")

    g_new = Graph()
    g_new.parse(data=q_res.serialize(format='xml'))
    g_new.serialize(destination='file.n3', format='n3')
