import api from "./api";
import type { Order } from "../types/types";

async function createOrder(): Promise<Order> {
  const response = await api.post("/orders");
  return response.data;
}

async function getAllOrders(): Promise<Order[]> {
  const response = await api.get("/orders");
  return response.data;
}

async function getOrder(public_id: string): Promise<Order> {
  const response = await api.get(`/orders/${public_id}`);
  return response.data;
}

async function finalizeOrder(public_id: string): Promise<Order> {
  const response = await api.put(`/orders/${public_id}/complete`);
  return response.data;
}

async function cancelOrder(public_id: string) {
  await api.delete(`/orders/${public_id}`);
}


export { createOrder, getAllOrders, getOrder, finalizeOrder, cancelOrder };









