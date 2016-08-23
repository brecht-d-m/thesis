import pandas as pd
import csv
import sys
import getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('parse_nt_index_table.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('parse_nt_index_table.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    
    if inputfile != '' and outputfile != '':
        parse_file(inputfile, outputfile)    

def parse_file(nt_file, csv_output_file): 
    # Read triples file
    df_nt_file = pd.read_table(nt_file, header = None, names = ["triple"])
    df_nt_file["triple"] = df_nt_file["triple"].str.replace("> ", ">\t")
    df_nt_file = df_nt_file["triple"].str.split("\t", expand=True, n=2) 

    # Predefined prefixes
    prefixArray = [
        "<http://xmlns.com/foaf/0.1/", 
        "<http://xmlns.com/foaf/", 
        "<http://localhost/vocabulary/bench/",
        "<http://www.w3.org/2001/XMLSchema#",
        "<http://purl.org/dc/elements/1.1/",
        "<http://purl.org/dc/terms/",
        "<http://purl.org/dc/dcmitype/",
        "<http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "<http://www.w3.org/2000/01/rdf-schema#",
        "<http://swrc.ontoware.org/ontology#",
        "<http://purl.org/rss/1.0/",
        "<http://www.w3.org/2002/07/owl#",
        "<http://localhost/persons/",
        "<http://example.org/",
        "<http://v.org/",
        "<http://rdfs.org/sioc/ns#>",
        "<http://rdfs.org/sioc/type#>",
        "<http://dbpedia.org/resource/",
        "<http://dbpedia.org/ontology/",
        "<http://dbpedia.org/property/",
        "<http://www.ins.cwi.nl/sib/vocabulary/>",
        "<http://www.ins.cwi.nl/sib/person/>",
        "<http://www.ins.cwi.nl/sib/user/>",
        "<http://www.ins.cwi.nl/sib/forum/>",
        "<http://www.ins.cwi.nl/sib/friendship/>",
        "<http://www.ins.cwi.nl/sib/group/>",
        "<http://www.ins.cwi.nl/sib/group/membership/>",
        "<http://www.ins.cwi.nl/sib/post/>",
        "<http://www.ins.cwi.nl/sib/post/comment/>",
        "<http://www.ins.cwi.nl/sib/photoalbum/photo/>",
        "<http://www.ins.cwi.nl/sib/photoalbum/>",
        "<http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#",
        "<http://www.w3.org/1999/02/22-rdf-syntax-ns#" ,
        "<http://www.w3.org/2002/07/owl#",
        "<http://db.uwaterloo.ca/~galuc/wsdbm/",
        "<http://schema.org/",
        "<http://purl.org/stuff/rev#",
        "<http://purl.org/ontology/mo/",
        "<http://purl.org/goodrelations/",
        "<http://www.geonames.org/ontology#",
        "<http://ogp.me/ns#"
    ]

    ## Subject
    subject_index = []
    parsed_subject = []
    for i in df_nt_file[0]:
        idx = 0

        prefix_idx = 0
        subject_parsed = i
        for prefix in prefixArray:
            if i.startswith(prefix):
                prefix_idx = idx
                subject_parsed = i[len(prefix):len(i)-1]
                break
            idx += 1

        subject_index.append(prefix_idx)
        parsed_subject.append(subject_parsed)

    ## Predicate
    predicate_index = []
    parsed_predicate = []
    for i in df_nt_file[1]:
        idx = 0

        prefix_idx = 0
        predicate_parsed = i
        for prefix in prefixArray:
            if i.startswith(prefix):
                prefix_idx = idx
                predicate_parsed = i[len(prefix):len(i)-1]
                break
            idx += 1

        predicate_index.append(prefix_idx)
        parsed_predicate.append(predicate_parsed)

    ## Object
    object_index = []
    parsed_object = []
    for i in df_nt_file[2]:
        idx = 0

        prefix_idx = 0
        object_parsed = i
        for prefix in prefixArray:
            if i.startswith(prefix):
                prefix_idx = idx+1
                object_parsed = i[len(prefix):len(i)]
                break
            idx += 1

        if prefix_idx == 0:
            object_parsed = object_parsed[:-2]

        object_index.append(prefix_idx)
        parsed_object.append(object_parsed)

    parsed_nt_file = pd.DataFrame()

    parsed_nt_file["subjectIndex"] = subject_index
    parsed_nt_file["subject"] = parsed_subject

    parsed_nt_file["predicateIndex"] = predicate_index
    parsed_nt_file["predicate"] = parsed_predicate

    parsed_nt_file["objectIndex"] = object_index
    parsed_nt_file["object"] = parsed_object
    parsed_nt_file["object"] = parsed_nt_file["object"].str.replace(">\t.","")

    parsed_nt_file.to_csv(csv_output_file, sep=",", header=False, index=False, quoting=csv.QUOTE_NONE)

if __name__ == "__main__":
   main(sys.argv[1:])
