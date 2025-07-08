import { useState, useEffect } from 'react'
import './App.css'

/**
 * Decodes a JWT token and returns its payload.
 * @param {string} token - JWT string.
 * @returns {object|null} Decoded payload or null if invalid.
 */
function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
    return JSON.parse(jsonPayload)
  } catch {
    return null
  }
}

// AWS and Auth environment configuration
const API_URL = "https://j76irwz266.execute-api.us-east-1.amazonaws.com/prod"
const COGNITO_DOMAIN = "https://us-east-1eeev1ta4c.auth.us-east-1.amazoncognito.com"
const CLIENT_ID = "2pcjgogv7lfe6r9213rn2krqq5"
const REDIRECT_URI = "https://staging.d11aup96239yxt.amplifyapp.com/"

function App() {
  const [todos, setTodos] = useState([])
  const [newTodo, setNewTodo] = useState("")
  const [dueDate, setDueDate] = useState("")
  const [token, setToken] = useState(localStorage.getItem("token"))
  const [email, setEmail] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  /**
   * Handles user authentication redirect, stores token, or redirects to login.
   */
  useEffect(() => {
    const hash = window.location.hash
    if (hash.includes("id_token")) {
      const params = new URLSearchParams(hash.substring(1))
      const idToken = params.get("id_token")
      if (idToken) {
        localStorage.setItem("token", idToken)
        setToken(idToken)
        window.history.replaceState(null, "", window.location.pathname)
      }
    }
    setIsLoading(false)

    // Redirect to login if no token found
    if (!localStorage.getItem("token")) {
      const loginUrl = `${COGNITO_DOMAIN}/login?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=token&scope=email+openid+phone`
      window.location.href = loginUrl
    }
  }, [])

  /**
   * On token update, decode and fetch user data.
   */
  useEffect(() => {
    if (!token) return
    const decoded = parseJwt(token)
    if (decoded && decoded.email) setEmail(decoded.email)
    fetchTodos()
  }, [token])

  /**
   * Fetches all todos from the backend (GET /get-all-todo).
   */
  async function fetchTodos() {
    try {
      const res = await fetch(`${API_URL}/get-all-todo`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (!res.ok) throw new Error("Failed to fetch todos")
      const data = await res.json()
      setTodos(data)
    } catch (err) {
      console.error(err)
    }
  }

  /**
   * Creates a new todo item (POST /create-todo).
   */
  async function handleAdd() {
    if (!token || !newTodo.trim()) return
    const todoData = {
      title: newTodo,
      dueDate: dueDate ? new Date(dueDate).toISOString() : null
    }
    try {
      const res = await fetch(`${API_URL}/create-todo`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(todoData)
      })
      if (!res.ok) throw new Error("Failed to add todo")
      await fetchTodos()
      setNewTodo("")
      setDueDate("")
    } catch (err) {
      console.error(err)
    }
  }

  /**
   * Toggles the completed status of a todo item (PATCH /update-todo/{id}).
   * @param {object} todo - The todo item to update.
   */
  async function toggleCompleted(todo) {
    if (!token) return
    try {
      const res = await fetch(`${API_URL}/update-todo/${todo.todoId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ completed: !todo.completed })
      })
      if (!res.ok) throw new Error("Failed to update todo")
      await fetchTodos()
    } catch (err) {
      console.error(err)
    }
  }

  /**
   * Deletes a todo item (DELETE /delete-todo/{id}).
   * @param {string} todoId - The ID of the todo to delete.
   */
  async function handleDelete(todoId) {
    if (!token) return
    try {
      const res = await fetch(`${API_URL}/delete-todo/${todoId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      if (!res.ok) throw new Error("Failed to delete todo")
      await fetchTodos()
    } catch (err) {
      console.error(err)
    }
  }

  /**
   * Logs out the user by clearing the token and redirecting.
   */
  function handleLogout() {
    localStorage.removeItem("token")
    setToken(null)
    setEmail(null)
    const logoutUrl = `${COGNITO_DOMAIN}/logout?client_id=${CLIENT_ID}&logout_uri=${REDIRECT_URI}`
    window.location.href = logoutUrl
  }

  if (isLoading) {
    return (
      <div className="container">
        <h1>My Todos</h1>
        <p>Loading... please wait</p>
      </div>
    )
  }

  return (
    <div className="container">
      <h1>My Todos</h1>

      {token && email && (
        <div style={{ marginBottom: "1em" }}>
          <strong>Logged in as: {email}</strong>
        </div>
      )}

      {token && (
        <div style={{ textAlign: "right", marginBottom: "1em" }}>
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}

      {token && (
        <>
          <div className="input-area">
            <input
              type="text"
              value={newTodo}
              onChange={(e) => setNewTodo(e.target.value)}
              placeholder="Enter a new todo"
            />
            <input
              type="datetime-local"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              placeholder="Due date and time"
            />
            <button onClick={handleAdd}>Add</button>
          </div>

          <ul className="todo-list">
            {todos.map((todo) => (
              <li key={todo.todoId}>
                <input
                  type="checkbox"
                  checked={todo.completed}
                  onChange={() => toggleCompleted(todo)}
                />
                <span className={todo.completed ? 'done' : ''}>
                  {todo.title}{" "}
                  {todo.dueDate && (
                    <small style={{ color: 'gray', fontSize: '0.8em' }}>
                      (Due {new Date(todo.dueDate).toLocaleString()})
                    </small>
                  )}
                </span>
                <button onClick={() => handleDelete(todo.todoId)} style={{ marginLeft: 8 }}>
                  Delete
                </button>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  )
}

export default App
