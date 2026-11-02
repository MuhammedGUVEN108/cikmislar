/* DOM simulation, not a browser or visual layout test. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const ctx={console,URLSearchParams};ctx.window=ctx;ctx.globalThis=ctx;vm.createContext(ctx);
for(const [,src] of html.matchAll(/<script\b[^>]*src="([^"]+)"/g))if(src.startsWith('js/')&&src!=='js/app.js')vm.runInContext(fs.readFileSync(path.join(root,src),'utf8'),ctx);
let doc;
class Node {
 constructor(tag='DIV'){this.tagName=tag.toUpperCase();this.children=[];this.dataset={};this.style={};this.attrs={};this.events={};this.value='';this.checked=true;this.hidden=false;this.open=false;this.scrollTop=0;this.clientHeight=900;this.scrollHeight=500;this._text='';const classes=new Set();this.classList={add:(...v)=>v.forEach(x=>classes.add(x)),remove:(...v)=>v.forEach(x=>classes.delete(x)),contains:v=>classes.has(v)};}
 append(...nodes){this.children.push(...nodes);}
 replaceChildren(...nodes){this.children=[...nodes];this._text='';}
 get childElementCount(){return this.children.length;}
 get options(){return this.children;}
 set textContent(v){this._text=String(v);this.children=[];}
 get textContent(){return this._text+this.children.map(c=>typeof c==='string'?c:c.textContent).join('');}
 set innerHTML(v){this.textContent=String(v).replace(/<[^>]*>/g,'');}
 setAttribute(k,v){this.attrs[k]=String(v);}
 removeAttribute(k){delete this.attrs[k];}
 getAttribute(k){return this.attrs[k];}
 addEventListener(k,f){(this.events[k]??=[]).push(f);}
 emit(k,extra={}){for(const f of this.events[k]||[])f({preventDefault(){},target:this,...extra});}
 click(){if(!this.disabled)this.emit('click');}
 focus(){doc.activeElement=this;}
 showModal(){this.open=true;}
 close(){this.open=false;}
 querySelector(selector){const m=selector.match(/^\[data-(subject|label)="([^"]*)"\]$/);if(!m)throw Error('Unsupported test selector '+selector);return this.children.find(c=>c.dataset?.[m[1]]===m[2])||null;}
}
const nodes=new Map();for(const [,id] of html.matchAll(/\bid="([^"]+)"/g))nodes.set(id,new Node());
for(const [,id,body] of html.matchAll(/<select\b[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/select>/g)){
 const el=nodes.get(id);el.tagName='SELECT';
 for(const [,value,attrs,text] of body.matchAll(/<option\s+value="([^"]*)"([^>]*)>([^<]*)<\/option>/g)){const o=new Node('OPTION');o.value=value;o.textContent=text;el.append(o);if(attrs.includes('selected'))el.value=value;}
}
doc={documentElement:{dataset:{theme:'light'}},activeElement:null,getElementById:id=>{assert.ok(nodes.has(id),'Missing HTML ID '+id);return nodes.get(id);},createElement:tag=>new Node(tag),querySelector:s=>s==='meta[name="theme-color"]'?{}:null,addEventListener(){}};
ctx.document=doc;ctx.location={search:'?kurul=2'};ctx.scrollTo=()=>{};ctx.requestAnimationFrame=f=>f();ctx.addEventListener=()=>{};
vm.runInContext(fs.readFileSync(path.join(root,'js/app.js'),'utf8'),ctx,{filename:'app.js'});
const $=id=>nodes.get(id),change=(id,value)=>{$(id).value=value;$(id).emit('change');};
assert.equal($('filtered-count').textContent,'469');$('release-continue').click();
change('year-filter','2021-2022');assert.equal($('filtered-count').textContent,'95');
$('start-session').click();assert.ok($('question-source').textContent.startsWith('2. Kurul'));
const q1=ctx.QUESTION_DATA.find(q=>q.id==='imu-d1-k2-2021-2022-q001');
$('question-options').querySelector('[data-label="'+q1.sourceKeys[0]+'"]').click();assert.equal($('correct-count').textContent,'1');
const wrong=q1.sourceKeys[0]==='A'?'B':'A';$('question-options').querySelector('[data-label="'+wrong+'"]').click();assert.equal($('correct-count').textContent,'1');assert.equal($('wrong-count').textContent,'0');
$('next-question').click();assert.ok($('question-warning').textContent.includes('eksik'));
$('question-options').querySelector('[data-label="A"]').click();assert.equal($('review-count').textContent,'1');assert.equal($('wrong-count').textContent,'0');
for(let i=0;i<16;i++)$('next-question').click();assert.ok($('question-visuals').childElementCount>0,'Question 18 source table missing');
$('generated-mode-toggle').click();assert.ok($('committee-field').hidden);assert.equal($('filtered-count').textContent,'90');
$('generated-back').click();assert.equal($('committee-filter').value,'2');assert.equal($('year-filter').value,'2021-2022');assert.equal($('review-count').textContent,'1');
$('back-to-setup').click();change('committee-filter','1');assert.equal($('filtered-count').textContent,'91');
change('year-filter','2026-2027');assert.equal($('filtered-count').textContent,'90');
change('committee-filter','2');assert.equal($('year-filter').value,'');assert.equal($('filtered-count').textContent,'469');
$('reset-filters').click();assert.equal($('filtered-count').textContent,'1010');
change('committee-filter','2');change('year-filter','2022-2023');assert.equal($('filtered-count').textContent,'93');
$('subject-filters').querySelector('[data-subject="Ders belirtilmemiş"]').click();assert.equal($('filtered-count').textContent,'93');
$('start-session').click();assert.equal($('question-subject').textContent,'Ders belirtilmemiş');
$('open-question-info').click();assert.ok($('question-info-dialog').open);$('source-details').open=true;$('source-details').emit('toggle');assert.ok($('source-images').childElementCount>0);
assert.ok(!$('question-source').textContent.includes('Soru sahibi'));
const report={passed:true,method:'Node VM DOM simulation; NOT a browser/visual test',checks:['deep link kurul=2','committee/year/subject filters','first answer locks','incomplete source review only','source table render model','generated mode separate','archive session restored','unsupported year resets','reset all committees','unknown subject filter','source dialog']};
fs.mkdirSync(path.join(root,'_work/reports'),{recursive:true});fs.writeFileSync(path.join(root,'_work/reports/kurul2-ui-check.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
