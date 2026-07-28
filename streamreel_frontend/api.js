// api.js — the single place that knows how to talk to the backend.
// Every page includes this file instead of writing its own fetch logic.

const API_BASE = "https://streamreel-backend.onrender.com"; // change to your deployed backend URL in production

function getToken() {
  return localStorage.getItem("streamreel_token");
}

function setToken(token) {
  localStorage.setItem("streamreel_token", token);
}

function clearToken() {
  localStorage.removeItem("streamreel_token");
}

function isLoggedIn() {
  return !!getToken();
}

async function apiRequest(path, { method = "GET", body = null, auth = true } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth && getToken()) {
    headers["Authorization"] = `Bearer ${getToken()}`;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  let data = null;
  try {
    data = await response.json();
  } catch (e) {
    // some endpoints may return no body
  }

  if (!response.ok) {
    const message = (data && data.detail) || `Request failed (${response.status})`;
    throw new Error(message);
  }
  return data;
}

// ---- Auth ----
async function signup(email, password) {
  const data = await apiRequest("/api/auth/signup", {
    method: "POST",
    body: { email, password },
    auth: false,
  });
  setToken(data.access_token);
  return data;
}

async function login(email, password) {
  const data = await apiRequest("/api/auth/login", {
    method: "POST",
    body: { email, password },
    auth: false,
  });
  setToken(data.access_token);
  return data;
}

function logout() {
  clearToken();
  localStorage.removeItem("streamreel_profile_id");
  window.location.href = "login.html";
}

// ---- Profiles ----
async function listProfiles() {
  return apiRequest("/api/profiles");
}

async function createProfile(name, isKids = false) {
  return apiRequest("/api/profiles", {
    method: "POST",
    body: { name, is_kids: isKids },
  });
}

async function deleteProfile(profileId) {
  return apiRequest(`/api/profiles/${profileId}`, { method: "DELETE" });
}

// ---- Videos ----
async function listVideos(genre = null, language = null) {
  const params = new URLSearchParams();
  if (genre) params.set("genre", genre);
  if (language) params.set("language", language);
  const query = params.toString() ? `?${params.toString()}` : "";
  return apiRequest(`/api/videos${query}`);
}

async function listFeaturedVideos() {
  return apiRequest("/api/videos/featured");
}

async function searchVideos(query) {
  return apiRequest(`/api/videos/search?q=${encodeURIComponent(query)}`);
}

// ---- Watch history ----
async function saveWatchPosition(profileId, videoId, positionSeconds) {
  return apiRequest("/api/watch-history", {
    method: "POST",
    body: { profile_id: profileId, video_id: videoId, position_seconds: positionSeconds },
  });
}

async function getResumePosition(profileId, videoId) {
  return apiRequest(`/api/watch-history/${profileId}/${videoId}`);
}

// ---- Recommendations ----
async function getRecommendations(profileId) {
  return apiRequest(`/api/recommendations/${profileId}`);
}
