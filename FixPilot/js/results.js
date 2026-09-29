document.addEventListener('DOMContentLoaded', () => {
  FixPilot.setupNavigation();
  const result = JSON.parse(sessionStorage.getItem('fixpilot-result') || 'null');
  const content = document.getElementById('resultContent');
  const empty = document.getElementById('emptyResult');
  if (!result) { empty.hidden = false; return; }
  content.hidden = false;
  document.getElementById('resultCategory').textContent = result.category_name;
  const severity = document.getElementById('severity');
  severity.textContent = `Severity · ${result.severity || 'review'}`;
  severity.className = `severity ${result.severity || 'warn'}`;
  document.getElementById('diagTitle').textContent = result.diagnosis;
  document.getElementById('diagSub').textContent = result.description;
  document.getElementById('confNum').textContent = `${result.confidence}%`;
  document.getElementById('symptomList').innerHTML = result.symptoms.map(item => `<li>${FixPilot.esc(item)}</li>`).join('');
  document.getElementById('actionList').innerHTML = result.actions.map(item => `<li>${FixPilot.esc(item)}</li>`).join('');
  document.getElementById('whyText').textContent = `The ${result.model.algorithm} model found the strongest match between your submitted signals and “${result.diagnosis}”. Key reported signals include ${result.symptoms.slice(0, 3).join(', ').toLowerCase()}.`;
  document.getElementById('modelInfo').innerHTML = [['Algorithm', result.model.algorithm], ['Dataset', `${Number(result.model.samples).toLocaleString()} samples`], ['Features', result.model.features], ['Training accuracy', `${result.model.train_acc}%`], ['Test accuracy', `${result.model.test_acc}%`]].map(([label, value]) => `<div><dt>${label}</dt><dd>${value}</dd></div>`).join('');
  document.getElementById('again').href = FixPilot.pageFor(result.categoryId);
  document.getElementById('anotherCategory').addEventListener('click', () => sessionStorage.removeItem('fixpilot-result'));
  sessionStorage.setItem('fixpilot-diagnostic-context', JSON.stringify({
    category: result.categoryId,
    categoryName: result.category_name,
    result: {
      diagnosis: result.diagnosis,
      description: result.description,
      symptoms: result.symptoms,
      confidence: result.confidence
    }
  }));
  const understandResult = document.createElement('a');
  understandResult.className = 'button-link quiet';
  understandResult.href = '/understanding?topic=' + encodeURIComponent(result.categoryId)
    + '&question=' + encodeURIComponent('Please help me understand this FixPilot result and what it means: ' + result.diagnosis);
  understandResult.textContent = 'Understand this result';
  document.querySelector('.result-actions').prepend(understandResult);
  FixPilotAssistant.mount({ category: result.categoryId, target: document.querySelector('.result') });
});
