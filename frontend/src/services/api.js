/**
 * API Service for Todo App
 * Connects React frontend to Flask backend
 */
import axios from "axios";

// Base URL for Flask backend
const BASE_URL = "http://127.0.0.1:5000/api";

// Create axios instance with default config
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // 10 seconds timeout
});

// API endpoints
export const todoAPI = {
  // Get all todos
  getAllTodos: async () => {
    try {
      const response = await api.get("/todos");
      return response.data;
    } catch (error) {
      console.error("Error fetching todos:", error);
      throw error;
    }
  },

  // Create new todo
  createTodo: async (todoData) => {
    try {
      const response = await api.post("/todos", todoData);
      return response.data;
    } catch (error) {
      console.error("Error creating todo:", error);
      throw error;
    }
  },

  // Get single todo by ID
  getTodo: async (id) => {
    try {
      const response = await api.get(`/todos/${id}`);
      return response.data;
    } catch (error) {
      console.error("Error fetching todo:", error);
      throw error;
    }
  },

  // Update todo
  updateTodo: async (id, todoData) => {
    try {
      const response = await api.put(`/todos/${id}`, todoData);
      return response.data;
    } catch (error) {
      console.error("Error updating todo:", error);
      throw error;
    }
  },

  // Delete todo
  deleteTodo: async (id) => {
    try {
      const response = await api.delete(`/todos/${id}`);
      return response.data;
    } catch (error) {
      console.error("Error deleting todo:", error);
      throw error;
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await api.get("/health");
      return response.data;
    } catch (error) {
      console.error("Backend health check failed:", error);
      throw error;
    }
  },
};

export default todoAPI;
