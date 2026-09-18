import api from "./api";
import type { AuthResponse, User } from "../types/types";

async function register(
  username: string,
  email: string,
  password: string,
): Promise<AuthResponse> {
  const response = await api.post("/auth/register", {
    username,
    email,
    password,
  });
  return response.data;
}

async function login(
  usernameOrEmail: string,
  password: string,
): Promise<AuthResponse> {
  const res_body = usernameOrEmail.includes("@")
    ? { email: usernameOrEmail, password }
    : { username: usernameOrEmail, password };
  const response = await api.post("/auth/login", res_body);
  return response.data;
}

async function me(token: string): Promise<User> {
  const response = await api.get('/auth/me', {
    headers: { Authorization: `Bearer ${token}` }
  })
  return response.data
}

async function logout() {
  localStorage.removeItem("token");
}

export {register, login, logout, me};
