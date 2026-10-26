import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Layout,
  PageHeader,
  Button,
  EmptyState,
  ErrorMessage,
} from "../../components/UI";
import { useAuth } from "../../context/AuthContext";
import type { Product } from "../../types/types";
import {
  getAllProducts,
  createProduct,
  updateProduct,
  deleteProduct,
} from "../../services/products";
import { addCartItem } from "../../services/cart";
import styles from "./Products.module.scss";


export default function ProductsPage() {
  const navigate = useNavigate();
  const { isAdmin } = useAuth();

  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [addedIds, setAddedIds] = useState<Set<string>>(new Set());
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<Product | undefined>();

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

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this product?")) return;
    try {
      await deleteProduct(id);
      setProducts((prev) => prev.filter((p) => p.public_id !== id));
    } catch {
      setError("Could not delete product.");
    }
  };

  const handleSave = async (data: Omit<Product, "public_id">) => {
    try {
      if (editing) {
        await updateProduct(editing.public_id, data);
        setProducts((prev) =>
          prev.map((p) =>
            p.public_id === editing.public_id ? { ...p, ...data } : p,
          ),
        );
      } else {
        const created = await createProduct(
          data.name,
          data.price,
          data.description ?? undefined,
        );
        setProducts((prev) => [...prev, created]);
      }
      setShowModal(false);
      setEditing(undefined);
    } catch {
      setError("Could not save product.");
    }
  };

  const format = (n: number) =>
    n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

  return (
    <Layout>
      <PageHeader
        title="Products"
        subtitle={`${products.length} item${products.length !== 1 ? "s" : ""}`}
        action={
          isAdmin ? (
            <Button
              onClick={() => {
                setEditing(undefined);
                setShowModal(true);
              }}
            >
              Add product
            </Button>
          ) : undefined
        }
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
          action={
            isAdmin ? (
              <Button onClick={() => setShowModal(true)}>
                Add the first product
              </Button>
            ) : undefined
          }
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
                  {isAdmin ? (
                    <>
                      <Button
                        variant="secondary"
                        className={styles.actionButton}
                        onClick={() => {
                          setEditing(product);
                          setShowModal(true);
                        }}
                      >
                        Edit
                      </Button>
                      <Button
                        variant="danger"
                        className={styles.actionButton}
                        onClick={() => handleDelete(product.public_id)}
                      >
                        Delete
                      </Button>
                    </>
                  ) : (
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
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {showModal && (
        <ProductModal
          product={editing}
          onClose={() => {
            setShowModal(false);
            setEditing(undefined);
          }}
          onSave={handleSave}
        />
      )}
    </Layout>
  );
}

interface ProductModalProps {
  product?: Product;
  onClose: () => void;
  onSave: (data: Omit<Product, "public_id">) => void;
}

function ProductModal({ product, onClose, onSave }: ProductModalProps) {
  const [name, setName] = useState(product?.name ?? "");
  const [description, setDescription] = useState(product?.description ?? "");
  const [price, setPrice] = useState(product?.price.toString() ?? "");

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalPanel}>
        <h3 className={styles.modalTitle}>
          {product ? "Edit product" : "New product"}
        </h3>
        <div className={styles.modalForm}>
          <div className={styles.field}>
            <label className={styles.fieldLabel}>Name</label>
            <input
              className={styles.fieldInput}
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Product name"
              autoFocus
            />
          </div>
          <div className={styles.field}>
            <label className={styles.fieldLabel}>Description</label>
            <textarea
              className={`${styles.fieldInput} ${styles["resize-none"]}`}
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Optional"
            />
          </div>
          <div className={styles.field}>
            <label className={styles.fieldLabel}>Price (R$)</label>
            <input
              type="number"
              step="0.01"
              min="0"
              className={`${styles.fieldInput} ${styles.mono}`}
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              placeholder="0.00"
            />
          </div>
        </div>
        <div className={styles.modalActions}>
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button
            onClick={() => {
              if (!name.trim() || !price) return;
              onSave({
                name,
                description: description || null,
                price: parseFloat(price),
              });
            }}
          >
            Save product
          </Button>
        </div>
      </div>
    </div>
  );
}
