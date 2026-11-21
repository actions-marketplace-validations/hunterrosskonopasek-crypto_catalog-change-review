'use strict';
const byId = id => document.getElementById(id);
const exampleIncoming = 'sku;name\nBX-17;Box\n00031;Screw\nKIT-9;Kit\nkit-9;Kit refill\n;Insert\nREF-6;Reference\n';
const exampleExisting = 'sku;name\nbx-17;Existing box\n00031;Existing screw\n';
let report = null;
let run = 0;
function reset(message) {
  run++;
  report = null;
  byId('status').textContent = message;
  byId('results').replaceChildren();
  byId('download').hidden = true;
}
function show(data, label) {
  report = data;
  const comparison = data.compared ? data.existingCount + ' existing records compared.' : 'Within-file check only.';
  byId('status').textContent = label + ' ' + data.proposedCount + ' proposed records. ' + data.findings.length + ' need review. ' + comparison;
  if (!data.findings.length) return;
  const table = document.createElement('table');
  const head = table.createTHead().insertRow();
  for (const title of ['Proposed row', 'Reason for review', 'Existing rows']) {
    const cell = document.createElement('th'); cell.scope = 'col'; cell.textContent = title; head.append(cell);
  }
  const body = table.createTBody();
  for (const f of data.findings.slice(0,100)) {
    const row = body.insertRow();
    const matches = f.existing.join(', ') + (f.matchCount > 10 ? ' (first 10 of ' + f.matchCount + ')' : '');
    for (const value of [f.number, f.reasons.join(' / '), matches || '—']) row.insertCell().textContent = value;
  }
  byId('results').append(table);
  if (data.findings.length > 100) byId('results').append('Showing the first 100 rows. Download the full review below.');
  byId('download').hidden = false;
}
async function readFile(file) {
  if (file.size > 5 * 1024 * 1024) throw new Error('Each file must be at most 5 MiB.');
  return new TextDecoder('utf-8', {fatal: true}).decode(await file.arrayBuffer());
}
for (const id of ['incoming','existing','key','delimiter']) {
  byId(id).addEventListener('input', () => reset('Inputs changed. Run the check again.'));
}
byId('check').addEventListener('click', async () => {
  reset('Reading files locally…');
  const ticket = run;
  try {
    const incoming = byId('incoming').files[0], existing = byId('existing').files[0];
    if (!incoming) throw new Error('Choose the proposed CSV first.');
    const delimiter = byId('delimiter').value, header = byId('key').value;
    const [left, right] = await Promise.all([readFile(incoming), existing ? readFile(existing) : null]);
    if (ticket !== run) return;
    show(checkCatalog(left, right, delimiter === 'tab' ? '\t' : delimiter, header), 'Your files.');
  } catch (err) { if (ticket === run) reset(err instanceof TypeError ? 'Use a valid UTF-8 CSV file.' : err.message); }
});
byId('sample').addEventListener('click', () => {
  reset(''); show(checkCatalog(exampleIncoming, exampleExisting), 'Illustrative example.');
});
byId('download').addEventListener('click', () => {
  if (!report) return;
  const rows = [['proposed_record','reasons','existing_records_first_10','existing_match_count'], ...report.findings.map(f => [f.number,f.reasons.join(' | '),f.existing.join(' '),f.matchCount])];
  const csv = rows.map(row => row.map(v => '"' + String(v).replace(/"/g,'""') + '"').join(',')).join('\r\n') + '\r\n';
  const url = URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
  const link = document.createElement('a'); link.href = url; link.download = 'identifier-review.csv'; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
