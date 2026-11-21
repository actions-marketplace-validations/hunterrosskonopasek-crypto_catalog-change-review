'use strict';

// Records are numbered after the header, independent of embedded newlines.
function parseRows(text, delimiter) {
  const data = text.replace(/^\uFEFF/, '');
  if (![',', ';', '\t'].includes(delimiter)) throw new Error('Choose comma, semicolon or tab.');
  const rows = [];
  let row = [], field = '', quoted = false, afterQuote = false, started = false;
  for (let i = 0; i < data.length; i++) {
    const char = data[i];
    if (quoted) {
      if (char !== '"') field += char;
      else if (data[i + 1] === '"') { field += '"'; i++; }
      else { quoted = false; afterQuote = true; }
    } else if (char === delimiter) {
      row.push(field); field = ''; afterQuote = false; started = true;
    } else if (char === '\r' || char === '\n') {
      if (char === '\r' && data[i + 1] === '\n') i++;
      rows.push(started ? [...row, field] : []);
      if (rows.length > 50001) throw new Error('A file may contain up to 50,000 data records.');
      row = []; field = ''; afterQuote = false; started = false;
    } else if (afterQuote || (char === '"' && field.length)) {
      throw new Error('Unexpected character in quoted CSV at record ' + (rows.length + 1) + '.');
    } else if (char === '"') { quoted = true; started = true; }
    else { field += char; started = true; }
  }
  if (quoted) throw new Error('An opening CSV quote has no closing quote.');
  if (started) rows.push([...row, field]);
  if (rows.length > 50001) throw new Error('A file may contain up to 50,000 data records.');
  return rows;
}

function readKeys(text, delimiter, header, label) {
  const [names = [], ...rows] = parseRows(text, delimiter);
  if (!header || names.filter(name => name === header).length !== 1)
    throw new Error(label + ' needs one column named "' + header + '". Check the delimiter and header.');
  const index = names.indexOf(header);
  const entries = [];
  rows.forEach((row, i) => {
    if (!row.length) return;
    if (row.length !== names.length) throw new Error(label + ' record ' + (i + 1) + ' has the wrong field count.');
    entries.push({number: i + 1, key: row[index]});
  });
  return entries;
}

const asciiFold = key => key.replace(/[A-Z]/g, ch => ch.toLowerCase());
function groupByKey(entries) {
  const groups = new Map();
  for (const entry of entries) {
    if (!entry.key.trim()) continue;
    const key = asciiFold(entry.key);
    if (!groups.has(key)) groups.set(key, {count: 0, sample: [], spellings: new Set()});
    const group = groups.get(key);
    group.count++;
    group.spellings.add(entry.key);
    if (group.sample.length < 10) group.sample.push(entry.number);
  }
  return groups;
}

function checkCatalog(incoming, existing, delimiter = ';', header = 'sku') {
  const incomingRows = readKeys(incoming, delimiter, header, 'Proposed file');
  if (!incomingRows.length) throw new Error('The proposed file has no product records.');
  const currentRows = existing === null ? [] : readKeys(existing, delimiter, header, 'Existing file');
  const proposedGroups = groupByKey(incomingRows);
  const currentGroups = groupByKey(currentRows);
  const findings = [];
  for (const {key, number} of incomingRows) {
    const reasons = [];
    const folded = asciiFold(key);
    const group = proposedGroups.get(folded);
    const current = currentGroups.get(folded);
    if (!key.trim()) reasons.push('Blank identifier');
    if (key.trim() && key.trim() !== key) reasons.push('Leading or trailing whitespace');
    if (/[^\x20-\x7e]/.test(key)) reasons.push('Non-ASCII or control character requires review');
    if (group && group.count > 1) reasons.push('Repeated proposed identifier (ASCII case ignored)');
    if (current && current.count > 1) reasons.push('Multiple matching existing records');
    if (current && (current.spellings.size > 1 || !current.spellings.has(key))) reasons.push('Case differs from existing identifier');
    if (reasons.length) findings.push({number, reasons, existing: current ? current.sample : [], matchCount: current ? current.count : 0});
  }
  return {proposedCount: incomingRows.length, existingCount: currentRows.length, compared: existing !== null, findings};
}
if (typeof module !== 'undefined') module.exports = {parseRows, checkCatalog};
