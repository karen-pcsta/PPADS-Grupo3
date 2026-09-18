import api from "./api";
import type { Cart, CartItem } from "../types/types";

async function getCart(): Promise<Cart> {
  const response = await api.get("/cart");
  return response.data;
}

async function addCartItem(
  product_id: string,
  quantity: number,
): Promise<CartItem> {
  const response = await api.post("/cart/items", { product_id, quantity });
  return response.data;
}

async function updateCartItem(
  public_id: string,
  updated_item: Partial<CartItem>,
): Promise<CartItem> {
  const response = await api.put(`/cart/items/${public_id}`, updated_item);
  return response.data;
}

async function deleteCartItem(public_id: string) {
  await api.delete(`/cart/items/${public_id}`);
}

export { getCart, addCartItem, updateCartItem, deleteCartItem };
