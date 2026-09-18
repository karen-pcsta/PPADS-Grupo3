import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Layout, PageHeader, Button, EmptyState, ErrorMessage } from '../../components/UI'
import type { Cart, CartItem } from '../../types/types'
import { getCart, updateCartItem, deleteCartItem } from '../../services/cart'
import { createOrder } from '../../services/orders'
import styles from './Cart.module.scss'

export default function CartPage() {
  const navigate = useNavigate()

  const [cart, setCart] = useState<Cart | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [placing, setPlacing] = useState(false)

  useEffect(() => {
    const fetch = async () => {
      try {
        const data = await getCart()
        setCart(data)
      } catch {
        setError('Failed to load cart.')
      } finally {
        setLoading(false)
      }
    }
    fetch()
  }, [])

  const updateQty = async (item: CartItem, qty: number) => {
    if (qty < 1) return
    try {
      await updateCartItem(item.public_id, { quantity: qty })
      setCart(prev => prev ? {
        ...prev,
        items: prev.items.map(i => i.public_id === item.public_id ? { ...i, quantity: qty } : i),
      } : prev)
    } catch {
      setError('Could not update quantity.')
    }
  }

  const removeItem = async (id: string) => {
    try {
      await deleteCartItem(id)
      setCart(prev => prev ? { ...prev, items: prev.items.filter(i => i.public_id !== id) } : prev)
    } catch {
      setError('Could not remove item.')
    }
  }

  const placeOrder = async () => {
    setPlacing(true)
    try {
      await createOrder()
      navigate('/orders')
    } catch {
      setError('Failed to place order.')
    } finally {
      setPlacing(false)
    }
  }

  const format = (n: number) => n.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

  const total = cart?.items.reduce((acc, i) => acc + i.unit_price * i.quantity, 0) ?? 0

  return (
    <Layout>
      <PageHeader title="Cart" subtitle={cart ? `${cart.items.length} item${cart.items.length !== 1 ? 's' : ''}` : ''} />

      {error && <div className={styles.pageError}><ErrorMessage message={error} /></div>}

      {loading ? (
        <div className={styles.skeletonList}>
          {[1, 2, 3].map(i => <div key={i} className={styles.skeletonRow} />)}
        </div>
      ) : !cart || cart.items.length === 0 ? (
        <EmptyState
          message="Your cart is empty."
          action={<Button variant="secondary" onClick={() => navigate('/products')}>Browse products</Button>}
        />
      ) : (
        <div className={styles.layout}>
          <div className={styles.itemsCol}>
            <table className={styles.table}>
              <thead>
                <tr className={styles.headRow}>
                  <th className={styles.thProduct}>Product</th>
                  <th className={styles.thQty}>Qty</th>
                  <th className={styles.thPrice}>Unit price</th>
                  <th className={styles.thSubtotal}>Subtotal</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {cart.items.map(item => (
                  <tr key={item.public_id} className={styles.row}>
                    <td className={styles.cellProduct}>
                      <span className={styles.itemName}>{item.product.name}</span>
                    </td>
                    <td className={styles.cellQty}>
                      <div className={styles.stepper}>
                        <button
                          onClick={() => updateQty(item, item.quantity - 1)}
                          className={styles.stepperButton}
                        >
                          −
                        </button>
                        <span className={styles.stepperValue}>
                          {item.quantity}
                        </span>
                        <button
                          onClick={() => updateQty(item, item.quantity + 1)}
                          className={styles.stepperButton}
                        >
                          +
                        </button>
                      </div>
                    </td>
                    <td className={styles.cellPrice}>
                      {format(item.unit_price)}
                    </td>
                    <td className={styles.cellSubtotal}>
                      {format(item.unit_price * item.quantity)}
                    </td>
                    <td className={styles.cellRemove}>
                      <button
                        onClick={() => removeItem(item.public_id)}
                        className={styles.removeButton}
                        title="Remove"
                      >
                        ✕
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className={styles.summaryCol}>
            <div className={styles.summaryCard}>
              <h3 className={styles.summaryTitle}>Order summary</h3>

              <div className={styles.summaryList}>
                {cart.items.map(item => (
                  <div key={item.public_id} className={styles.summaryLine}>
                    <span className={styles.summaryLineName}>{item.product.name} ×{item.quantity}</span>
                    <span className={styles.summaryLinePrice}>{format(item.unit_price * item.quantity)}</span>
                  </div>
                ))}
              </div>

              <div className={styles.summaryTotal}>
                <span className={styles.summaryTotalLabel}>Total</span>
                <span className={styles.summaryTotalValue}>{format(total)}</span>
              </div>

              <Button className={styles.placeOrderButton} loading={placing} onClick={placeOrder}>
                Place order
              </Button>
            </div>
          </div>
        </div>
      )}
    </Layout>
  )
}
