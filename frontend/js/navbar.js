function renderNavbar() {
  const container = document.getElementById("navbar");
  if (!container) return;

  // Current page
  const currentPage = window.location.pathname.split("/").pop() || "index.html";

  // Force public navbar on friend pages
  const isFriendPage =
    currentPage === "session-photos.html" ||
    currentPage === "request-access.html" ||
    currentPage === "request-status.html";

  // Logged in only if token exists AND not on friend page
  const loggedIn = isLoggedIn() && !isFriendPage;

  // Base link (inactive)
  const baseLink =
    "px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 text-gray-300 hover:text-white hover:bg-purple-600/10";

  // Active link (current page)
  const activeLink =
    "px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 text-white bg-purple-600/20 border border-purple-500/40 shadow-sm shadow-purple-900/30";

  // Helper
  function navLink(href, label) {
    const isActive = href === currentPage;
    return `<a href="${href}" class="${isActive ? activeLink : baseLink}">${label}</a>`;
  }

  // Sign Up button
  const signupBtn = `
    <a href="signup.html"
       class="px-5 py-2 rounded-lg text-sm font-semibold transition-all duration-200 text-white
              bg-gradient-to-r from-purple-600 to-indigo-600
              hover:from-purple-500 hover:to-indigo-500
              shadow-lg shadow-purple-900/30
              hover:shadow-purple-900/50
              hover:scale-[1.03] active:scale-[0.98]">
      Sign Up
    </a>
  `;

  // Logout button
  const logoutBtn = `
    <button onclick="logout()"
      class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200
             text-gray-300 bg-white/5 border border-white/10
             hover:bg-white/10 hover:text-white hover:border-white/20">
      Logout
    </button>
  `;

  const publicLinks = `
    ${navLink("index.html", "Home")}
    ${navLink("about.html", "About")}
    ${navLink("request-access.html", "Request Access")}
    ${navLink("request-status.html", "Check Status")}
    ${navLink("login.html", "Login")}
    ${signupBtn}
  `;

  const authLinks = `
    ${navLink("index.html", "Home")}
    ${navLink("about.html", "About")}
    ${navLink("dashboard.html", "Dashboard")}
    ${navLink("groups.html", "Groups")}
    ${navLink("pending.html", "Requests")}
    ${navLink("sessions.html", "Sessions")}
    ${logoutBtn}
  `;

  container.innerHTML = `
    <nav class="bg-bg/80 backdrop-blur-lg border-b border-border sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center flex-wrap gap-3">
        <a href="index.html" class="flex items-center gap-2.5 text-lg font-bold text-white hover:opacity-90 transition">
          <span class="w-8 h-8 bg-gradient-to-br from-purple-600 to-indigo-600 rounded-lg flex items-center justify-center text-sm shadow-lg shadow-purple-900/40">
            📸
          </span>
          <span>PhotoShare</span>
        </a>
        <div class="flex gap-1.5 items-center text-sm flex-wrap">
          ${loggedIn ? authLinks : publicLinks}
        </div>
      </div>
    </nav>
  `;
}