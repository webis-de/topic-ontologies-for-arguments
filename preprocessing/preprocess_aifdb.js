const fs = require('fs');
const toCsvString = require('../string2csv').toCsvString;
const readFileAutoEncoding = require('../readfileautoencoding').readFileAutoEncoding;

exports.preprocess = function (config) {
    let files = fs.readdirSync(config['source']);

    let argumentsCSV = 'argument-id,argument\n';
    let documentsCSV = 'document-id,document\n';


    files.forEach(path => {
        try {
            let obj = JSON.parse(readFileAutoEncoding(`${config['source']}${path}`));
            let doc = '';
            obj.nodes.forEach(node => {
                if (node.type === 'I') {
                    doc += node.text;
                    argumentsCSV += `${path.replace('.json', '')}.${node.nodeID},${toCsvString(node.text)}\n`;
                }
            });
            documentsCSV += `${path.replace('.json', '')},${toCsvString(doc)}\n`;
        } catch(e) {

        }  
    });

    if (config['preprocessed-arguments']) {
        fs.writeFileSync(config['preprocessed-arguments'], argumentsCSV);
    }

    if (config['preprocessed-documents']) {
        fs.writeFileSync(config['preprocessed-documents'], documentsCSV);
    }

    console.log('Done preprocessing aifdb.\n');
}