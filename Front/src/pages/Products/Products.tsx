import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Layout,
  PageHeader,
  Button,
  EmptyState,
  ErrorMessage,
} from "../../components/UI";
import type { Product } from "../../types/types";
import {
  getAllProducts,
} from "../../services/products";
import { addCartItem } from "../../services/cart";
import styles from "./Products.module.scss";


export default function ProductsPage() {
  const navigate = useNavigate();

  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [addedIds, setAddedIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    const fetch = async () => {
      try {
        const data = await getAllProducts();
        setProducts(data);
      } catch {
        setError("Failed to load products.");
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  const handleAddToCart = async (product: Product) => {
    try {
      await addCartItem(product.public_id, 1);
      setAddedIds((prev) => new Set(prev).add(product.public_id));
      setTimeout(
        () =>
          setAddedIds((prev) => {
            const n = new Set(prev);
            n.delete(product.public_id);
            return n;
          }),
        1500,
      );
    } catch {
      setError("Could not add item to cart.");
    }
  };

  const format = (n: number) =>
    n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

  return (
    <Layout>
      <PageHeader
        title="Products"
        subtitle={`${products.length} item${products.length !== 1 ? "s" : ""}`}
      />

      {error && (
        <div className={styles.pageError}>
          <ErrorMessage message={error} />
        </div>
      )}

      {loading ? (
        <div className={styles.grid}>
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className={styles.skeletonCard} />
          ))}
        </div>
      ) : products.length === 0 ? (
        <EmptyState
          message="No products yet."
        />
      ) : (
        <div className={styles.grid}>
          {products.map((product) => (
            <div
              key={product.public_id}
              className={styles.card}
              onClick={() => navigate(`/products/${product.public_id}`)}
            >
              <div className={styles.cardBody}>
                <h3 className={styles.cardName}>{product.name}</h3>
                {product.description && (
                  <p className={styles.cardDescription}>
                    {product.description}
                  </p>
                )}
              </div>

              <div className={styles.cardFooter}>
                <span className={styles.price}>
                  {format(product.price)}
                </span>

                <div
                  className={styles.actions}
                  onClick={(e) => e.stopPropagation()}
                >
                  <Button
                    variant={
                      addedIds.has(product.public_id)
                        ? "secondary"
                        : "primary"
                    }
                    className={styles.actionButton}
                    onClick={() => handleAddToCart(product)}
                  >
                    {addedIds.has(product.public_id)
                      ? "Added"
                      : "Add to cart"}
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
}
