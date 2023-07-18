const fs = require('fs');
const toCsvString = require('../string2csv').toCsvString;

exports.preprocess = function (config) {
    let files = fs.readdirSync(config['source']);

    let argumentsCSV = 'argument-id,argument\n';
    let documentsCSV = 'document-id,document\n';

    files.forEach(path => {
        let discussion = JSON.parse(fs.readFileSync(`${config['source']}/${path}`));

        let id = discussion.id;
        let fullText = '';
        
        discussion.arguments.claims.forEach(claim => {
            let text = toCsvString(claim.text);
            let claim_id = claim.id;
            argumentsCSV += `${claim_id},${text}\n`;
            fullText += claim.text + ' ';
        });

        documentsCSV += `${id},${toCsvString(fullText)}\n`;
        
    });

    if (config['preprocessed-arguments']) {
        fs.writeFileSync(config['preprocessed-arguments'], argumentsCSV);
    }

    if (config['preprocessed-documents']) {
        fs.writeFileSync(config['preprocessed-documents'], documentsCSV);
    }

    console.log('Done preprocessing kialo.\n');
}