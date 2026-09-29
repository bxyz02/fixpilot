window.FixPilot = (() => {
  const esc = value => String(value).replace(/[&<>"']/g, character => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[character]));
  const pages = { pc: '/pages/pc.html', smartphone: '/pages/smartphone.html', wifi: '/pages/wifi.html', gaming: '/pages/gaming.html', battery: '/pages/battery.html', car: '/pages/car.html', home_electronics: '/pages/electronics.html', electrical: '/pages/electrical.html' };
  const paths = {
    cpu: '<rect x="5" y="5" width="14" height="14" rx="2"/><rect x="9" y="9" width="6" height="6" rx="1"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',
    phone: '<rect x="7" y="3" width="10" height="18" rx="2"/><path d="M10 6h4M11 18h2"/>',
    network: '<circle cx="12" cy="12" r="8"/><path d="M4 12h16M12 4c2.1 2.2 3.2 4.9 3.2 8S14.1 17.8 12 20M12 4C9.9 6.2 8.8 8.9 8.8 12s1.1 5.8 3.2 8"/>',
    controller: '<path d="M7.1 9.2h9.8c2.4 0 3.9 2.1 3.2 4.4l-1 3.2a2.4 2.4 0 0 1-4.4.4l-.8-1.5H10l-.8 1.5a2.4 2.4 0 0 1-4.4-.4l-1-3.2C3.2 11.3 4.7 9.2 7.1 9.2Z"/><path d="M7.5 12.2v3M6 13.7h3M16 12.5h.01M18 14.5h.01"/>',
    battery: '<rect x="4" y="7" width="15" height="10" rx="2"/><path d="M19 10h1.5v4H19M12 9.5 9.5 13H12l-.5 2.5L14.5 12H12z"/>',
    car: '<path d="M5 16.5h14l-1-5.4a2.4 2.4 0 0 0-2.3-1.9H8.3A2.4 2.4 0 0 0 6 11.1l-1 5.4Z"/><path d="M4 16.5v2h2M20 16.5v2h-2M6.5 13h11M7 16.5h.01M17 16.5h.01"/>',
    monitor: '<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M9 21h6M12 17v4"/>',
    power: '<path d="M12 3v9M7.1 5.9a7 7 0 1 0 9.8 0"/>',
    chart: '<path d="M4 19V5M4 19h16M8 15l3-3 3 2 5-6"/><path d="M16 8h3v3"/>',
    thermometer: '<path d="M10 14.5V5a2 2 0 1 1 4 0v9.5a4 4 0 1 1-4 0Z"/><path d="M12 17v-7"/>',
    drive: '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 14h.01M11 14h6"/>',
    window: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01"/>',
    list: '<path d="M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01"/>',
    chevron: '<path d="m8 10 4 4 4-4"/>'
  };
  const icon = (name, className = '') => `<svg class="ui-icon ${className}" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${paths[name] || paths.list}</svg>`;
  const categoryIcon = id => icon({pc:'cpu', smartphone:'phone', wifi:'network', gaming:'controller', battery:'battery', car:'car', home_electronics:'monitor', electrical:'power'}[id] || 'list');
  const sequenceIcon = title => {
    const name = title.toLowerCase();
    if (name.includes('hardware')) return icon('cpu');
    if (name.includes('performance')) return icon('chart');
    if (name.includes('temperature') || name.includes('thermal') || name.includes('cool')) return icon('thermometer');
    if (name.includes('storage')) return icon('drive');
    if (name.includes('network') || name.includes('connect')) return icon('network');
    if (name.includes('operating') || name.includes('system') || name.includes('software')) return icon('window');
    if (name.includes('power') || name.includes('supply')) return icon('power');
    return icon('list');
  };
  const setupNavigation = () => {
    const button = document.querySelector('[data-mobile-menu]');
    const nav = document.querySelector('.desktop-nav');
    if (!nav) return;
    if (!nav.querySelector('a[href="/understanding"]')) {
      const link = document.createElement('a');
      link.href = '/understanding';
      link.textContent = 'Understanding';
      if (location.pathname.endsWith('/understanding') || location.pathname.endsWith('/understanding.html')) link.setAttribute('aria-current', 'page');
      nav.insertBefore(link, nav.querySelector('a[href="about.html"]') || null);
    }
    if (button) button.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      button.setAttribute('aria-expanded', String(open));
    });
  };
  return { esc, icon, categoryIcon, sequenceIcon, pageFor: id => pages[id] || '/categories', setupNavigation };
})();
