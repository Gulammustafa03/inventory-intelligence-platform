document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }

  const shell = document.querySelector(".app-shell");
  const sidebarToggle = document.querySelector("[data-sidebar-toggle]");
  if (shell && sidebarToggle) {
    const collapsed = localStorage.getItem("sidebar-collapsed") === "true";
    shell.classList.toggle("sidebar-collapsed", collapsed);

    sidebarToggle.addEventListener("click", () => {
      shell.classList.toggle("sidebar-collapsed");
      localStorage.setItem("sidebar-collapsed", shell.classList.contains("sidebar-collapsed"));
      if (window.lucide) {
        window.lucide.createIcons();
      }
    });
  }

  document.querySelectorAll("[data-counter]").forEach((node) => {
    const target = Number(node.dataset.counter || 0);
    const duration = 700;
    const start = performance.now();

    const tick = (time) => {
      const progress = Math.min((time - start) / duration, 1);
      node.textContent = Math.round(target * progress).toLocaleString();
      if (progress < 1) {
        requestAnimationFrame(tick);
      }
    };

    requestAnimationFrame(tick);
  });

  const grid = document.querySelector("[data-product-grid]");
  const table = document.querySelector("[data-product-table]");
  document.querySelectorAll("[data-view]").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll("[data-view]").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      const showTable = button.dataset.view === "table";
      grid?.classList.toggle("is-hidden", showTable);
      table?.classList.toggle("is-hidden", !showTable);
      if (window.lucide) {
        window.lucide.createIcons();
      }
    });
  });

  document.querySelectorAll(".alert").forEach((alert) => {
    setTimeout(() => {
      const instance = bootstrap.Alert.getOrCreateInstance(alert);
      instance.close();
    }, 6000);
  });

  const notificationBadge = document.getElementById("notificationBadge");
  const notificationCount = document.getElementById("notificationCount");
  const notificationList = document.getElementById("notificationList");

  const renderNotifications = (data) => {
    if (!notificationList) {
      return;
    }

    const notifications = data.notifications || [];
    const unread = data.unread_count || 0;

    notificationCount.textContent = unread;
    notificationBadge.style.display = unread ? "block" : "none";

    if (!notifications.length) {
      notificationList.innerHTML = '<div class="dropdown-item text-muted">No notifications</div>';
      return;
    }

    notificationList.innerHTML = notifications
      .map((notification) => {
        const readClass = notification.is_read ? "text-muted" : "fw-semibold";
        return `
          <a href="/notifications/" class="dropdown-item d-flex flex-column ${readClass}">
            <span>${notification.title}</span>
            <small>${notification.message}</small>
          </a>
        `;
      })
      .join("");
  };

  const loadNotifications = async () => {
    try {
      const response = await fetch("/notifications/latest", { credentials: "same-origin" });
      if (!response.ok) {
        throw new Error("Failed to load notifications");
      }
      const data = await response.json();
      renderNotifications(data);
    } catch (error) {
      console.warn(error);
    }
  };

  if (window.io) {
    try {
      const socket = io({ transports: ["websocket", "polling"] });
      socket.on("connect", () => {
        loadNotifications();
      });
      socket.on("notification", () => {
        loadNotifications();
      });
    } catch (error) {
      loadNotifications();
      setInterval(loadNotifications, 30000);
    }
  } else {
    loadNotifications();
    setInterval(loadNotifications, 30000);
  }
});
