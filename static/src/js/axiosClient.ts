import axios from "axios";
import $ from "jquery";

// Helper to read CSRF cookie from Django
function getCookie(name: string) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const axiosClient = axios.create({
  baseURL: "/",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosClient.interceptors.request.use((config: any) => {
  if (config.data instanceof FormData) {
    config.headers["Content-Type"] = "multipart/form-data";
  }

  // Attach CSRF token for unsafe methods
  const csrfToken = getCookie("csrftoken") || $("input[name=csrfmiddlewaretoken").val();
  if (csrfToken && !["get", "head", "options", "trace"].includes(config.method)) {
    config.headers["X-CSRFToken"] = csrfToken;
  }

  return config;
});

export default axiosClient;
