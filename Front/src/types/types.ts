export interface User {
  public_id: string
  username: string
  email: string
  role: string
}

export interface Product {
  public_id: string
  name: string
  description: string | null
  price: number
}

export interface CartItem {
  public_id: string
  quantity: number
  unit_price: number
  product: {
    public_id: string
    name: string
  }
}

export interface Cart {
  public_id: string
  items: CartItem[]
}

export interface OrderItem {
  quantity: number
  unit_price: number
  product: {
    public_id: string
    name: string
  }
}

export interface Order {
  public_id: string
  status: string
  total: number
  created_at: string
  items: OrderItem[]
}

export interface AuthResponse {
  access_token: string
  token_type: string
}