const parseString = require('xml2js').parseString;
const fs = require('fs');
const toCsvString = require('../string2csv').toCsvString;

exports.preprocess = function (config) {    
    const source = config['source'];

    let filenames = fs.readdirSync(source);

    let documentsCSV = 'document-id,document\n';
    let argumentsCSV = 'argument-id,argument\n'

    filenames.forEach(filename => {
        let file = fs.readFileSync(`${source}/${filename}`, 'utf8');

        parseString(file, (error, result) => {
            if (!error) {
                let doc = result['xmi:XMI']['cas:Sofa']['0']['$']['sofaString'];

                let docId = filename.replace('.xmi', '');

                documentsCSV += `${toCsvString(docId)},${toCsvString(doc)}\n`;
                // console.log(doc)
                result['xmi:XMI']['argumentation:Argument'].forEach(entry => {
                    let argument = entry['$'];

                    let argumentText = doc.substring(argument['begin'], argument['end']);
                    argumentsCSV += `${toCsvString(`${docId}.${argument['xmi:id']}`)},${toCsvString(argumentText)}\n`;
                });
            }
        });
    });

    if (config['preprocessed-arguments']) {
        fs.writeFileSync(config['preprocessed-arguments'], argumentsCSV);
    }

    if (config['preprocessed-documents']) {
        fs.writeFileSync(config['preprocessed-documents'], documentsCSV);
    }
    console.log(`Done preprocessing ukp-argument-annotated-essays-v2.\n`);
}