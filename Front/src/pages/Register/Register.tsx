import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { Button, Input, ErrorMessage } from '../../components/UI'
import { register as registerService, me as getMeService } from '../../services/auth'
import styles from './Register.module.scss'


export default function RegisterPage() {
  const { login } = useAuth()
  const navigate = useNavigate()

  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)

  const validate = () => {
    const next: Record<string, string> = {}
    if (!username.trim()) next.username = 'Username is required.'
    if (!/\S+@\S+\.\S+/.test(email)) next.email = 'Enter a valid email address.'
    if (password.length < 8) next.password = 'Password must be at least 8 characters.'
    return next
  }



  return (
    <div className={styles.page}>
      <div className={styles.sidebar}>
        <span className={styles.sidebarLabel}>Orders</span>
        <div>
          <p className={styles.sidebarTitle}>
            Your account.<br />
            <span className={styles.sidebarMuted}>Your orders, your history.</span>
          </p>
        </div>
        <p className={styles.sidebarFooter}>&copy; {new Date().getFullYear()} Orders Management</p>
      </div>

      <div className={styles.formPane}>
        <div className={styles.formWrap}>
          <div className={styles.formHeader}>
            <h2 className={styles.formHeading}>Create account</h2>
            <p className={styles.formSubtitle}>
              Already have one?{' '}
              <Link to="/login" className={styles.link}>
                Sign in
              </Link>
            </p>
          </div>

          <form onSubmit={async (e) => {
            e.preventDefault()
            const v = validate()
            if (Object.keys(v).length) { setErrors(v); return }
            setErrors({})
            setLoading(true)
            try {
              const { access_token } = await registerService(username, email, password)
              const user = await getMeService(access_token)
              login(access_token, user)
              navigate('/products')
            } catch {
              setErrors({ form: 'Registration failed. Username or email may already be in use.' })
            } finally {
              setLoading(false)
            }
          }} className={styles.form}>
            {errors.form && <ErrorMessage message={errors.form} />}

            <Input
              label="Username"
              type="text"
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="your_username"
              error={errors.username}
              autoFocus
            />
            <Input
              label="Email"
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="you@example.com"
              error={errors.email}
            />
            <Input
              label="Password"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="at least 8 characters"
              error={errors.password}
            />

            <Button type="submit" loading={loading} className={styles.submitButton}>
              Create account
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}
