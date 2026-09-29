document.addEventListener('DOMContentLoaded', () => {
  FixPilot.setupNavigation();
  const TOPICS = [
    { id: 'pc', label: 'PC & hardware', suggestions: ['What is RAM?', 'Why does a CPU get hot?', 'SSD vs HDD?'] },
    { id: 'smartphone', label: 'Smartphone basics', suggestions: ['What is battery health?', 'Why is charging slow?', 'What uses phone storage?'] },
    { id: 'wifi', label: 'Wi-Fi & internet', suggestions: ['What is an IP address?', 'What is DNS?', 'Why does Wi-Fi say connected but have no internet?'] },
    { id: 'gaming', label: 'Gaming & console', suggestions: ['Why is my ping high?', 'Why does a console overheat?', 'What does storage affect?'] },
    { id: 'battery', label: 'Battery & charging', suggestions: ['Why is charging slow?', 'What is battery health?', 'Why does heat affect a battery?'] },
    { id: 'car', label: 'Car systems', suggestions: ['Why is my check-engine light on?', 'Why does an engine overheat?', 'What causes slow cranking?'] },
    { id: 'home_electronics', label: 'Home electronics', suggestions: ['What does a power surge do?', 'Why does a device restart?', 'What should I check first?'] },
    { id: 'electrical', label: 'Electrical & power', suggestions: ['What is a power surge?', 'Why does a breaker trip?', 'What does a UPS do?'] }
  ];
  const storeKey = 'fixpilot-understanding-conversations';
  const messages = document.querySelector('[data-messages]');
  const suggestions = document.querySelector('[data-suggestions]');
  const composer = document.querySelector('[data-composer]');
  const input = document.querySelector('[data-message]');
  const send = document.querySelector('[data-send]');
  const contextCard = document.querySelector('[data-context-card]');
  let activeTopic = new URLSearchParams(window.location.search).get('topic') || '';
  let busy = false;
  const esc = FixPilot.esc;
  const read = () => { try { return JSON.parse(sessionStorage.getItem(storeKey) || '{}'); } catch { return {}; } };
  const write = value => sessionStorage.setItem(storeKey, JSON.stringify(value));
  const context = () => { try { return JSON.parse(sessionStorage.getItem('fixpilot-diagnostic-context') || '{}'); } catch { return {}; } };
  const thread = () => read()[activeTopic || 'general'] || [];
  const saveThread = items => { const all = read(); all[activeTopic || 'general'] = items.slice(-20); write(all); };
  const selectedTopic = () => TOPICS.find(item => item.id === activeTopic);

  function renderTopics() {
    const target = document.querySelector('[data-topics]');
    target.innerHTML = '';
    TOPICS.forEach(item => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = item.id === activeTopic ? 'active' : '';
      button.innerHTML = FixPilot.categoryIcon(item.id) + '<span>' + esc(item.label) + '</span>';
      button.addEventListener('click', () => {
        activeTopic = item.id;
        history.replaceState(null, '', '/understanding?topic=' + encodeURIComponent(activeTopic));
        render();
      });
      target.appendChild(button);
    });
  }

  function renderContext() {
    const value = context();
    const category = value.categoryName || value.category || '';
    const step = value.step || '';
    if (!category && !step && !value.result) { contextCard.hidden = true; return; }
    contextCard.hidden = false;
    contextCard.querySelector('[data-context-title]').textContent = category || 'Current diagnostic';
    contextCard.querySelector('[data-context-detail]').textContent = value.result ? 'Result: ' + (value.result.diagnosis || 'available') : (step ? 'Current step: ' + step : 'Diagnostic context available');
  }

  function addMessage(item) {
    const article = document.createElement('article');
    article.className = 'assistant-message ' + item.role;
    const role = document.createElement('span');
    role.className = 'assistant-message-role';
    role.textContent = item.role === 'user' ? 'You' : 'FixPilot';
    const body = document.createElement('div');
    if (item.visual) {
      const figure = document.createElement('figure');
      figure.className = 'assistant-message-visual';
      const image = document.createElement('img');
      image.src = item.visual.url;
      image.alt = item.visual.alt;
      image.loading = 'lazy';
      const caption = document.createElement('figcaption');
      caption.textContent = item.visual.description;
      figure.append(image, caption);
      body.appendChild(figure);
    }
    const paragraph = document.createElement('p');
    paragraph.textContent = item.content;
    body.appendChild(paragraph);
    article.append(role, body);
    messages.appendChild(article);
  }

  function render() {
    renderTopics();
    renderContext();
    const current = thread();
    const selected = selectedTopic();
    document.getElementById('assistantTitle').textContent = selected ? selected.label + ': explained simply.' : 'Learn what FixPilot is checking.';
    messages.innerHTML = '';
    if (current.length) current.forEach(addMessage);
    else {
      const empty = document.createElement('div');
      empty.className = 'assistant-empty';
      empty.innerHTML = '<h2>Ask FixPilot to explain.</h2><p>Choose a topic or ask about the diagnostic you are currently working through.</p>';
      messages.appendChild(empty);
    }
    const choices = selected ? selected.suggestions : ['What is DNS?', 'What is RAM?', 'Why is FixPilot asking this?'];
    suggestions.innerHTML = '';
    choices.forEach(question => {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = question;
      button.addEventListener('click', () => ask(question));
      suggestions.appendChild(button);
    });
    messages.scrollTop = messages.scrollHeight;
  }

  function showTyping() {
    const typing = document.createElement('article');
    typing.className = 'assistant-message assistant typing';
    typing.dataset.typing = '';
    typing.innerHTML = '<span class="assistant-message-role">FixPilot</span><div><span></span><span></span><span></span></div>';
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;
  }

  async function ask(raw) {
    const message = String(raw || input.value).trim();
    if (!message || busy) return;
    busy = true;
    send.disabled = true;
    input.value = '';
    const history = thread();
    saveThread(history.concat({ role: 'user', content: message }));
    render();
    showTyping();
    try {
      const diagnostic = context();
      const payload = {
        message,
        context: Object.assign({}, diagnostic, { category: diagnostic.category || activeTopic }),
        history
      };
      const response = await fetch('/api/understanding/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
      const reply = await response.json();
      if (!response.ok) throw new Error(reply.error || 'FixPilot could not prepare an explanation.');
      saveThread(thread().concat({ role: 'assistant', content: reply.answer, visual: reply.visual || null }));
    } catch (error) {
      saveThread(thread().concat({ role: 'assistant', content: error.message || 'FixPilot could not prepare that explanation. Please try again.' }));
    } finally {
      busy = false;
      send.disabled = false;
      render();
      input.focus();
    }
  }

  composer.addEventListener('submit', event => { event.preventDefault(); ask(); });
  input.addEventListener('keydown', event => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); ask(); } });
  document.querySelector('[data-new-chat]').addEventListener('click', () => { saveThread([]); render(); input.focus(); });
  document.querySelector('[data-clear-chat]').addEventListener('click', () => { saveThread([]); render(); });
  document.querySelector('[data-clear-context]').addEventListener('click', () => { sessionStorage.removeItem('fixpilot-diagnostic-context'); renderContext(); });
  const requestedQuestion = new URLSearchParams(window.location.search).get('question');
  render();
  if (requestedQuestion) ask(requestedQuestion);
});
