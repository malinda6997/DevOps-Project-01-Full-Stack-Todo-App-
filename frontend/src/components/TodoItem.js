/**
 * TodoItem Component
 * Modern, interactive todo item with animations
 */
import React, { useState } from "react";
import { motion } from "framer-motion";
import { Check, Edit3, Trash2, X, Save } from "lucide-react";
import "./TodoItem.css";

const TodoItem = ({ todo, onUpdate, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description);
  const [isLoading, setIsLoading] = useState(false);

  const handleToggleComplete = async () => {
    setIsLoading(true);
    try {
      await onUpdate(todo.id, { completed: !todo.completed });
    } catch (error) {
      console.error("Error toggling todo:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveEdit = async () => {
    if (!editTitle.trim()) return;

    setIsLoading(true);
    try {
      await onUpdate(todo.id, {
        title: editTitle.trim(),
        description: editDescription.trim(),
      });
      setIsEditing(false);
    } catch (error) {
      console.error("Error updating todo:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description);
    setIsEditing(false);
  };

  const handleDelete = async () => {
    setIsLoading(true);
    try {
      await onDelete(todo.id);
    } catch (error) {
      console.error("Error deleting todo:", error);
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, x: -100 }}
      transition={{ duration: 0.3 }}
      className={`todo-item ${todo.completed ? "completed" : ""} ${
        isLoading ? "loading" : ""
      }`}
    >
      <div className="todo-content">
        <button
          className={`check-button ${todo.completed ? "checked" : ""}`}
          onClick={handleToggleComplete}
          disabled={isLoading || isEditing}
        >
          {todo.completed && <Check size={16} />}
        </button>

        {isEditing ? (
          <div className="edit-form">
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="edit-title"
              placeholder="Todo title..."
              autoFocus
            />
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="edit-description"
              placeholder="Description (optional)..."
              rows="2"
            />
          </div>
        ) : (
          <div className="todo-text">
            <h3
              className={`todo-title ${todo.completed ? "completed-text" : ""}`}
            >
              {todo.title}
            </h3>
            {todo.description && (
              <p
                className={`todo-description ${
                  todo.completed ? "completed-text" : ""
                }`}
              >
                {todo.description}
              </p>
            )}
            <span className="todo-date">
              {new Date(todo.created_at).toLocaleDateString()}
            </span>
          </div>
        )}
      </div>

      <div className="todo-actions">
        {isEditing ? (
          <>
            <button
              className="action-button save"
              onClick={handleSaveEdit}
              disabled={isLoading || !editTitle.trim()}
            >
              <Save size={16} />
            </button>
            <button
              className="action-button cancel"
              onClick={handleCancelEdit}
              disabled={isLoading}
            >
              <X size={16} />
            </button>
          </>
        ) : (
          <>
            <button
              className="action-button edit"
              onClick={() => setIsEditing(true)}
              disabled={isLoading}
            >
              <Edit3 size={16} />
            </button>
            <button
              className="action-button delete"
              onClick={handleDelete}
              disabled={isLoading}
            >
              <Trash2 size={16} />
            </button>
          </>
        )}
      </div>
    </motion.div>
  );
};

export default TodoItem;
