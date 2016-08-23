#!/bin/bash

java -server -Xmx1024M -classpath 'hdt-lib.jar:lib/*' org.rdfhdt.hdt.tools.HdtSearch $*
