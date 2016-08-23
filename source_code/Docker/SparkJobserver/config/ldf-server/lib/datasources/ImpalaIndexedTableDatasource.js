var Datasource = require('./Datasource'),
	http = require('http'),
	querystring = require('querystring'),
    N3 = require('n3'),
    request_ = require('request'),
    LRU = require('lru-cache'),
    Readable = require('stream').Readable;

var ENDPOINT_ERROR = 'Error accessing Impala endpoint';

var prefixArray = [
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
];

function ImpalaIndexedTableDatasource(options) {
    if(!(this instanceof ImpalaIndexedDatasource))
        return new ImpalaIndexedDatasource(options);
    Datasource.call(this, options);

    // Set endpoint URL
    options = options || {};
    this._endpointHost = (options.endpointHost || 'localhost').replace(/[\?#][^]*$/, '');
    this._endpointPort = (options.endpointPort || 5000);
	this._endpointPath = '/impala';
}

Datasource.extend(ImpalaIndexedTableDatasource, ['triplePattern', 'limit', 'offset', 'totalCount']);

// Writes the results of the query to the given triple stream
ImpalaIndexedDatasource.prototype._executeQuery = function (query, tripleStream, metadataCallback) {

	// Send a count request
	this._doTotalCount(query, metadataCallback);

	// Create data for GET request
	var data = {q: this._createTriplePattern(query, false)};
	var queryString = querystring.stringify(data);

	var options = {
		host: this._endpointHost,
		port: this._endpointPort,
		path: this._endpointPath + '?' + queryString,
		method: 'GET',
		headers: {
      			'Accept': 'application/json'
    		}
	}
	var req = http.request(options, function(res) {
		res.setEncoding('utf8');
		res.on('data', function(chunk) {	
			var result = JSON.parse(chunk);
			for(var idx in result) {
				tripleStream.push(parseTriple(result[idx]));
			}
		});
		res.on('end', function() {
			tripleStream.push(null);
		});
	});
	
	req.end();
	req.on('error', function(e) {
  		console.log('problem with request: ' + e.message);
	});

	// Emits an error on the triple stream
    function emitError(error) {
        error && tripleStream.emit('error', new Error(ENDPOINT_ERROR + ' ' + self._endpoint + ': ' + error.message));
    }
};

// Input something like:
//  {"predicateIndex", predicateIndex, "predicate": "testPredicate", "object": "testObject", "objectIndex": objectIndex, "subject": "testSubject", "subjectIndex": subjectIndex}
// Output: JSON object
function parseTriple(triple) {
	var tripleResult = {};
	
    subjectIndex = triple.subjectIndex;
    if(subjectIndex == 0) {
        // Not index  is not represented in the predefined prefix table 
	    tripleResult["subject"] = triple.subject.trim();
	    if(tripleResult["subject"][0] == '<' && tripleResult["subject"][tripleResult["subject"].length - 1] == '>') {
		    tripleResult["subject"] = tripleResult["subject"].substring(1, tripleResult["subject"].length - 1);
	    }
    } else {
        // Get prefix + concat
        tripleResult["subject"] = prefixArray[subjectIndex] + triple.subject.trim() + ">";
        tripleResult["subject"] = tripleResult["subject"].substring(1, tripleResult["subject"].length - 1);
    }
	
    predicateIndex = triple.predicateIndex;
    if(predicateIndex == 0) {
	    tripleResult["predicate"] = triple.predicate.trim();
	    if(tripleResult["predicate"][0] == '<' && tripleResult["predicate"][tripleResult["predicate"].length - 1] == '>') {
		    tripleResult["predicate"] = tripleResult["predicate"].substring(1, tripleResult["predicate"].length - 1);
	    }
    } else {
        tripleResult["predicate"] = prefixArray[predicateIndex] + triple.predicate.trim() + ">";
        tripleResult["predicate"] = tripleResult["predicate"].substring(1, tripleResult["predicate"].length - 1);
    }
	
    objectIndex = triple.objectIndex;
    if(objectIndex == 0) {
	    tripleResult["object"] = triple.object.trim();
	    if(tripleResult["object"][0] == '<' && tripleResult["object"][tripleResult["object"].length - 1] == '>') {
		    tripleResult["object"] = tripleResult["object"].substring(1, tripleResult["object"].length - 1);
	    }
    } else {
        tripleResult["object"] = prefixArray[objectIndex] + triple.object.trim() + ">";
        tripleResult["object"] = tripleResult["object"].substring(1, tripleResult["object"].length - 1);
    }

	return tripleResult;
}

ImpalaIndexedDatasource.prototype._doTotalCount = function(query, metadataCallback) {
	// Create the HTTP request
	var data = {q: this._createTriplePattern(query, true)};
	var queryString = querystring.stringify(data);

	var options = {
		host: this._endpointHost,
		port: this._endpointPort,
		path: this._endpointPath + '?' + queryString,
		method: 'GET',
		headers: {
      		'Accept': 'application/json'
    	}
	}

	var req = http.request(options, function(res) {
    	res.setEncoding('utf8');
    	res.on('data', function (chunk) {
			metadataCallback({ totalCount: JSON.parse(chunk)[0].count });
    	});
  	});
	
	req.on('error', function(e) {
    	console.log('problem with request: ' + e.message);
  	});
	
  	req.end();
};

// Creates a SQL pattern for the given triple pattern
ImpalaIndexedDatasource.prototype._createTriplePattern = function (triple, count) {
    if(count) {
		var query = "SELECT count(*) as count FROM temp_table ";
	} else {
		var query = "SELECT subject, predicate, object FROM temp_table ";
	}
    var queryFilter = "WHERE "
    var queryFilterAvailable = false;

    // Add a possible subject IRI
    if(triple.subject) {
        var prefixIdx = parseURI(triple.subject);
        queryFilter += 'subjectIndex = ' + prefixIdx[1] + ' AND subject = "' + prefixIdx[0] + '" ';
        queryFilterAvailable = true;
    }

    // Add a possible predicate IRI
    if(triple.predicate) {
        if(queryFilterAvailable) {
 	        queryFilter += "AND "
	    }

        var prefixIdx = parseURI(triple.predicate);
        queryFilter += 'predicateIndex = ' + prefixIdx[1] + ' AND predicate = "' + prefixIdx[0] + '" ';
        queryFilterAvailable = true;
    }

	if(triple.object) {
        if(queryFilterAvailable) {
 	        queryFilter += "AND "
	    }
        
        queryFilterAvailable = true;
		// Add a possible object IRI or literal
		if (N3.Util.isIRI(triple.object)) {
            var prefixIdx = parseURI(triple.object);
            queryFilter += 'objectIndex = ' + prefixIdx[1] + ' AND object = "' + prefixIdx[0] + '" ';
		} else if (!(literalMatch = /^"([^]*)"(?:(@[^"]+)|\^\^([^"]+))?$/.exec(triple.object))) {
		    noop();
		} else {
            var queryObject = triple.object.replace(/\"/g, '\\"');
            queryObject = queryObject.replace(/\'/g, "\\'");
			queryFilter += 'objectIndex = 0 AND object = "' + queryObject + '" ';
		}
	}
    
    if(queryFilterAvailable) {
        query += queryFilter;
    } 

	if(!count && (triple.limit || triple.offset)) {
		query += "ORDER BY subject "
		if(!triple.limit) {
			//query += "LIMIT 10 ";
		} else {
    		query += "LIMIT " + triple.limit + " ";
		}
    	if(!triple.offset) {
			//query += "OFFSET 0 ";
    	} else {
			query += "OFFSET " + triple.offset + " ";
    	}
	}
    query += ";";

    console.log(query);
    
    return query;
};

// The empty function
function noop() {}

// Remove the prefix from the uri, or if the prefix is not available return the uri
// Return the index
function parseURI(uri) {
    var idx = 0;
    for(var prefix in prefixArray) {
        if(uri.startsWith(prefix)) {
            return [uri.substring(prefix.length, uri.length), idx+1];
        }
        idx += 1;
    }
}

module.exports = ImpalaIndexedDatasource;
