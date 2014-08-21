#!/bin/bash
# Function:
#	process the SinicaSemanticParser/input.txt
#	and emit the xml format data in SinicaSemanticParser/output.txt
# History:
#	2014/08/21 @MaxisKao
java -cp .:../stanford-parser-full-2014-01-04/stanford-parser.jar:../stanford-parser-full-2014-01-04/stanford-parser-3.3.1-models.jar:../classifier/maxent/lib/trove-3.0.3.jar:../apache-opennlp-1.5.3/lib/opennlp-maxent-3.0.3.jar ConceptExtractorBatchClient
