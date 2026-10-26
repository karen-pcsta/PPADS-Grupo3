import api from "./api";
import type { Product } from "../types/types";

async function getAllProducts(): Promise<Product[]> {
  const response = await api.get("/products");
  return response.data;
}

async function getProduct(public_id: string): Promise<Product> {
  const response = await api.get(`/products/${public_id}`);
  return response.data;
}

async function createProduct(
  name: string,
  price: number,
  description?: string,
): Promise<Product> {
  const response = await api.post("/products", {
    name,
    price,
    description,
  });
  return response.data;
}

async function updateProduct(
  public_id: string,
  update_data: Partial<Product>,
): Promise<Product> {
  const response = await api.put(`/products/${public_id}`, update_data);
  return response.data;
}

async function deleteProduct(public_id: string) {
  await api.delete(`/products/${public_id}`);
}

export {
  getAllProducts,
  getProduct,
  createProduct,
  updateProduct,
  deleteProduct,
};
