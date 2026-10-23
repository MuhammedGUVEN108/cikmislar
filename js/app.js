(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const C = window.QuizCore;
  const all = window.QUESTION_DATA;
  if (!C || !Array.isArray(all) || all.length === 0) {
    $('loading-message').textContent = 'Soru dosyası yüklenemedi. Klasörü eksiksiz kopyalayıp sayfayı yeniden açın. Okunabilir arşiv: soru-arsivi.html';
    return;
  }
  const subjects = [...new Set(all.map(q => q.subject))].sort((a,b) => a.localeCompare(b,'tr'));
  const years = [...new Set(all.map(q => q.year))].sort();
  let selectedSubject = '';
  let session = [];
  let answers = new Map();
  let position = 0;
  let view = 'setup';
  let sessionLabel = '';
  const filters = () => ({ year: $('year-filter').value, subject: selectedSubject, includeReview: $('review-filter').checked });
  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function scrollTop() { window.scrollTo({ top: 0, behavior: 'instant' }); }
  function fitQuestion() {
    if (view !== 'study') return;
    const reader=$('question-reader');
    const previousTop=reader.scrollTop || 0;
    reader.dataset.density='normal';
    if (reader.clientHeight > 0 && reader.scrollHeight > reader.clientHeight + 2) reader.dataset.density='compact';
    reader.scrollTop=previousTop;
  }
  function scheduleFit() {
    if (typeof window.requestAnimationFrame === 'function') window.requestAnimationFrame(fitQuestion);
    else fitQuestion();
  }
  function openQuestionInfo(showSource=false) {
    if (!session[position]) return;
    $('question-info-title').textContent=`${session[position].year} · Soru ${session[position].number}`;
    if (!$('question-info-dialog').open) $('question-info-dialog').showModal();
    if (showSource) { $('source-details').open=true;loadSource(session[position]); }
  }
  function setView(name) {
    view = name;
    document.documentElement.dataset.view=name;
    $('secim').hidden = name !== 'setup';
    $('cozum').hidden = name !== 'study';
    $('sonuc').hidden = name !== 'results';
    $('not-hesaplama').hidden = name !== 'grades';
    for (const [id, active] of [['nav-setup',name === 'setup'],['nav-study',name === 'study' || name === 'results'],['nav-grades',name === 'grades']]) {
      if (active) $(id).setAttribute('aria-current','location');
      else $(id).removeAttribute('aria-current');
    }
    scrollTop();
  }
  function updateFilters() {
    const f = filters();
    const selected = C.select(all,f);
    const graded = selected.filter(q => C.gradingKey(q)).length;
    $('filtered-count').textContent = selected.length;
    $('selection-description').textContent = `${f.year || 'Bütün yıllar'} · ${f.subject || 'Bütün dersler'}`;
    $('set-breakdown').textContent = `${graded} cevap anahtarlı · ${selected.length - graded} puan dışı`;
    $('start-session').disabled = selected.length === 0;
    const pool = C.select(all,{year:f.year,includeReview:f.includeReview});
    const list = $('subject-filters'); list.replaceChildren();
    for (const [index, subject] of ['',...subjects].entries()) {
      const count = subject ? pool.filter(q=>q.subject===subject).length : pool.length;
      const button = element('button','subject-choice');
      button.type = 'button'; button.dataset.subject = subject;
      button.setAttribute('aria-pressed',String(selectedSubject===subject));
      button.append(element('span','subject-index',String(index).padStart(2,'0')),element('span','subject-name',subject || 'Bütün dersler'),element('span','subject-count',count));
      button.addEventListener('click',()=>{selectedSubject=subject;updateFilters();$('subject-filters').querySelector(`[data-subject="${subject}"]`)?.focus();});
      list.append(button);
    }
  }
  function start(items, label) {
    if (!items.length) return;
    session = [...items]; answers = new Map(); position = 0; sessionLabel = label;
    $('bank-search').value = '';
    setView('study'); renderQuestion(true);
  }
  function updateStats() {
    const stats = C.summarize(session,answers);
    $('correct-count').textContent = stats.correct;
    $('wrong-count').textContent = stats.wrong;
    $('review-count').textContent = stats.review;
    $('answered-count').textContent = `${stats.answered} / ${stats.total} cevaplandı`;
    $('session-progress').style.width = `${stats.total ? stats.answered / stats.total * 100 : 0}%`;
  }
  function renderQuestion(focus = false) {
    const q = session[position];
    if (!q) return;
    const answer = answers.get(q.id);
    const reader=$('question-reader');
    const previousTop=focus ? 0 : reader.scrollTop || 0;
    reader.dataset.choiceLayout=q.options.filter(o=>o.image).length>=3 ? 'images' : 'text';
    const reason = C.reviewReason(q);
    $('session-context').textContent = sessionLabel;
    $('question-position').textContent = `SORU ${String(position + 1).padStart(2,'0')} / ${session.length}`;
    $('question-subject').textContent = q.subject;
    $('question-source').textContent = `${q.year} · Soru ${q.number}`;
    $('question-stem').textContent = q.stem;
    const aiSupport = $('ai-support');
    if (aiSupport.dataset.questionId !== q.id) aiSupport.open = false;
    aiSupport.dataset.questionId = q.id;
    $('ai-explanation').textContent = q.aiExplanation || 'Bu soru için AI açıklaması eklenmedi.';
    $('question-id').textContent = q.id;
    $('question-pages').textContent = `Kaynak sayfa: ${q.pages.join(', ')}`;
    $('question-warning').hidden = !reason;
    $('question-warning').textContent = reason ? `${reason}.${C.gradingKey(q) ? '' : ' Doğru/yanlış sayısına katılmaz.'}` : '';
    $('source-details').open = false;
    $('source-images').replaceChildren();
    const visuals = $('question-visuals'); visuals.replaceChildren();
    for (const [i,src] of q.visuals.entries()) {
      const figure = element('figure','visual-figure');
      const link = element('a'); link.href = src; link.target='_blank'; link.rel='noopener noreferrer';
      const caption=q.visualCaptions[i] || `Kaynak şekli ${i+1}`;
      const img = element('img'); img.src=src; img.alt=`${q.year}, soru ${q.number}: ${caption}`; img.decoding='async';img.addEventListener('load',scheduleFit);
      link.append(img); figure.append(link,element('figcaption','',`${caption} · Büyütmek için dokun.`)); visuals.append(figure);
    }
    if (q.needsVisual && q.visuals.length === 0 && !q.options.some(o=>o.image)) {
      const hint = element('div','visual-hint');
      const button = element('button','text-button','Kaynak görseli (cevap işaretli olabilir) ↗'); button.type='button';
      button.addEventListener('click',()=>openQuestionInfo(true));
      hint.append(button); visuals.append(hint);
    }
    const options = $('question-options'); options.replaceChildren();
    for (const option of q.options) {
      const button = element('button','option'); button.type='button'; button.dataset.label = option.label;
      button.setAttribute('aria-pressed',String(answer?.selected === option.label));
      button.setAttribute('aria-disabled',String(Boolean(answer)));
      let text = option.text || 'Bu şık kaynakta okunamıyor.';
      if (option.imageOnly && !option.text) text = 'Şekil kaynak görselinde';
      const body=element('span','option-text',option.image ? '' : text);
      if (option.image) {const img=element('img','option-image');img.src=option.image;img.alt=`${option.label} şıkkındaki yapı`;img.addEventListener('load',scheduleFit);body.append(img);}
      button.append(element('span','option-letter',option.label),body);
      if (answer) {
        if (answer.key === option.label) { button.classList.add('correct'); button.append(element('span','option-state','✓ Doğru')); }
        if (answer.selected === option.label && answer.result === 'wrong') { button.classList.add('wrong'); button.append(element('span','option-state','× Yanlış')); }
        if (answer.selected === option.label && answer.result === 'review') { button.classList.add('review-selected'); button.append(element('span','option-state','! Seçimin')); }
      }
      button.addEventListener('click',()=>{
        if (answers.has(q.id)) return;
        answers.set(q.id,C.evaluate(q,option.label));renderQuestion();
        $('question-options').querySelector(`[data-label="${option.label}"]`)?.focus({preventScroll:true});
      });
      options.append(button);
    }
    const feedback = $('answer-feedback'); feedback.className='answer-feedback'; feedback.textContent='';
    if (answer) {
      feedback.classList.add(answer.result);
      if (answer.result === 'correct') feedback.textContent=`✓ Doğru. Kaynak anahtarı: ${answer.key}.`;
      else if (answer.result === 'wrong') feedback.textContent=`× Yanlış. Seçimin ${answer.selected}; kaynak anahtarı ${answer.key}.`;
      else feedback.textContent=q.status==='cancelled'?'! İptal edilmiş soru; doğru/yanlış sayısına katılmaz.':'! Kaynak cevap anahtarı yok veya okunamıyor; doğru/yanlış sayısına katılmaz.';
    }
    const notes = $('answer-notes'); notes.replaceChildren(); notes.hidden=!answer;
    if (answer) {
      for (const text of q.correctionNotes) notes.append(element('p','',text));
      if (!notes.childElementCount) notes.hidden=true;
    }
    $('previous-question').disabled=position===0;
    $('next-question').textContent=position===session.length-1?'Sonuçları gör →':'Sonraki soru →';
    updateStats();
    fitQuestion();reader.scrollTop=previousTop;
    if (focus) {$('question-stem').focus({preventScroll:true});}
    scheduleFit();
  }
  function loadSource(q) {
    const container=$('source-images');if(container.childElementCount)return;
    for (const [i,src] of q.sourceImages.entries()) {
      const figure=element('figure','source-page');const img=element('img');img.src=src;img.alt=`${q.year} kaynak sayfa ${q.pages[i] ?? q.pages[0]}`;img.loading='lazy';
      const a=element('a','',`Kaynak sayfa ${q.pages[i] ?? q.pages[0]} · Ayrı sekmede büyüt ↗`);a.href=src;a.target='_blank';a.rel='noopener noreferrer';
      figure.append(img,element('figcaption','',`Bu tam sayfada aradığın soru: ${q.number}.`),a);container.append(figure);
    }
  }
  function renderResults() {
    const s=C.summarize(session,answers);setView('results');
    $('results-description').textContent=`${sessionLabel} · ${s.total} sorunun ${s.answered} tanesini cevapladın.`;
    const box=$('results-stats');box.replaceChildren();
    for(const [label,value] of [['Doğru',s.correct],['Yanlış',s.wrong],['Puan dışı',s.review],['Cevaplanmadı',s.unanswered]]){
      const item=element('div','result-stat');item.append(element('strong','',value),element('span','',label));box.append(item);
    }
    $('retry-wrong').disabled=s.wrong===0;
    $('results-title').focus({preventScroll:true});
  }
  function renderBank() {
    const query=C.normalize($('bank-search').value).trim();const grid=$('bank-grid');grid.replaceChildren();
    session.forEach((q,index)=>{
      if(query && !C.normalize(`${q.stem} ${q.subject} ${q.year} ${q.number} ${q.id} ${q.options.map(o=>o.text||'').join(' ')}`).includes(query))return;
      const a=answers.get(q.id);const mark=a ? {correct:'✓',wrong:'×',review:'!'}[a.result] : '·';
      const b=element('button',`bank-cell ${a?.result||''}`,`${index+1} ${mark}`);b.type='button';
      b.append(element('span','',`${q.year.slice(2,4)}–${q.year.slice(7)} / ${q.number}`));
      b.setAttribute('aria-label',`${index+1}. soru, ${q.year}, kaynak soru ${q.number}, ${q.subject}, ${a?{correct:'doğru',wrong:'yanlış',review:'puan dışı'}[a.result]:'cevaplanmadı'}`);
      if(position===index)b.setAttribute('aria-current','step');
      b.addEventListener('click',()=>{position=index;$('bank-dialog').close();setView('study');renderQuestion(true);});grid.append(b);
    });
    $('bank-empty').hidden=grid.childElementCount>0;
  }
  function openBank(){if(!session.length)$('start-session').click();if(!session.length)return;renderBank();if(!$('bank-dialog').open)$('bank-dialog').showModal();}
  for(const year of years){const o=element('option','',year);o.value=year;$('year-filter').append(o);}
  $('year-filter').addEventListener('change',updateFilters);
  $('review-filter').addEventListener('change',updateFilters);
  $('reset-filters').addEventListener('click',()=>{$('year-filter').value='';selectedSubject='';$('review-filter').checked=true;$('order-filter').value='ordered';updateFilters();});
  $('start-session').addEventListener('click',()=>{const f=filters();const items=C.select(all,f);start($('order-filter').value==='random'?C.shuffle(items):items,`${f.year||'Bütün yıllar'} · ${f.subject||'Bütün dersler'}`);});
  for(const id of ['back-to-setup','new-selection'])$(id).addEventListener('click',()=>setView('setup'));
  $('nav-setup').addEventListener('click',e=>{e.preventDefault();setView('setup');});
  $('nav-study').addEventListener('click',e=>{e.preventDefault();if(!session.length){$('start-session').click();}else{setView('study');renderQuestion(true);}});
  $('nav-bank').addEventListener('click',e=>{e.preventDefault();openBank();});
  $('nav-grades').addEventListener('click',e=>{e.preventDefault();setView('grades');$('grades-title').focus({preventScroll:true});});
  $('show-bank').addEventListener('click',openBank);
  $('close-bank').addEventListener('click',()=>$('bank-dialog').close());
  $('open-question-info').addEventListener('click',()=>openQuestionInfo());
  $('close-question-info').addEventListener('click',()=>$('question-info-dialog').close());
  $('bank-search').addEventListener('input',renderBank);
  $('source-details').addEventListener('toggle',()=>{if($('source-details').open && session[position])loadSource(session[position]);});
  $('ai-support').addEventListener('toggle',scheduleFit);
  $('previous-question').addEventListener('click',()=>{if(position>0){position--;renderQuestion(true);}});
  $('next-question').addEventListener('click',()=>{if(position<session.length-1){position++;renderQuestion(true);}else renderResults();});
  $('finish-session').addEventListener('click',renderResults);
  $('continue-session').addEventListener('click',()=>{setView('study');renderQuestion(true);});
  $('retry-all').addEventListener('click',()=>start(session,sessionLabel));
  $('retry-wrong').addEventListener('click',()=>start(session.filter(q=>answers.get(q.id)?.result==='wrong'),`${sessionLabel} · Yanlışlar`));
  $('theme-toggle').addEventListener('click',()=>{const dark=document.documentElement.dataset.theme!=='dark';document.documentElement.dataset.theme=dark?'dark':'light';$('theme-label').textContent=dark?'Açık tema':'Koyu tema';for(const id of ['theme-toggle','study-theme-toggle'])$(id).setAttribute('aria-label',dark?'Açık temaya geç':'Koyu temaya geç');document.querySelector('meta[name="theme-color"]').content=dark?'#262624':'#f3efe4';});
  $('study-theme-toggle').addEventListener('click',()=>$('theme-toggle').click());
  document.addEventListener('keydown',e=>{if(view!=='study'||$('bank-dialog').open||$('question-info-dialog').open||e.altKey||e.ctrlKey||e.metaKey||['INPUT','SELECT','TEXTAREA','BUTTON'].includes(document.activeElement?.tagName))return;if(e.key==='ArrowRight'){e.preventDefault();$('next-question').click();}else if(e.key==='ArrowLeft'){e.preventDefault();$('previous-question').click();}});
  window.addEventListener('resize',scheduleFit);
  window.visualViewport?.addEventListener('resize',scheduleFit);
  window.addEventListener('pageshow',e=>{if(e.persisted){answers=new Map();session=[];position=0;setView('setup');}});
  $('release-close').addEventListener('click',()=>$('release-dialog').close());
  $('release-continue').addEventListener('click',()=>$('release-dialog').close());
  $('loading-message').hidden=true;updateFilters();setView('setup');
  $('release-dialog').showModal();
})();
