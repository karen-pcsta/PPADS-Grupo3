import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Layout, Button, ErrorMessage } from '../../components/UI'
import type { Product } from '../../types/types'
import { getProduct } from '../../services/products'
import { addCartItem } from '../../services/cart'
import styles from './ProductDetail.module.scss'

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [quantity, setQuantity] = useState(1)
  const [added, setAdded] = useState(false)

  useEffect(() => {
    const fetch = async () => {
      try {
        const data = await getProduct(id!)
        if (!data) throw new Error('Not found')
        setProduct(data)
      } catch {
        setError('Product not found.')
      } finally {
        setLoading(false)
      }
    }
    if (id) fetch()
  }, [id])

  const handleAddToCart = async () => {
    try {
      await addCartItem(product!.public_id, quantity)
      setAdded(true)
      setTimeout(() => setAdded(false), 2000)
    } catch {
      setError('Could not add to cart.')
    }
  }

  const format = (n: number) => n.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

  return (
    <Layout>
      <button
        onClick={() => navigate('/products')}
        className={styles.backButton}
      >
        <span>←</span> Back to products
      </button>

      {error && <ErrorMessage message={error} />}

      {loading ? (
        <div className={styles.skeleton}>
          <div className={`${styles.skeletonLine} ${styles.skeletonTitle}`} />
          <div className={`${styles.skeletonLine} ${styles.skeletonText}`} />
          <div className={`${styles.skeletonLine} ${styles.skeletonSmall}`} />
        </div>
      ) : product ? (
        <div className={styles.content}>
          <h1 className={styles.title}>{product.name}</h1>

          <p className={styles.description}>
            {product.description ?? 'No description available'}
          </p>

          <div className={styles.purchaseBox}>
            <div className={styles.priceRow}>
              <span className={styles.price}>
                {format(product.price)}
              </span>
              {quantity > 1 && (
                <span className={styles.priceTotal}>
                  × {quantity} = {format(product.price * quantity)}
                </span>
              )}
            </div>

            <div className={styles.actionsRow}>
              <div className={styles.stepper}>
                <button
                  onClick={() => setQuantity(q => Math.max(1, q - 1))}
                  className={styles.stepperButton}
                >
                  −
                </button>
                <span className={styles.stepperValue}>
                  {quantity}
                </span>
                <button
                  onClick={() => setQuantity(q => q + 1)}
                  className={styles.stepperButton}
                >
                  +
                </button>
              </div>

              <Button
                variant={added ? 'secondary' : 'primary'}
                onClick={handleAddToCart}
              >
                {added ? 'Added to cart' : 'Add to cart'}
              </Button>
            </div>
          </div>
        </div>
      ) : null}
    </Layout>
  )
}
