import type { ReactNode } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import styles from './UI.module.scss'

export function Layout({ children }: { children: ReactNode }) {
  const { user, logout, isAdmin } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className={styles.layout}>
      <header className={styles.header}>
        <div className={styles.brand}>
          <Link to="/products" className={styles.brandLink}>
            Orders Management
          </Link>
        </div>
        <nav className={styles.nav}>
          <Link to="/products" className={styles.navLink}>
            Products
          </Link>
          <Link to="/cart" className={styles.navLink}>
            Cart
          </Link>
          <Link to="/orders" className={styles.navLink}>
            Orders
          </Link>
        </nav>
        {user && (
          <div className={styles.userSection}>
            <span className={styles.username}>{user.username}</span>
            {isAdmin && <span className={styles.adminBadge}>admin</span>}
            <button onClick={handleLogout} className={styles.signOut}>
              Sign out
            </button>
          </div>
        )}
      </header>
      <main className={styles.main}>{children}</main>
    </div>
  )
}


const tagStyles: Record<string, string> = {
  pending: styles.pending,
  confirmed: styles.confirmed,
  processing: styles.processing,
  finalized: styles.finalized,
  cancelled: styles.cancelled,
}

export function StatusTag({ status }: { status: string }) {
  const style = tagStyles[status.toLowerCase()] ?? styles.cancelled
  return (
    <span className={`${styles.statusTag} ${style}`}>
      {status}
    </span>
  )
}


type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  loading?: boolean
}

const buttonVariants: Record<ButtonVariant, string> = {
  primary: styles.primary,
  secondary: styles.secondary,
  ghost: styles.ghost,
  danger: styles.danger,
}

export function Button({ variant = 'primary', loading, children, className = '', disabled, ...props }: ButtonProps) {
  return (
    <button
      {...props}
      disabled={loading || disabled}
      className={`${styles.button} ${buttonVariants[variant]} ${className}`}
    >
      {loading ? 'Loading...' : children}
    </button>
  )
}

// Input

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string
  error?: string
}

export function Input({ label, error, className = '', ...props }: InputProps) {
  return (
    <div className={styles.field}>
      <label className={styles.label}>{label}</label>
      <input
        {...props}
        className={`${styles.input} ${error ? styles.inputError : ''} ${className}`}
      />
      {error && <span className={styles.errorText}>{error}</span>}
    </div>
  )
}

// PageHeader

export function PageHeader({ title, subtitle, action }: { title: string; subtitle?: string; action?: ReactNode }) {
  return (
    <div className={styles.pageHeader}>
      <div>
        <h1 className={styles.pageTitle}>{title}</h1>
        {subtitle && <p className={styles.pageSubtitle}>{subtitle}</p>}
      </div>
      {action && <div>{action}</div>}
    </div>
  )
}

// EmptyState

export function EmptyState({ message, action }: { message: string; action?: ReactNode }) {
  return (
    <div className={styles.emptyState}>
      <p className={styles.emptyMessage}>{message}</p>
      {action}
    </div>
  )
}

// ErrorMessage

export function ErrorMessage({ message }: { message: string }) {
  return (
    <div className={styles.errorMessage}>
      {message}
    </div>
  )
}
