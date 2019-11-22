(function() {
  document.addEventListener('DOMContentLoaded', function() {
      var $burger = document.querySelector('#g-burger');
      var $userButton = document.querySelector('#g-user');
      var $mainNav = document.querySelector('#g-main-nav');
      var $userNav = document.querySelector('#g-user-nav');
      var $dropdowns = [].slice.call(document.querySelectorAll('.g-nav-has-dropdown'));
      var $closeButtons = [].slice.call(document.querySelectorAll('.g-nav-close'));
      var activeClassName = 'is-active';



      function isActive($el) {
          return $el.classList.contains(activeClassName);
      }

      function setActive($el) {
          $el.classList.add(activeClassName);
      }

      function unsetActive($el) {
          $el.classList.remove(activeClassName);
      }

      function collapseAllDropdowns() {
          $dropdowns.forEach(function ($dropdown) {
              unsetActive($dropdown);
          });
      }

      function activateDropdown(event) {
          var item = event.currentTarget;
          var shouldOpen = !isActive(item);
          collapseAllDropdowns();
          if (shouldOpen) {
              setActive(item);
          }
      }

      function enableExpandHandlers($el) {
          var $currentDropdowns = [].slice.call($el.querySelectorAll('.g-nav-has-dropdown'));
          $currentDropdowns.forEach(function ($dropdown) {
              $dropdown.addEventListener('click', activateDropdown);
          });

          if ($currentDropdowns.length === 1) {
              setActive($currentDropdowns[0]);
          }
      }

      function uninstallExpandHandlers() {
          $dropdowns.forEach(function (dropdown) {
              dropdown.removeEventListener('click', activateDropdown);
          });
      }

      function openMobileNav($el) {
          enableExpandHandlers($el);
          setActive($el);
      }

      function closeMobileNav($el) {
          collapseAllDropdowns();
          uninstallExpandHandlers();
          unsetActive($el);
      }

      function toggleMobileNav(e) {
          var $el = document.querySelector(e.currentTarget.getAttribute('data-nav-toggle'));
          if (isActive($el)) {
              closeMobileNav($el);
          } else {
              openMobileNav($el);
          }
      }

      $burger.addEventListener('click', toggleMobileNav);
      if($userButton) {
          $userButton.addEventListener('click', toggleMobileNav);
      }

      $closeButtons.forEach(function (closeButton) {
          closeButton.addEventListener('click', function (e) {
              var $el = document.querySelector(e.currentTarget.getAttribute('data-nav-close'));
              closeMobileNav($el);
          });
      });


      function resetNav() {
          closeMobileNav($mainNav);
          if($userNav) {
              closeMobileNav($userNav);
          }
      }

      window.addEventListener('resize', resetNav);
      window.addEventListener('orientationchange', resetNav);
  });
})();
