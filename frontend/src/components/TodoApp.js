/**
 * TodoApp Component
 * Main todo application with modern UI and backend integration
 */
import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  CheckCircle,
  Circle,
  Filter,
  Search,
  Moon,
  Sun,
  Wifi,
  WifiOff,
} from "lucide-react";
import { Toaster, toast } from "react-hot-toast";
import TodoForm from "./TodoForm";
import TodoItem from "./TodoItem";
import { todoAPI } from "../services/api";
import "./TodoApp.css";

const TodoApp = () => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all"); // all, active, completed
  const [searchTerm, setSearchTerm] = useState("");
  const [darkMode, setDarkMode] = useState(false);
  const [isOnline, setIsOnline] = useState(true);

  // Load todos on component mount
  useEffect(() => {
    loadTodos();
    checkBackendHealth();

    // Check initial theme preference
    const savedTheme = localStorage.getItem("theme");
    if (
      savedTheme === "dark" ||
      (!savedTheme && window.matchMedia("(prefers-color-scheme: dark)").matches)
    ) {
      setDarkMode(true);
    }
  }, []);

  // Apply theme
  useEffect(() => {
    document.documentElement.setAttribute(
      "data-theme",
      darkMode ? "dark" : "light"
    );
    localStorage.setItem("theme", darkMode ? "dark" : "light");
  }, [darkMode]);

  const checkBackendHealth = async () => {
    try {
      await todoAPI.healthCheck();
      setIsOnline(true);
    } catch (error) {
      setIsOnline(false);
      toast.error("Backend server is not responding");
    }
  };

  const loadTodos = async () => {
    try {
      setLoading(true);
      const response = await todoAPI.getAllTodos();
      setTodos(response.todos || []);
      setIsOnline(true);
    } catch (error) {
      console.error("Error loading todos:", error);
      setIsOnline(false);
      toast.error("Failed to load todos");
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (todoData) => {
    try {
      const response = await todoAPI.createTodo(todoData);
      setTodos((prev) => [response.todo, ...prev]);
      toast.success("Todo added successfully!");
    } catch (error) {
      console.error("Error adding todo:", error);
      toast.error("Failed to add todo");
      throw error;
    }
  };

  const handleUpdateTodo = async (id, updates) => {
    try {
      const response = await todoAPI.updateTodo(id, updates);
      setTodos((prev) =>
        prev.map((todo) => (todo.id === id ? response.todo : todo))
      );
      toast.success("Todo updated!");
    } catch (error) {
      console.error("Error updating todo:", error);
      toast.error("Failed to update todo");
      throw error;
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      await todoAPI.deleteTodo(id);
      setTodos((prev) => prev.filter((todo) => todo.id !== id));
      toast.success("Todo deleted!");
    } catch (error) {
      console.error("Error deleting todo:", error);
      toast.error("Failed to delete todo");
      throw error;
    }
  };

  // Filter todos based on status and search term
  const filteredTodos = todos.filter((todo) => {
    const matchesFilter =
      filter === "all"
        ? true
        : filter === "active"
        ? !todo.completed
        : filter === "completed"
        ? todo.completed
        : true;

    const matchesSearch =
      searchTerm === "" ||
      todo.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      todo.description.toLowerCase().includes(searchTerm.toLowerCase());

    return matchesFilter && matchesSearch;
  });

  const totalTodos = todos.length;
  const completedTodos = todos.filter((todo) => todo.completed).length;
  const activeTodos = totalTodos - completedTodos;

  return (
    <div className={`todo-app ${darkMode ? "dark" : "light"}`}>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: darkMode ? "#1f2937" : "#ffffff",
            color: darkMode ? "#f9fafb" : "#111827",
            border: darkMode ? "1px solid #374151" : "1px solid #e5e7eb",
          },
        }}
      />

      <div className="app-container">
        {/* Header */}
        <header className="app-header">
          <div className="header-content">
            <div className="header-left">
              <h1 className="app-title">
                <CheckCircle className="title-icon" />
                TodoMaster
              </h1>
              <div className="connection-status">
                {isOnline ? (
                  <span className="status online">
                    <Wifi size={14} />
                    Connected
                  </span>
                ) : (
                  <span className="status offline">
                    <WifiOff size={14} />
                    Offline
                  </span>
                )}
              </div>
            </div>

            <div className="header-right">
              <button
                className="theme-toggle"
                onClick={() => setDarkMode(!darkMode)}
                title={`Switch to ${darkMode ? "light" : "dark"} mode`}
              >
                {darkMode ? <Sun size={20} /> : <Moon size={20} />}
              </button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="main-content">
          {/* Add Todo Form */}
          <TodoForm onAdd={handleAddTodo} />

          {/* Stats */}
          <div className="todo-stats">
            <div className="stat-card">
              <Circle className="stat-icon active" />
              <div className="stat-content">
                <span className="stat-number">{activeTodos}</span>
                <span className="stat-label">Active</span>
              </div>
            </div>
            <div className="stat-card">
              <CheckCircle className="stat-icon completed" />
              <div className="stat-content">
                <span className="stat-number">{completedTodos}</span>
                <span className="stat-label">Completed</span>
              </div>
            </div>
            <div className="stat-card">
              <Filter className="stat-icon total" />
              <div className="stat-content">
                <span className="stat-number">{totalTodos}</span>
                <span className="stat-label">Total</span>
              </div>
            </div>
          </div>

          {/* Search and Filter */}
          <div className="controls">
            <div className="search-container">
              <Search className="search-icon" />
              <input
                type="text"
                placeholder="Search todos..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>

            <div className="filter-buttons">
              {["all", "active", "completed"].map((filterType) => (
                <button
                  key={filterType}
                  className={`filter-button ${
                    filter === filterType ? "active" : ""
                  }`}
                  onClick={() => setFilter(filterType)}
                >
                  {filterType.charAt(0).toUpperCase() + filterType.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Todo List */}
          <div className="todo-list">
            {loading ? (
              <div className="loading-state">
                <div className="loading-spinner"></div>
                <p>Loading your todos...</p>
              </div>
            ) : filteredTodos.length === 0 ? (
              <div className="empty-state">
                {searchTerm ? (
                  <>
                    <Search className="empty-icon" />
                    <h3>No todos found</h3>
                    <p>Try adjusting your search or filter criteria</p>
                  </>
                ) : totalTodos === 0 ? (
                  <>
                    <CheckCircle className="empty-icon" />
                    <h3>No todos yet</h3>
                    <p>Create your first todo to get started!</p>
                  </>
                ) : (
                  <>
                    <Filter className="empty-icon" />
                    <h3>No {filter} todos</h3>
                    <p>
                      All your {filter === "active" ? "active" : "completed"}{" "}
                      todos will appear here
                    </p>
                  </>
                )}
              </div>
            ) : (
              <AnimatePresence>
                {filteredTodos.map((todo) => (
                  <TodoItem
                    key={todo.id}
                    todo={todo}
                    onUpdate={handleUpdateTodo}
                    onDelete={handleDeleteTodo}
                  />
                ))}
              </AnimatePresence>
            )}
          </div>
        </main>
      </div>
    </div>
  );
};

export default TodoApp;
