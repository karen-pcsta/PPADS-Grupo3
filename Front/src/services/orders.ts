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


export { createOrder, getAllOrders, getOrder };









