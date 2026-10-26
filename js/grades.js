(function (root) {
  'use strict';
  const components = Object.freeze([
    { id: 'k1', label: 'Kurul 1', weight: 0.11 },
    { id: 'k2', label: 'Kurul 2', weight: 0.09 },
    { id: 'k3', label: 'Kurul 3', weight: 0.11 },
    { id: 'k4', label: 'Kurul 4', weight: 0.11 },
    { id: 'k5', label: 'Kurul 5', weight: 0.12 },
    { id: 'science', label: 'Bilimsellik', weight: 0.03 },
    { id: 'ihu', label: 'İHU', weight: 0.03 }
  ].map(Object.freeze));
  const validScore = value => value === null || (Number.isFinite(value) && value >= 0 && value <= 100);
  const roundUp = value => Math.ceil((value - 1e-10) * 100) / 100;
  const thresholds = Object.freeze({ exemption: 79.5, passWithFinal: 59.5 });
  function calculate(scores, finalScore = null) {
    if (!Array.isArray(scores) || scores.length !== 7 || !scores.every(validScore) || !validScore(finalScore)) throw new Error('Notlar 0–100 arasında olmalı.');
    let sum = 0, weight = 0, count = 0;
    components.forEach((component, index) => {
      if (scores[index] !== null) { sum += scores[index] * component.weight; weight += component.weight; count++; }
    });
    const complete = count === 7;
    const average = count ? sum / weight : null;
    const exempt = complete && sum >= thresholds.exemption * 0.60 - 1e-9;
    const remaining = complete || !count ? null : roundUp((thresholds.exemption * 0.60 - sum) / (0.60 - weight));
    const finalNeeded = complete ? Math.max(0, roundUp((thresholds.passWithFinal - sum) / 0.40)) : null;
    const total = complete && finalScore !== null ? sum + finalScore * 0.40 : null;
    return { count, complete, average, exempt, remaining, finalNeeded, total, passedWithFinal: total === null ? null : total >= thresholds.passWithFinal - 1e-9 };
  }
  root.GradeCalculator = Object.freeze({ components, thresholds, calculate });
  if (!root.document) return;
  const $ = id => root.document.getElementById(id);
  if (!$('grade-form')) return;
  const fields = [];
  for (const component of components) {
    const row = document.createElement('div'); row.className = 'grade-entry';
    const label = document.createElement('label'); label.htmlFor = 'grade-' + component.id; label.textContent = component.label;
    const hint = document.createElement('span'); hint.className = 'field-hint'; hint.textContent = `Yıl sonuna katkı: %${Math.round(component.weight * 100)}`;
    label.append(hint);
    const input = document.createElement('input'); input.id = 'grade-' + component.id; input.className = 'wd-input'; input.type = 'text'; input.inputMode = 'decimal'; input.maxLength = 6; input.placeholder = '0–100'; input.setAttribute('aria-describedby', 'grade-error');
    row.append(label, input); $('grade-inputs').append(row); fields.push(input);
  }
  const format = new Intl.NumberFormat('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 4 });
  function parse(input) {
    const raw = input.value.trim();
    const value = raw === '' ? null : Number(raw.replace(',', '.'));
    const valid = raw === '' || (/^\d{1,3}(?:[.,]\d{1,2})?$/.test(raw) && validScore(value));
    input.setAttribute('aria-invalid', String(!valid));
    return { valid, value };
  }
  function update() {
    const inputs = [...fields, $('grade-final')].map(parse);
    const valid = inputs.every(input => input.valid);
    $('grade-error').hidden = valid;
    $('grade-error').textContent = valid ? '' : 'Notları 0–100 arasında, en fazla iki ondalık basamakla gir.';
    if (!valid) {
      for (const id of ['grade-average', 'grade-exemption', 'grade-final-needed']) $(id).textContent = '—';
      $('grade-completeness').textContent = 'İşaretli notu düzelt.';
      $('grade-exemption-note').textContent = 'Geçersiz not varken sonuç hesaplanmaz.';
      $('grade-final-note').textContent = 'Geçersiz not varken sonuç hesaplanmaz.';
      $('grade-total-card').hidden = true;
      return;
    }
    const result = calculate(inputs.slice(0, 7).map(input => input.value), inputs[7].value);
    $('grade-average-label').textContent = result.complete ? 'Yıl içi ortalaman' : 'Girilen notların ortalaması';
    $('grade-average').textContent = result.average === null ? '—' : format.format(result.average);
    $('grade-completeness').textContent = result.complete ? 'Yedi notun ağırlıklı ortalaması.' : `${result.count} / 7 not girildi. Eksik notlar hesap dışında.`;
    if (!result.count) {
      $('grade-exemption').textContent = '—';
      $('grade-exemption-note').textContent = 'Notlarını girdikçe kalan hedefin hesaplanır.';
    } else if (result.complete) {
      $('grade-exemption').textContent = result.exempt ? 'Hedef sağlandı' : '79,5’in altında';
      $('grade-exemption-note').textContent = result.exempt ? '79,5 ve üzeri 80 barajını karşılar; finalsiz geçiş hedefi sağlandı.' : 'Finalle 59,5 → 60 hedefi için gereken not aşağıda.';
    } else if (result.remaining > 100) {
      $('grade-exemption').textContent = '100’ü aşıyor';
      $('grade-exemption-note').textContent = 'Kalan notlarda 100 ortalama bile finalsiz 79,5 → 80 barajına yetmiyor.';
    } else if (result.remaining <= 0) {
      $('grade-exemption').textContent = 'Hedef karşılanıyor';
      $('grade-exemption-note').textContent = 'Girdiğin notların katkısı 79,5 → 80 barajı için yeterli; eksik notları da tamamla.';
    } else {
      $('grade-exemption').textContent = format.format(result.remaining);
      $('grade-exemption-note').textContent = 'Kalan notlarının ağırlıklı ortalaması en az bu kadar olmalı.';
    }
    if (!result.complete) {
      $('grade-final-needed').textContent = '—'; $('grade-final-note').textContent = 'Yıl içindeki yedi not tamamlanınca hesaplanır.';
    } else if (result.exempt) {
      $('grade-final-needed').textContent = 'Gerek yok'; $('grade-final-note').textContent = 'Finalsiz geçiş için 79,5 → 80 barajı sağlandı.';
    } else if (result.finalNeeded > 100) {
      $('grade-final-needed').textContent = '100’ü aşıyor'; $('grade-final-note').textContent = 'Bu yıl içi notlarla finalden 100 almak toplamı 59,5 barajına ulaştırmıyor.';
    } else {
      $('grade-final-needed').textContent = format.format(result.finalNeeded); $('grade-final-note').textContent = 'Final dahil toplamın en az 59,5 olması için gereken not; 59,5 ve üzeri 60 barajını karşılar.';
    }
    $('grade-total-card').hidden = result.total === null || result.exempt;
    if (result.total !== null) {
      $('grade-total').textContent = format.format(result.total);
      $('grade-total-note').textContent = result.passedWithFinal ? '59,5 ve üzeri: 60 barajı sağlanıyor.' : 'Final dahil sonuç 59,5 barajının altında.';
    }
  }
  for (const input of [...fields, $('grade-final')]) input.addEventListener('input', update);
  $('grade-clear').addEventListener('click', () => { for (const input of [...fields, $('grade-final')]) input.value = ''; update(); });
  $('grade-form').addEventListener('submit', event => event.preventDefault());
  update();
})(typeof window !== 'undefined' ? window : globalThis);
