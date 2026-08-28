import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

const api = axios.create({ baseURL: API });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("teachkit_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// FastAPI's error body is usually {"detail": "some string"}, but for
// Pydantic validation errors (422s) `detail` is instead an ARRAY of
// {type, loc, msg, input, ctx} objects — passing that straight to a toast
// crashes React ("Objects are not valid as a React child"). Always route
// error display through one of these so any error shape renders as plain text.
export function detailToMessage(detail, fallback = "Something went wrong") {
  if (!detail) return fallback;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail.map((d) => (typeof d === "string" ? d : d?.msg || JSON.stringify(d))).join("; ") || fallback;
  }
  return fallback;
}

export function getErrorMessage(error, fallback = "Something went wrong") {
  return detailToMessage(error?.response?.data?.detail, fallback);
}

export default api;
