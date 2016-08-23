#!/bin/bash

export hdtFile=$1
shift

java -d64 -server -Xmx1024M -classpath 'hdt-lib.jar:hdt-jena.jar:lib/*' org.rdfhdt.hdtjena.HDTSparql $hdtFile "$*"
