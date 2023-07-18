const fs = require('fs');
const toCsvString = require('../string2csv').toCsvString;
const parseString = require('xml2js').parseString;
const readFileAutoEncoding = require('../readfileautoencoding').readFileAutoEncoding;

exports.preprocess = function (config) {
    let files = fs.readdirSync(config['source']);

    let argumentsCSV = 'argument-id,argument\n';
    let documentsCSV = 'document-id,document\n';


    files.forEach(path => {
        let splitPath = path.split('.');
        let file = readFileAutoEncoding(`${config['source']}/${path}`, 'utf8');
        if (splitPath.length === 2 &&  splitPath[1] === 'txt') {
            documentsCSV += `${toCsvString(path.replace('.txt', ''))},${toCsvString(file)}\n`;
        } else {
            // Get TextWithNodes
            let textWithNodesMatch = (/<TextWithNodes>([\s\S]*?)<\/TextWithNodes>/g).exec(file);

            if (textWithNodesMatch === null || textWithNodesMatch.length !== 2) {
                console.warn(`Missing TextWithNodes-node in ${path}`);
                return;
            }
            let nodeText = textWithNodesMatch[1];

            // Get AnnotationSet
            let annotationSetMatch =  (/<AnnotationSet>([\s\S]*?)<\/AnnotationSet>/g).exec(file);
            if (annotationSetMatch === null || annotationSetMatch.length !== 2) {
                console.warn(`Missing AnnotationSet-node in ${path}`);
                return;
            }
            let annotationSetText = annotationSetMatch[0];

            parseString(annotationSetText, (error, result) => {
                if (!error) {

                    result['AnnotationSet']['Annotation'].filter(annotation => annotation['$']['Type'] === 'arg').forEach(annotation => {
                        let id = annotation['$']['Id'];
                        let startNode = annotation['$']['StartNode'];
                        let endNode = annotation['$']['EndNode'];

                        let argumentExp = new RegExp(`<Node id="${startNode}" \/>([\\s\\S]*?)<Node id="${endNode}" \/>` ,'g');
                        let argumentMatch = argumentExp.exec(nodeText);
                        
                        if (argumentMatch == null || argumentMatch.length !== 2) {
                            console.warn(`No argument-text found with id ${id}, start-node ${startNode}, end-node ${endNode}`);
                        } else {
                            let argId = `${path.replace('.xml', '')}.${id}`;
                            argumentsCSV += `${argId},${toCsvString(argumentMatch[1])}\n`
                        }
                    });
                }
            });
        }
    });

    if (config['preprocessed-arguments']) {
        fs.writeFileSync(config['preprocessed-arguments'], argumentsCSV);
    }

    if (config['preprocessed-documents']) {
        fs.writeFileSync(config['preprocessed-documents'], documentsCSV);
    }

    console.log('Done preprocessing corpus-upittsburgh-arguing-subjectivity.\n');
}