#!/bin/bash
# Function:
#	Download dependency pakages to run SinicaSemanticParser
# History:
#	2014/08/21 @MaxisKao

StanfordParserVersion="2014-01-04"
ApacheOpenNLPVersion="1.5.3"

STANFORD="stanford-parser-full-$StanfordParserVersion"
OPENNLP="apache-opennlp-$ApacheOpenNLPVersion"

if [ ! -f "$STANFORD.zip" ]; then
	wget http://nlp.stanford.edu/software/$STANFORD.zip
fi

if [ ! -f "$OPENNLP-bin.zip" ]; then
	wget http://apache.stu.edu.tw//opennlp/opennlp-$ApacheOpenNLPVersion/$OPENNLP-bin.zip
fi

if [ ! -d "$STANFORD" ]; 
then
	echo "unzip $STANFORD"
	unzip -q $STANFORD.zip
else
	echo "$STANFORD exists"
fi

if [ ! -d "$OPENNLP" ]; 
then
	echo "unzip $OPENNLP-bin.zip"
	unzip -q $OPENNLP-bin.zip
else
	echo "$OPENNLP exists"
fi

## compile java

echo "building system..."
javac -cp system/.:stanford-parser-full-2014-01-04/stanford-parser.jar:stanford-parser-full-2014-01-04/stanford-parser-3.3.1-models.jar:classifier/maxent/lib/trove-3.0.3.jar:apache-opennlp-1.5.3/lib/opennlp-maxent-3.0.3.jar system/*.java

echo "Done!"

