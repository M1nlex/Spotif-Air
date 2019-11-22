(function() {
  document.addEventListener('DOMContentLoaded', function() {
      var $searchButton = document.querySelector('#g-search');
      var $searchButtonIcon = document.querySelector('#g-search > i');
      var $searchBox = document.querySelector('#g-search-input');
      var $searchInput = document.querySelector('#g-search-input input');
      var $topBar = document.querySelector('#g-top-bar');
      var $mainNav = document.querySelector('#g-main-nav');
      var searchingClassName = 'searching';


      function isSearching() {
          return $topBar.classList.contains(searchingClassName);
      }

      function show($el) {
          $el.style.display = 'block';
      }

      function hide($el) {
          $el.style.display = 'none';
      }

      function switchClass($el, oldClass, newClass) {
          $el.classList.remove(oldClass);
          $el.classList.add(newClass);
      }

      function toggleSearching() {
          if (isSearching()) {
              closeSearchBar();
          } else {
              openSearchBar();
          }
      }

      function openSearchBar() {
          hide($mainNav);
          show($searchBox);
          switchClass($searchButtonIcon, 'fa-search', 'fa-times');
          $topBar.classList.add(searchingClassName);
          $searchInput.focus();
      }

      function closeSearchBar() {
          show($mainNav);
          hide($searchBox);
          $topBar.classList.remove(searchingClassName);
          switchClass($searchButtonIcon, 'fa-times', 'fa-search');
      }

      $searchButton.addEventListener('click', toggleSearching);
  });
})();