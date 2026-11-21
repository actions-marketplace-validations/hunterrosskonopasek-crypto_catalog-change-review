'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const {parseRows, checkCatalog} = require('./identity-check.js');

test('case collision, exact intended update and preserved leading zeros', () => {
  const report = checkCatalog('sku;name\nAB;one\n0003;two\n03;third', 'sku;name\nab;old\n0003;other');
  assert.deepEqual(report.findings.map(f => [f.number,f.existing]), [[1,[1]]]);
});
test('mixed and exact duplicates flag every participating proposed record', () => {
  assert.deepEqual(checkCatalog('sku\nA\na\na',null).findings.map(f => f.number), [1,2,3]);
});
test('UTF-8 BOM, blank physical records, leading whitespace and non-ASCII holds', () => {
  const report = checkCatalog('\uFEFFsku;name\r\n\r\n;missing\r\n x;space\r\nø;accent',null);
  assert.equal(report.proposedCount,3);
  assert.deepEqual(report.findings.map(f => f.number),[2,3,4]);
});
test('quoted separators and multiline fields retain correct record numbers', () => {
  assert.deepEqual(parseRows('sku,name\r\n"00,21","say ""hi""\nand go"\r\n',','),[['sku','name'],['00,21','say "hi"\nand go']]);
});
test('invalid inputs fail visibly', () => {
  for (const data of ['sku;sku\na;b','name\nx','sku;name\na','sku\n"bad','sku\n"a"x','sku\na"b','sku\n']) {
    assert.throws(() => checkCatalog(data,null));
  }
});
test('existing ambiguous duplicates include total count and bounded example records', () => {
  const report = checkCatalog('sku\nA', 'sku\n' + Array(10000).fill('a').join('\n'));
  assert.equal(report.findings[0].matchCount,10000);
  assert.deepEqual(report.findings[0].existing,[1,2,3,4,5,6,7,8,9,10]);
});
test('existing export is optional and CSV accepts custom header and tab', () => {
  assert.equal(checkCatalog('item\tname\nA\tBox',null,'\t','item').compared,false);
  assert.equal(checkCatalog('item\tname\nA\tBox','item\tname','\t','item').compared,true);
});
