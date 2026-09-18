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



export {
  getAllProducts,
  getProduct,
};
