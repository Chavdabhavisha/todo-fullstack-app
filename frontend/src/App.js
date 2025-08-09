import React, { useEffect, useState, useRef } from "react";
import './App.css';

function App() {
  const [todos, setTodos] = useState([]);
  const [text, setText] = useState("");
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const [editId, setEditId] = useState(null);
  const [editText, setEditText] = useState("");
  const editInputRef = useRef(null);

  const API_BASE = "https://todo-fullstack-application-enht.onrender.com/api/todos";
const AUTH_API = "https://todo-fullstack-application-enht.onrender.com/api/auth/google-login";


  useEffect(() => {
    if (token) fetchTodos();
  }, [token]);

  useEffect(() => {
    if (editId && editInputRef.current) {
      editInputRef.current.focus();
    }
  }, [editId]);

  const fetchTodos = async () => {
    try {
      const res = await fetch(`${API_BASE}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.status === 401) {
        localStorage.removeItem("token");
        setToken("");
        setIsAuthenticated(false);
        return;
      }

      const data = await res.json();
      setTodos(data);
      setIsAuthenticated(true);
    } catch (err) {
      console.error("Error fetching todos:", err);
    }
  };

  const addTodo = async () => {
  if (!text.trim()) return;

  try {
    const res = await fetch(`${API_BASE}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ text }),
    });

    if (res.ok) {
      alert("✅ Todo created. Email sent!");
    } else {
      alert("⚠️ Failed to add todo.");
    }

    setText("");
    fetchTodos();
  } catch (err) {
    console.error("Error adding todo:", err);
    alert("❌ Something went wrong.");
  }
};


  const toggleTodo = async (id, completed) => {
    try {
      await fetch(`${API_BASE}/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ completed: !completed }),
      });
      fetchTodos();
    } catch (err) {
      console.error("Error toggling todo:", err);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await fetch(`${API_BASE}/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchTodos();
    } catch (err) {
      console.error("Error deleting todo:", err);
    }
  };

  const updateTodoText = async (id) => {
    if (!editText.trim()) return;

    try {
      await fetch(`${API_BASE}/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ text: editText }),
      });
      setEditId(null);
      setEditText("");
      fetchTodos();
    } catch (err) {
      console.error("Error updating todo text:", err);
    }
  };

  const handleGoogle = (response) => {
    fetch(AUTH_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ credential: response.credential }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.token) {
          localStorage.setItem("token", data.token);
          setToken(data.token);
          setIsAuthenticated(true);
        } else {
          alert("Login failed.");
        }
      })
      .catch((err) => {
        console.error("Login failed", err);
      });
  };

  useEffect(() => {
    if (window.google && window.google.accounts) {
      window.google.accounts.id.initialize({
        client_id:
          "274333479323-h9ekpt485olvrf0ranojadnonorhf7t5.apps.googleusercontent.com",
        callback: handleGoogle,
      });

      window.google.accounts.id.renderButton(
        document.getElementById("googleBtn"),
        { theme: "outline", size: "large" }
      );
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken("");
    setTodos([]);
    setIsAuthenticated(false);
  };

  return (
    <div className="container">
      <h2>📝 Todo App</h2>

      {!isAuthenticated ? (
        <div>
          <div id="googleBtn"></div>
          <p>Please login with Google to manage your todos.</p>
        </div>
      ) : (
        <>
          <button onClick={handleLogout} style={{ float: "right" }}>
            Logout
          </button>

          <div className="todo-input">
            <input
              type="text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Add todo"
              disabled={!!editId}
            />
            <button onClick={addTodo} disabled={!!editId}>
              Add
            </button>
          </div>

          <ul style={{ marginTop: "1rem" }}>
            {todos.length === 0 ? (
              <li>No todos yet. Add something! ✍️</li>
            ) : (
              todos.map((todo) => (
                <li key={todo._id}>
                  <input
                    type="checkbox"
                    checked={todo.completed}
                    onChange={() => toggleTodo(todo._id, todo.completed)}
                  />

                  {editId === todo._id ? (
                    <>
                      <input
                        type="text"
                        value={editText}
                        ref={editInputRef}
                        onChange={(e) => setEditText(e.target.value)}
                      />
                      <button onClick={() => updateTodoText(todo._id)}>
                        💾 Save
                      </button>
                      <button onClick={() => setEditId(null)}>Cancel</button>
                    </>
                  ) : (
                    <>
                      <span
                        style={{
                          textDecoration: todo.completed
                            ? "line-through"
                            : "none",
                          color: todo.completed ? "gray" : "black",
                          marginRight: "10px",
                        }}
                      >
                        {todo.text}
                      </span>
                      <button
                        onClick={() => {
                          setEditId(todo._id);
                          setEditText(todo.text);
                        }}
                      >
                        ✏️ Edit
                      </button>
                    </>
                  )}

                  <button onClick={() => deleteTodo(todo._id)}>
                    ❌ Delete
                  </button>
                </li>
              ))
            )}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;