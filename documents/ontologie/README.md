## Property or Attribute - Extraction and Ontology
# related to issue: https://git.rwth-aachen.de/lab-semantic-data-integration-2021/team-2-data-lake/-/issues/6

The issue was to provide an ontology by default. Therefore we decided on the 'Property or Attribute' subset of the
NCIT Ontology(https://bioportal.bioontology.org/ontologies/NCIT?p=classes&conceptid=http%3A%2F%2Fncicb.nci.nih.gov%2Fxml%2Fowl%2FEVS%2FThesaurus.owl%23C44185).

The 'Property or Attribute' subset was extracted with query_poa.py. If you want to repeat the step you can download the
ontology in a suitable format(e.g. xrdf) and simply execute the python program. This takes some(probably more) time.

The Subset contains the Property or Attribute class, all subclasses and labels for referenced instances that are not in
the 'Property or Attribute'-subset itself.


