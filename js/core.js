(function (root) {
  'use strict';
  const allowedLabels = new Set(['A', 'B', 'C', 'D', 'E']);
  function normalize(value) {
    return String(value ?? '').toLocaleLowerCase('tr-TR').replace(/ı/g, 'i').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }
  function gradingKey(q) {
    if (q.origin === 'generated') return allowedLabels.has(q.authoredKey) ? q.authoredKey : null;
    if (q.status === 'cancelled' || q.sourceKeys.length !== 1) return null;
    return allowedLabels.has(q.sourceKeys[0]) ? q.sourceKeys[0] : null;
  }
  function reviewReason(q) {
    if (q.origin === 'generated') return gradingKey(q) ? '' : 'Deneme cevap anahtarı eksik';
    if (q.status === 'cancelled') return 'Bu soru kaynakta iptal edilmiş';
    if (!gradingKey(q)) return 'Kaynak cevap anahtarı yok veya okunamıyor';
    if (q.correctionNotes?.length) return 'Kaynakta bu soruya ilişkin düzeltme notu var';
    return '';
  }
  function select(questions, filters = {}) {
    return questions.filter(q => (!filters.year || q.year === filters.year) && (!filters.subject || q.subject === filters.subject) && (filters.includeReview !== false || gradingKey(q)));
  }
  function evaluate(q, label) {
    if (!allowedLabels.has(label) || !q.options.some(o => o.label === label)) throw new Error('Geçersiz şık');
    const key = gradingKey(q);
    return { selected: label, result: key ? (label === key ? 'correct' : 'wrong') : 'review', key };
  }
  function shuffle(items, random = Math.random) {
    const copy = [...items];
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }
  function summarize(questions, answers) {
    const out = { total: questions.length, correct: 0, wrong: 0, review: 0, answered: 0, unanswered: 0 };
    for (const q of questions) {
      const answer = answers.get(q.id);
      if (answer) { out[answer.result]++; out.answered++; }
      else out.unanswered++;
    }
    return out;
  }
  root.QuizCore = Object.freeze({ normalize, gradingKey, reviewReason, select, evaluate, shuffle, summarize });
})(typeof window !== 'undefined' ? window : globalThis);
