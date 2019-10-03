import io
import unittest
import warnings
import xml.etree.ElementTree as etree

import pronto



class TestOwlXMLParser(unittest.TestCase):

    @staticmethod
    def get_ontology(content):
        xml = f"""
        <rdf:RDF xmlns="http://purl.obolibrary.org/obo/TEMP#"
             xml:base="http://purl.obolibrary.org/obo/TEMP"
             xmlns:owl="http://www.w3.org/2002/07/owl#"
             xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns:xml="http://www.w3.org/XML/1998/namespace"
             xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
             xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
             xmlns:oboInOwl="http://www.geneontology.org/formats/oboInOwl#">
            {content}
        </rdf:RDF>
        """
        s = io.BytesIO(xml.encode('utf-8'))
        return pronto.Ontology(s)

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter("error")

    @classmethod
    def tearDownClass(cls):
        warnings.simplefilter(warnings.defaultaction)

    def test_cyclic_relationship(self):
        ont = self.get_ontology(
            """
            <owl:Ontology/>
            <owl:ObjectProperty rdf:about="http://purl.obolibrary.org/obo/TST_001">
                <oboInOwl:id rdf:datatype="http://www.w3.org/2001/XMLSchema#string">TST:001</oboInOwl:id>
                <oboInOwl:is_cyclic rdf:datatype="http://www.w3.org/2001/XMLSchema#boolean">true</oboInOwl:is_cyclic>
            </owl:ObjectProperty>
            """
        )
        self.assertIn("TST:001", ont)
        self.assertTrue(ont["TST:001"].cyclic)
