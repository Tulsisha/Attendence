
  // live clock update
  function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    document.getElementById('time').textContent = timeString;
  }
  setInterval(updateTime, 1000);
  updateTime();

  // Elements
  const punchBtn = document.getElementById('punchBtn');
  const punchMenu = document.querySelector('li:nth-child(1)'); // Punch menu
  const punchOutMenu = document.querySelector('li:nth-child(2)'); // Punch Out menu

  let currentMode = 'punch'; // default

  // Punch menu click
  punchMenu.addEventListener('click', function() {
    currentMode = 'punch';
    punchBtn.textContent = "Punch";
    punchBtn.style.backgroundColor = "#2563eb"; // blue
  });

  // Punch Out menu click
  punchOutMenu.addEventListener('click', function() {
    currentMode = 'punchout';
    punchBtn.textContent = "Punch Out";
    punchBtn.style.backgroundColor = "#dc2626"; // red
  });

  // Button click behavior
  punchBtn.addEventListener('click', function() {
    const now = new Date();
    const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    if (currentMode === 'punch') {
      alert(`✅ Good Morning!!\nYou have punched in successfully at ${timeString}\nHave a nice day, Thank You!!`);
    } else if (currentMode === 'punchout') {
      alert(`👋 You have punched out successfully at ${timeString}\nSee you again!`);
    }
  });