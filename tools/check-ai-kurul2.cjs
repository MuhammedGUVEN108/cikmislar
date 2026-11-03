'use strict';
// Static data/behavior validation; not medical review and not a browser test.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict'),cp=require('node:child_process');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const c={};c.window=c;vm.createContext(c);
let snapshot;
for(const [,src] of html.matchAll(/<script\b[^>]*src="([^"]+)"/g)) {
 if(!src.startsWith('js/')||src==='js/app.js')continue;
 if(src.endsWith('ai-support-kurul2.js'))snapshot=JSON.stringify([c.QUESTION_DATA,c.GENERATED_QUESTION_DATA,c.GENERATED_EXPLANATIONS,c.GENERATED_GLOSSARY]);
 vm.runInContext(fs.readFileSync(path.join(root,src),'utf8'),c,{filename:src});
 if(src.endsWith('ai-support-kurul2.js'))assert.equal(JSON.stringify([c.QUESTION_DATA,c.GENERATED_QUESTION_DATA,c.GENERATED_EXPLANATIONS,c.GENERATED_GLOSSARY]),snapshot,'AI script mutated original data');
}
const m=c.ARCHIVE_AI_MANIFEST,d=c.ARCHIVE_EXPLANATIONS,g=c.ARCHIVE_GLOSSARY,qs=c.QUESTION_DATA.filter(q=>q.committee===2);
assert.equal(m.total,qs.length);assert.equal(m.pending,0);assert.equal(m.mode,'static_authored');
assert.equal(Object.keys(d).length,m.supported);assert.equal(m.excluded.length,m.omitted);assert.equal(m.total,m.supported+m.omitted);
const excluded=new Map(m.excluded.map(x=>[x.id,x]));assert.equal(excluded.size,m.omitted);
let options=0;
for(const q of qs) {
 const detail=d[q.id];assert.equal(Boolean(detail),!excluded.has(q.id),'Scope gap/overlap '+q.id);
 if(!detail){assert.ok(excluded.get(q.id).reason.length>15,'Missing exclusion reason '+q.id);continue;}
 assert.notEqual(q.status,'source_incomplete');assert.equal(q.verifiedKeys,null);
 assert.ok(detail.summary.length>60);assert.equal(detail.provenance,'ai_authored');assert.equal(detail.academicVerification,false);
 assert.equal(detail.options.length,5);assert.equal(new Set(detail.options.map(o=>o.reason)).size,5,'Duplicate option filler '+q.id);
 for(let i=0;i<5;i++) {
  const a=detail.options[i],o=q.options[i];
  assert.equal(a.label,o.label);assert.equal(a.optionText,o.text);assert.equal(a.isCorrect,q.sourceKeys.includes(o.label));
  assert.ok(a.reason.length>20,'Missing reason '+q.id+' '+a.label);assert.ok(!/[<>]/.test(a.reason),'Unexpected markup');options++;
 }
 assert.ok(detail.terms.length>=2&&detail.terms.length<=6);assert.equal(new Set(detail.terms).size,detail.terms.length);
 for(const term of detail.terms)assert.ok(g[term]?.length>20,'Missing glossary definition '+term);
}
for(const id of Object.keys(d))assert.ok(qs.some(q=>q.id===id),'Unknown ID '+id);
// The tracked 469-question source must remain byte-identical to its published commit.
const original=cp.execFileSync('git',['show','HEAD:js/data/archive/questions-kurul-2.js'],{cwd:root,maxBuffer:8*1024*1024});
assert.equal(original.toString('utf8').replace(/\r\n/g,'\n'),fs.readFileSync(path.join(root,'js/data/archive/questions-kurul-2.js'),'utf8').replace(/\r\n/g,'\n'),'Question source changed (line endings ignored)');
const report={passed:true,scope:qs.length,supported:m.supported,excluded:m.omitted,optionReasons:options,glossaryTerms:Object.keys(g).length,originalQuestionsUnchanged:true,generatedDataUnchanged:true,scientificVerification:false};
fs.mkdirSync(path.join(root,'_work/reports'),{recursive:true});fs.writeFileSync(path.join(root,'_work/reports/ai-kurul2-check.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
