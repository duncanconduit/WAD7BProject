document.addEventListener('DOMContentLoaded', function() {
    const dropdownToggle = document.getElementById('dropdownToggle');
    const dropdownMenu = document.getElementById('dropdownMenu');
    const transitionDuration = 100; // in milliseconds
  
    function showDropdown() {
      // Remove hidden and then force a reflow to apply the transition
      dropdownMenu.classList.remove('hidden');
      // Using requestAnimationFrame ensures CSS changes are recognised
      requestAnimationFrame(() => {
        dropdownMenu.classList.remove('opacity-0', 'scale-90');
        dropdownMenu.classList.add('opacity-100', 'scale-100');
      });
    }
  
    function hideDropdown() {
      dropdownMenu.classList.remove('opacity-100', 'scale-100');
      dropdownMenu.classList.add('opacity-0', 'scale-90');
      // After the transition ends add the hidden class
      setTimeout(() => {
        dropdownMenu.classList.add('hidden');
      }, transitionDuration);
    }
  
    function toggleDropdown() {
      if (dropdownMenu.classList.contains('hidden')) {
        showDropdown();
      } else {
        hideDropdown();
      }
    }
  
    // When the toggle button is clicked, show/hide dropdown menu.
    dropdownToggle.addEventListener('click', function(event) {
      event.stopPropagation(); // Prevent propagation to document click
      toggleDropdown();
    });
  
    // Hide the dropdown if clicking outside of it.
    document.addEventListener('click', function(event) {
      if (!dropdownMenu.contains(event.target) && !dropdownToggle.contains(event.target)) {
        // Only hide if already visible
        if (!dropdownMenu.classList.contains('hidden')) {
          hideDropdown();
        }
      }
    });
  });