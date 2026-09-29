window.FixPilotAssistant = (() => {
  const render = (root, response) => {
    const sections = (response.sections || []).map(section => {
      const image = section.image ? `<figure class="learning-visual"><img src="${FixPilot.esc(section.image.url)}" alt="${FixPilot.esc(section.image.alt)}" loading="lazy"><figcaption>${FixPilot.esc(section.image.description)}</figcaption></figure>` : '';
      return `<article class="learning-section"><h3>${FixPilot.esc(section.title)}</h3>${image}<p>${FixPilot.esc(section.content)}</p></article>`;
    }).join('');
    const suggestions = (response.suggestedQuestions || []).map(question => `<button type="button" class="learning-suggestion" data-question="${FixPilot.esc(question)}">${FixPilot.esc(question)}</button>`).join('');
    root.querySelector('[data-learning-answer]').innerHTML = sections || `<p>${FixPilot.esc(response.answer || 'Ask a question to get a simple explanation.')}</p>`;
    root.querySelector('[data-learning-suggestions]').innerHTML = suggestions;
    root.querySelectorAll('[data-question]').forEach(button => button.addEventListener('click', () => {
      root.querySelector('[data-learning-input]').value = button.dataset.question;
      requestExplanation(root, button.dataset.question);
    }));
  };

  const requestExplanation = async (root, question = '') => {
    const status = root.querySelector('[data-learning-status]');
    status.textContent = 'Preparing a simple explanation…';
    try {
      const response = await fetch('/explain', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question, category: root.dataset.category }) });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || 'The explanation is unavailable right now.');
      render(root, payload);
      status.textContent = '';
    } catch (error) {
      root.querySelector('[data-learning-answer]').innerHTML = `<p class="learning-error">${FixPilot.esc(error.message || 'The explanation is unavailable right now.')}</p>`;
      status.textContent = '';
    }
  };

  const mount = ({ category = '', target }) => {
    const host = typeof target === 'string' ? document.querySelector(target) : target;
    if (!host || host.querySelector('.understanding-assistant')) return;
    const root = document.createElement('section');
    root.className = 'understanding-assistant';
    root.dataset.category = category;
    root.setAttribute('aria-labelledby', 'understandingTitle');
    root.innerHTML = `<div class="learning-heading"><span class="learning-mark">${FixPilot.icon('list')}</span><div><div class="eyebrow"><i></i> UNDERSTANDING ASSISTANT</div><h2 id="understandingTitle">Learn it in plain language.</h2><p>Ask about a part, symptom, or diagnostic term. FixPilot will use a relevant visual when one is available.</p></div></div><form class="learning-form" data-learning-form><label for="learningQuestion">What would you like to understand?</label><div><input id="learningQuestion" data-learning-input maxlength="280" placeholder="For example: What is RAM?" autocomplete="off"><button class="button primary" type="submit">Explain</button></div></form><p class="learning-status" data-learning-status aria-live="polite"></p><div class="learning-answer" data-learning-answer></div><div class="learning-suggestions" data-learning-suggestions aria-label="Suggested questions"></div>`;
    host.appendChild(root);
    const fullAssistant = document.createElement('a');
    fullAssistant.className = 'learning-full-link';
    fullAssistant.href = '/understanding?topic=' + encodeURIComponent(category);
    fullAssistant.textContent = 'Open full Understanding Assistant →';
    root.appendChild(fullAssistant);
    root.querySelector('[data-learning-form]').addEventListener('submit', event => {
      event.preventDefault();
      requestExplanation(root, root.querySelector('[data-learning-input]').value.trim());
    });
    requestExplanation(root);
  };
  return { mount };
})();
