'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p),'utf8');
const html=read('index.html'),ctx={console};ctx.window=ctx;ctx.globalThis=ctx;vm.createContext(ctx);
const scripts=[...html.matchAll(/<script\b[^>]*\bsrc="([^"]+)"/g)].map(m=>m[1]);
for(const src of scripts.filter(p=>p.startsWith('js/')&&p!=='js/app.js'))vm.runInContext(read(src),ctx,{filename:src});
new vm.Script(read('js/app.js'));
const all=ctx.QUESTION_DATA,C=ctx.QuizCore,k1=C.select(all,{committee:'1'}),k2=C.select(all,{committee:'2'});
assert.equal(all.length,1010);assert.equal(k1.length,541);assert.equal(k2.length,469);
assert.equal(ctx.GENERATED_QUESTION_DATA.length,180);assert.equal(new Set(all.map(q=>q.id)).size,1010);
assert.equal(C.select(all,{committee:'2',includeReview:false}).length,459);
const expected={'2021-2022':95,'2022-2023':93,'2023-2024':93,'2024-2025':100,'2025-2026':88};
let matrices=0,options=0,figures=0;
for(const [year,n] of Object.entries(expected))assert.equal(C.select(all,{committee:'2',year}).length,n);
for(const committee of ['', '1','2'])for(const year of ['',...new Set(all.map(q=>q.year))])for(const subject of ['',...new Set(all.map(q=>q.subject))]){
 const expected=all.filter(q=>(!committee||String(q.committee||1)===committee)&&(!year||q.year===year)&&(!subject||q.subject===subject));
 assert.equal(C.select(all,{committee,year,subject}).length,expected.length);matrices++;
}
const readable=read('soru-arsivi.html');
for(const q of k2){
 assert.deepEqual(Array.from(q.options,o=>o.label),['A','B','C','D','E']);assert.equal(q.verifiedKeys,null);assert.equal(q.recommendedKeys,null);
 const key=C.gradingKey(q),incomplete=q.status==='source_incomplete';
 for(const o of q.options){
  const grade=C.evaluate(q,o.label);
  assert.equal(grade.result,incomplete?'review':o.label===q.sourceKeys[0]?'correct':'wrong');
  if(incomplete)assert.equal(grade.key,null);options++;
 }
 for(const p of [...q.sourceImages,...q.visuals,...q.options.map(o=>o.image).filter(Boolean)])assert.ok(fs.existsSync(path.join(root,p)),p);
 figures+=q.visuals.length+q.options.filter(o=>o.image).length;
 const article=readable.match(new RegExp('<article id="'+q.id+'">([\\s\\S]*?)</article>'))?.[1];assert.ok(article,q.id);
 if(q.author)assert.ok(!article.includes(q.author),'Author leaked into readable archive: '+q.id);
 assert.ok(!q.transcriptionNotes.some(s=>/doğru\s+(?:şık|seçenek)\s*:?\s*[A-E]\b/iu.test(s)));
}
assert.equal(figures,31);
assert.ok(k2.find(q=>q.id==='imu-d1-k2-2022-2023-q028').stem.toLocaleLowerCase('tr').includes('doğrudur'));
assert.equal(k2.find(q=>q.id==='imu-d1-k2-2025-2026-q005').options[0].text,'Promoter');
assert.equal(k2.filter(q=>q.subjectProvenance==='missing_in_source').length,93);
assert.equal(C.select(all,{committee:'2',subject:'Ders belirtilmemiş'}).length,93);
for(const q of k1)assert.equal(C.committeeOf(q),1);
assert.equal(C.select(all,{committee:'1',year:'2026-2027'}).length,90);
assert.equal(C.select(all,{committee:'2',year:'2026-2027'}).length,0);
for(const id of ['committee-filter','committee-field','year-filter','start-session'])assert.ok(html.includes('id="'+id+'"'));
assert.ok(!read('js/app.js').includes('q.author'),'Author displayed in UI');
const report={passed:true,archiveQuestions:1010,committee1:541,committee2:469,newReviewQuestions:10,generatedQuestions:180,filterCombinations:matrices,newOptionChecks:options,newFigures:figures,regressionNormalDogruPreserved:true,unknownSubjectsNotInvented:true};
const out=path.join(root,'_work/reports');fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'kurul2-check.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
