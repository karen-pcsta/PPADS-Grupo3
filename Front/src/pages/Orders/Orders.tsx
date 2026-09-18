import { useState, useEffect } from "react";
import {
  Layout,
  PageHeader,
  StatusTag,
  EmptyState,
  ErrorMessage,
} from "../../components/UI";
import { useAuth } from "../../context/AuthContext";
import type { Order } from "../../types/types";
import {
  getAllOrders,
} from "../../services/orders";
import styles from "./Orders.module.scss";

export default function OrdersPage() {
  const { isAdmin } = useAuth();

  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        const data = await getAllOrders();
        setOrders(data);
      } catch {
        setError("Failed to load orders.");
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);


  const format = (n: number) =>
    n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
  const fmtDate = (s: string) =>
    new Date(s).toLocaleDateString("en-US", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });

  return (
    <Layout>
      <PageHeader
        title="Orders"
        subtitle={
          isAdmin ? "All orders across all customers" : "Your order history"
        }
      />

      {error && (
        <div className={styles.pageError}>
          <ErrorMessage message={error} />
        </div>
      )}

      {loading ? (
        <div className={styles.skeletonList}>
          {[1, 2, 3].map((i) => (
            <div key={i} className={styles.skeletonRow} />
          ))}
        </div>
      ) : orders.length === 0 ? (
        <EmptyState message="No orders yet." />
      ) : (
        <div className={styles.list}>
          {orders.map((order) => {
            const isOpen = expanded === order.public_id;

            return (
              <div key={order.public_id} className={styles.order}>
                <div
                  className={styles.orderRow}
                  onClick={() => setExpanded(isOpen ? null : order.public_id)}
                >
                  <span className={styles.orderId}>
                    {order.public_id}
                  </span>
                  <span className={styles.orderDate}>
                    {fmtDate(order.created_at)}
                  </span>
                  <StatusTag status={order.status} />
                  <span className={styles.spacer} />
                  <span className={styles.orderTotal}>
                    {format(order.total)}
                  </span>
                  <span className={styles.chevron}>
                    {isOpen ? "▲" : "▼"}
                  </span>
                </div>

                {isOpen && (
                  <div className={styles.orderDetail}>
                    <table className={styles.table}>
                      <thead>
                        <tr className={styles.headRow}>
                          <th className={styles.thItem}>Item</th>
                          <th className={styles.thQty}>Qty</th>
                          <th className={styles.thPrice}>Unit price</th>
                          <th className={styles.thSubtotal}>Subtotal</th>
                        </tr>
                      </thead>
                      <tbody>
                        {order.items.map((item, idx) => (
                          <tr key={idx} className={styles.itemRow}>
                            <td className={styles.cellItem}>
                              {item.product.name}
                            </td>
                            <td className={styles.cellQty}>
                              {item.quantity}
                            </td>
                            <td className={styles.cellPrice}>
                              {format(item.unit_price)}
                            </td>
                            <td className={styles.cellSubtotal}>
                              {format(item.unit_price * item.quantity)}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </Layout>
  );
}
