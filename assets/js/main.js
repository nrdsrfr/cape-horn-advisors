(function () {
  'use strict';

  // ---- Sticky header: toggle .scrolled past 40px ----
  var header = document.querySelector('.site-header');
  function onScroll() {
    if (!header) return;
    if (window.scrollY > 40) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // ---- Hamburger: toggle body.nav-open ----
  var hamburger = document.querySelector('.hamburger');
  if (hamburger) {
    hamburger.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // ---- Mobile submenu toggles (tap parent -> expand) ----
  var MOBILE = 820;
  document.querySelectorAll('.main-nav .has-children').forEach(function (li) {
    var trigger = li.querySelector(':scope > a, :scope > .nav-toggle-label');
    if (!trigger) return;
    trigger.addEventListener('click', function (e) {
      if (window.innerWidth > MOBILE) return; // desktop uses hover
      var href = trigger.getAttribute('href');
      // Label-only parents (href="#" or none) always just toggle; real links
      // toggle on first tap when closed, then navigate on the follow-up tap.
      if (!href || href === '#' || !li.classList.contains('open')) {
        e.preventDefault();
        li.classList.toggle('open');
      }
    });
  });

  // Close mobile menu when a real link is followed
  document.querySelectorAll('.main-nav .submenu a').forEach(function (a) {
    a.addEventListener('click', function () {
      document.body.classList.remove('nav-open');
    });
  });

  // ---- Contact form success banner (FormSubmit redirect back with ?sent=1) ----
  var successBox = document.getElementById('contact-success');
  if (successBox && /[?&]sent=1(&|$)/.test(window.location.search)) {
    successBox.hidden = false;
    successBox.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  
  // ---- Tool quote slide-in (observe and stagger on enter) ----
  var quotes = document.querySelectorAll('.tool-quote');
  if (quotes && quotes.length) {
    try {
      var qObserver = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          var idx = Array.prototype.indexOf.call(quotes, el);
          var delay = 1000 + (idx * 400); // 1s + stagger
          setTimeout(function () { el.classList.add('visible'); }, delay);
          obs.unobserve(el);
        });
      }, { threshold: 0.2 });
      quotes.forEach(function (q) { qObserver.observe(q); });
    } catch (e) {
      // IntersectionObserver not supported -> reveal immediately
      quotes.forEach(function (q) { q.classList.add('visible'); });
    }
  }
  
})();
