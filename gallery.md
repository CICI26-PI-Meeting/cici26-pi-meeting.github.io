---
layout: page
title: Poster Gallery
permalink: /gallery/
---

<link rel="stylesheet" href="{{ '/assets/css/poster-gallery.css' | relative_url }}">

<!-- Search -->
<div class="gallery-search-wrapper">
  <span class="search-icon">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
      <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85zm-5.242.656a5 5 0 1 1 0-10 5 5 0 0 1 0 10z"/>
    </svg>
  </span>
  <input type="text" id="poster-search" placeholder="Search by title, author, or poster content…" autocomplete="off">
</div>

<div class="gallery-result-count" id="gallery-result-count"></div>

<!-- Gallery Grid -->
<div class="poster-gallery-grid" id="poster-gallery">
  {% for poster in site.data.posters %}
  {% assign thumb = poster.filename | replace: '.pdf', '.png' %}
  <div class="poster-card" data-title="{{ poster.title | downcase }}" data-author="{{ poster.author | downcase }}" data-summary="{{ poster.summary | downcase }}" data-pdftext="{{ poster.pdfText | downcase | escape }}">
    <a href="{{ '/assets/posters/' | append: poster.filename | relative_url }}" target="_blank" class="poster-card-preview">
      <img src="{{ '/assets/posters/thumbnails/' | append: thumb | relative_url }}" alt="{{ poster.title }}" loading="lazy">
    </a>
    <div class="poster-card-body">
      <h3>{{ poster.title }}</h3>
      <div class="poster-card-author">{{ poster.author }}</div>
      <div class="poster-card-actions">
        <a href="{{ '/assets/posters/' | append: poster.filename | relative_url }}" target="_blank" class="btn-view">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
            <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
            <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
          </svg>
          View
        </a>
        <a href="{{ '/assets/posters/' | append: poster.filename | relative_url }}" download class="btn-download">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
            <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
            <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
          </svg>
          Download
        </a>
      </div>
    </div>
  </div>
  {% endfor %}
</div>

<!-- No results message -->
<div class="gallery-no-results" id="gallery-no-results">
  <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16">
    <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85zm-5.242.656a5 5 0 1 1 0-10 5 5 0 0 1 0 10z"/>
  </svg>
  <p>No posters match your search.</p>
</div>

<script>
document.addEventListener('DOMContentLoaded', function () {
  var searchInput = document.getElementById('poster-search');
  var cards = document.querySelectorAll('.poster-card');
  var resultCount = document.getElementById('gallery-result-count');
  var noResults = document.getElementById('gallery-no-results');
  var totalPosters = cards.length;

  function updateCount(visible) {
    if (searchInput.value.trim() === '') {
      resultCount.textContent = totalPosters + ' poster' + (totalPosters !== 1 ? 's' : '');
    } else {
      resultCount.textContent = visible + ' of ' + totalPosters + ' poster' + (totalPosters !== 1 ? 's' : '') + ' shown';
    }
  }

  updateCount(totalPosters);

  searchInput.addEventListener('input', function () {
    var query = this.value.toLowerCase().trim();
    var visible = 0;

    cards.forEach(function (card) {
      var title = card.getAttribute('data-title') || '';
      var author = card.getAttribute('data-author') || '';
      var summary = card.getAttribute('data-summary') || '';
      var pdftext = card.getAttribute('data-pdftext') || '';
      var haystack = title + ' ' + author + ' ' + summary + ' ' + pdftext;

      if (!query || haystack.indexOf(query) !== -1) {
        card.classList.remove('hidden');
        visible++;
      } else {
        card.classList.add('hidden');
      }
    });

    updateCount(visible);
    noResults.style.display = visible === 0 ? 'block' : 'none';
  });
});
</script>
