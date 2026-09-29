document.addEventListener('DOMContentLoaded', async () => {
  FixPilot.setupNavigation();
  const grid = document.getElementById('categoryGrid');
  const count = document.getElementById('availableCount');
  try {
    const response = await fetch('/api/categories');
    if (!response.ok) throw new Error('FixPilot service is unavailable.');
    const categories = await response.json();
    const available = categories.filter(category => category.available).length;
    if (count) count.textContent = `${available} diagnostic systems available`;
    grid.innerHTML = categories.map(category => `<article class="category-card ${category.available ? '' : 'is-unavailable'}"><div class="card-icon">${FixPilot.categoryIcon(category.id)}</div><div class="card-arrow">${FixPilot.icon('chevron')}</div><h2>${FixPilot.esc(category.name)}</h2><p>${FixPilot.esc(category.description)}</p><div class="card-footer"><span>${category.available ? `${Number(category.dataset_size).toLocaleString()} training cases` : 'Model unavailable'}</span><a class="card-start" href="${category.available ? FixPilot.pageFor(category.id) : '#'}" ${category.available ? '' : 'aria-disabled="true"'}>Start diagnosis <b>→</b></a></div></article>`).join('');
  } catch (error) {
    grid.innerHTML = '<div class="service-card"><strong>FixPilot needs its diagnostic service</strong><p>Open Start Diagnostic Hub.bat in the project folder, then refresh this page.</p></div>';
  }
});
