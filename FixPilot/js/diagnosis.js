document.addEventListener('DOMContentLoaded', async () => {
  FixPilot.setupNavigation();
  const categoryId = document.body.dataset.category;
  const title = document.getElementById('diagnosticTitle');
  const description = document.getElementById('diagnosticDescription');
  const kicker = document.getElementById('categoryKicker');
  const list = document.getElementById('sequenceList');
  const errorBox = document.getElementById('errorBox');
  const busy = document.getElementById('busy');
  let category;
  let activeSequence = 0;
  let completedSequences = new Set();
  let values = {};

  const showError = message => { errorBox.textContent = message; errorBox.hidden = false; };
  const saveDiagnosticContext = () => {
    if (!category) return;
    const current = (category.sequences || [])[activeSequence] || {};
    sessionStorage.setItem('fixpilot-diagnostic-context', JSON.stringify({
      category: category.id,
      categoryName: category.name,
      step: current.title || '',
      stepDescription: current.description || '',
      answers: values
    }));
  };
  const sequences = () => category.sequences || [{ title: 'Diagnostic details', description: category.description, fields: category.features.map(field => field.name) }];

  function renderField(field) {
    const value = values[field.name];
    if (field.type === 'boolean') return `<label class="field-card toggle-field"><span><strong>${FixPilot.esc(field.label)}</strong><small>Turn on if you have noticed this symptom</small></span><input type="checkbox" name="${FixPilot.esc(field.name)}" ${value ? 'checked' : ''}><i></i></label>`;
    if (field.type === 'select') return `<label class="field-card"><span>${FixPilot.esc(field.label)}</span><select name="${FixPilot.esc(field.name)}">${field.options.map(option => `<option value="${FixPilot.esc(option)}" ${value === option ? 'selected' : ''}>${FixPilot.esc(option.replaceAll('_', ' '))}</option>`).join('')}</select></label>`;
    return `<label class="field-card"><span>${FixPilot.esc(field.label)}</span><div><input type="number" name="${FixPilot.esc(field.name)}" value="${value}" min="${field.min}" max="${field.max}" step="any" required><small>${FixPilot.esc(field.unit || '')}</small></div></label>`;
  }

  function bindValues() {
    list.querySelectorAll('input, select').forEach(input => input.addEventListener('input', () => {
      values[input.name] = input.type === 'checkbox' ? input.checked : input.type === 'number' ? Number(input.value) : input.value;
    }));
  }

  function renderJourney() {
    const currentSequences = sequences();
    const fields = Object.fromEntries(category.features.map(field => [field.name, field]));
    document.getElementById('progressFill').style.width = `${(completedSequences.size / currentSequences.length) * 100}%`;
    document.getElementById('progressText').textContent = `${completedSequences.size} of ${currentSequences.length} sections complete`;
    document.getElementById('progressList').innerHTML = currentSequences.map((sequence, index) => `<li class="${index === activeSequence ? 'active' : ''} ${completedSequences.has(index) ? 'done' : ''}"><button type="button" data-open="${index}"><span>${String(index + 1).padStart(2, '0')}</span>${FixPilot.esc(sequence.title)}<b>${completedSequences.has(index) ? '✓' : index === activeSequence ? '•' : '›'}</b></button></li>`).join('');
    list.innerHTML = currentSequences.map((sequence, index) => {
      const expanded = index === activeSequence;
      const final = index === currentSequences.length - 1;
      const fieldsHtml = expanded ? sequence.fields.map(name => renderField(fields[name])).join('') : '';
      return `<section class="sequence ${expanded ? 'expanded' : ''}" id="sequence-${index}"><button class="sequence-head" type="button" data-open="${index}" aria-expanded="${expanded}"><span class="sequence-mark">${FixPilot.sequenceIcon(sequence.title)}<em>${String(index + 1).padStart(2, '0')}</em></span><span><strong>${FixPilot.esc(sequence.title)}</strong><small>${FixPilot.esc(sequence.description)}</small></span><b>${FixPilot.icon('chevron', 'chevron-icon')}</b></button><div class="sequence-body"><div>${expanded ? `<div class="sequence-fields">${fieldsHtml}</div><div class="sequence-actions"><span>Complete this step to continue your diagnostic journey.</span><button type="button" class="button primary" data-continue="${index}">${final ? 'Run FixPilot diagnosis' : 'Continue'} <b>→</b></button></div>` : ''}</div></div></section>`;
    }).join('');
    document.querySelectorAll('[data-open]').forEach(button => button.addEventListener('click', () => { activeSequence = Number(button.dataset.open); renderJourney(); }));
    document.querySelectorAll('[data-continue]').forEach(button => button.addEventListener('click', () => continueSequence(Number(button.dataset.continue))));
    bindValues();
    const explainArea = document.querySelector('.sequence-actions');
    if (explainArea) {
      const explainLink = document.createElement('a');
      const current = currentSequences[activeSequence];
      explainLink.className = 'sequence-explain-link';
      explainLink.href = '/understanding?topic=' + encodeURIComponent(category.id)
        + '&question=' + encodeURIComponent('Why is FixPilot asking me to check ' + current.title + '?');
      explainLink.textContent = 'Why am I doing this?';
      explainArea.appendChild(explainLink);
    }
    saveDiagnosticContext();
  }

  function validateSequence(index) {
    const fieldMap = Object.fromEntries(category.features.map(field => [field.name, field]));
    for (const name of sequences()[index].fields) {
      const field = fieldMap[name];
      const value = values[name];
      if (field.type === 'number' && (!Number.isFinite(value) || value < field.min || value > field.max)) return `Enter a valid ${field.label.toLowerCase()} (${field.min}–${field.max}${field.unit || ''}).`;
      if (field.type === 'select' && !field.options.includes(value)) return `Choose a valid option for ${field.label.toLowerCase()}.`;
    }
    return '';
  }

  async function continueSequence(index) {
    const message = validateSequence(index);
    if (message) { showError(message); document.getElementById(`sequence-${index}`).scrollIntoView({ behavior: 'smooth', block: 'center' }); return; }
    errorBox.hidden = true;
    completedSequences.add(index);
    if (index < sequences().length - 1) {
      activeSequence = index + 1;
      renderJourney();
      document.getElementById(`sequence-${activeSequence}`).scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }
    renderJourney();
    busy.hidden = false;
    try {
      const response = await fetch('/diagnose', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ category: category.id, data: values }) });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || 'FixPilot could not complete this diagnosis.');
      sessionStorage.setItem('fixpilot-result', JSON.stringify({ ...result, categoryId: category.id }));
      window.location.assign('/results');
    } catch (error) {
      showError(error.message || 'FixPilot could not complete this diagnosis.');
    } finally {
      busy.hidden = true;
    }
  }

  try {
    const response = await fetch(`/categories/${encodeURIComponent(categoryId)}`, { headers: { Accept: 'application/json' } });
    if (!response.ok) throw new Error('This diagnostic system is unavailable.');
    category = await response.json();
    if (!category.available) throw new Error('This diagnostic model is not currently available.');
    values = Object.fromEntries(category.features.map(field => [field.name, field.type === 'boolean' ? false : field.default]));
    document.title = `${category.name} diagnosis | FixPilot`;
    kicker.innerHTML = `${FixPilot.categoryIcon(category.id)}<span>${FixPilot.esc(category.name.toUpperCase())}</span>`;
    title.textContent = `${category.name} diagnosis`;
    description.textContent = "Let's identify what is causing the problem, one focused step at a time.";
    renderJourney();
    FixPilotAssistant.mount({ category: category.id, target: document.querySelector('.diagnostic') });
  } catch (error) {
    showError(error.message || 'FixPilot could not load this diagnostic system.');
  }
});
