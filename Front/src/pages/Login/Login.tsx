import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { Button, Input, ErrorMessage } from '../../components/UI'
import { login as loginService, me as getMeService } from '../../services/auth'
import styles from './Login.module.scss'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()

  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)



  return (
    <div className={styles.page}>
      <div className={styles.sidebar}>
        <span className={styles.sidebarLabel}>Professional Practice in Systems Analysis and Development </span>
        <div>
          <p className={styles.sidebarTitle}>
            Orders management <br />
          </p>
        </div>
        <p className={styles.sidebarFooter}>Mackenzie</p>
      </div>

      <div className={styles.formPane}>
        <div className={styles.formWrap}>
          <div className={styles.formHeader}>
            <h2 className={styles.formHeading}>Sign in</h2>
            <p className={styles.formSubtitle}>
              No account?{' '}
              <Link to="/register" className={styles.link}>
                Create one
              </Link>
            </p>
          </div>

          <form onSubmit={async (e) => {
            e.preventDefault()
            setError('')
            setLoading(true)
            try {
              const { access_token } = await loginService(identifier, password)
              const user = await getMeService(access_token)
              login(access_token, user)
              navigate('/products')
            } catch {
              setError('Invalid credentials. Check your username and password.')
            } finally {
              setLoading(false)
            }
          }} className={styles.form}>
            {error && <ErrorMessage message={error} />}

            <Input
              label="Username or email"
              type="text"
              value={identifier}
              onChange={e => setIdentifier(e.target.value)}
              placeholder="your_username"
              required
              autoFocus
            />
            <Input
              label="Password"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />

            <Button type="submit" loading={loading} className={styles.submitButton}>
              Sign in
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}
