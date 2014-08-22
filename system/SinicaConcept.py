
# coding: utf-8

import logging
import socket
import conceptFormulator2
import conceptFormulator

class SinicaConcept(object):
    """
    A python wrapper for SinicaConceptParser

    - Dependency:
        conceptFormulator.py
        conceptFormulator2.py
    - Servers:
        featureExtractorServer [Python]
        ConceptExtractorServer [Java]

    MaxisKao @ 2014.08.22
    """
    def __init__(self, host="localhost", port=29999, **kwargs):

        loglevel = logging.DEBUG if 'verbose' in kwargs and kwargs['verbose'] == True else logging.INFO
        logging.basicConfig(format='[%(levelname)s] %(message)s', level=loglevel)

        self.host = host
        self.port = port

    def load_txt(self, path):
        ## read the input.txt into lines 
        try:
            sents = open(path).readlines()
        except OSError:
            logging.error("input file %s doesn't exist" % (path))
        return sents

    def parseAll(self, sents, formulators=[1, 2]):
        """
        Parse all loaded sentences
        """
        conceptsAll = []

        for sent in sents:

            concepts = self.parse(sent, formulators)

            conceptsAll.append( concepts )

        return conceptsAll

    def parse(self, sent, formulators=[1, 2]):
        """
        Parse one sentence
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        logging.debug("send '%s' to server" % (sent.strip()))

        if not sent.endswith('\n'): 
            sent = sent + '\n'
        sock.sendall(sent)

        received = sock.recv(1024)

        sock.close()

        if len(formulators) == 0:
            raise ValueError('set at least one formulator. Available: 1, 2')

        concepts = {}

        if 1 in formulators:
            logging.debug("Formulate using conceptFormulator")
            concepts[1] = conceptFormulator.build( sent=sent.strip(), tofile=False )

        if 2 in formulators:
            logging.debug("Formulate using conceptFormulator2")
            concepts[2] = conceptFormulator2.build( sent=sent.strip(), tofile=False )

        return concepts

    def test(self):
        sents = self.load_txt(path='../input/input.txt')
        for sent in sents:
            print sent
            concepts = self.parse(sent)
            print concepts        

if __name__ == '__main__':

    # from SinicaConcept import SinicaConcept

    sc = SinicaConcept(host="localhost", port=29999, verbose=True)

    sents = sc.load_txt(path='../input/input.txt')
    
    # for sent in sents:
    #     concepts = sc.parse(sent)
    #     print concepts

    conceptsAll = sc.parseAll(sents)
