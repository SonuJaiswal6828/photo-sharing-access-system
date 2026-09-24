function renderFooter() {
  const container = document.getElementById("footer");
  if (!container) return;

  container.innerHTML = `
    <footer class="bg-bg border-t border-border mt-16">
      <div class="max-w-7xl mx-auto px-4 py-12 grid md:grid-cols-3 gap-10">
        <div>
          <h3 class="text-white text-lg font-bold mb-4 flex items-center gap-2">
            <span class="w-7 h-7 bg-gradient-to-br from-purple-600 to-indigo-600 rounded-md flex items-center justify-center text-xs">📸</span>
            PhotoShare
          </h3>
          <p class="text-sm text-gray-400 leading-relaxed">
            Secure photo sharing system with temporary access control.
            Admin can grant 1-hour access that can be revoked anytime.
          </p>
        </div>
        <div>
          <h4 class="text-white font-semibold mb-4">Quick Links</h4>
          <ul class="space-y-2 text-sm">
            <li><a href="index.html" class="text-gray-400 hover:text-purple-400 transition">Home</a></li>
            <li><a href="about.html" class="text-gray-400 hover:text-purple-400 transition">About</a></li>
            <li><a href="request-access.html" class="text-gray-400 hover:text-purple-400 transition">Request Access</a></li>
            <li><a href="login.html" class="text-gray-400 hover:text-purple-400 transition">Admin Login</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-white font-semibold mb-4">Contact</h4>
          <ul class="space-y-2.5 text-sm text-gray-400">
            <li>📧 sonuj6828@gmail.com</li>
            <li>📱 7776839491</li>
            <li>📍 Vasai East, Maharashtra, India</li>
            <li class="flex gap-4 mt-4">
              <a href="https://github.com/SonuJaiswal6828" target="_blank" class="hover:text-purple-400 transition">GitHub</a>
              <a href="https://sonuj-portfolio.netlify.app" target="_blank" class="hover:text-purple-400 transition">Portfolio</a>
              <a href="mailto:sonuj6828@gmail.com" class="hover:text-purple-400 transition">Email</a>
            </li>
          </ul>
        </div>
      </div>
      <div class="border-t border-border py-5 text-center text-sm text-gray-500">
        © 2026 PhotoShare · Made with ❤️ by <span class="text-white font-medium">Sonu Jaiswal</span>
      </div>
    </footer>
  `;
}