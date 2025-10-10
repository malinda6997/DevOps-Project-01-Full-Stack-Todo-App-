/**
 * TodoForm Component
 * Modern form for creating new todos
 */
import React, { useState } from "react";
import { motion } from "framer-motion";
import { Plus, Loader } from "lucide-react";
import "./TodoForm.css";

const TodoForm = ({ onAdd }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsLoading(true);
    try {
      await onAdd({
        title: title.trim(),
        description: description.trim(),
        completed: false,
      });

      // Reset form
      setTitle("");
      setDescription("");
      setIsExpanded(false);
    } catch (error) {
      console.error("Error adding todo:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTitleFocus = () => {
    setIsExpanded(true);
  };

  const handleCancel = () => {
    setTitle("");
    setDescription("");
    setIsExpanded(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="todo-form-container"
    >
      <form
        onSubmit={handleSubmit}
        className={`todo-form ${isExpanded ? "expanded" : ""}`}
      >
        <div className="form-header">
          <div className="input-group">
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              onFocus={handleTitleFocus}
              placeholder="What needs to be done?"
              className="title-input"
              disabled={isLoading}
              maxLength={100}
            />
            {!isExpanded && (
              <motion.button
                type="submit"
                className="quick-add-button"
                disabled={!title.trim() || isLoading}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {isLoading ? (
                  <Loader className="spinning" size={18} />
                ) : (
                  <Plus size={18} />
                )}
              </motion.button>
            )}
          </div>
        </div>

        {isExpanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2 }}
            className="form-expanded"
          >
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Add a description (optional)..."
              className="description-input"
              rows="3"
              disabled={isLoading}
              maxLength={500}
            />

            <div className="form-actions">
              <div className="character-count">
                <span className="title-count">{title.length}/100</span>
                {description && (
                  <span className="desc-count">{description.length}/500</span>
                )}
              </div>

              <div className="action-buttons">
                <button
                  type="button"
                  onClick={handleCancel}
                  className="cancel-button"
                  disabled={isLoading}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="add-button"
                  disabled={!title.trim() || isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader className="spinning" size={16} />
                      Adding...
                    </>
                  ) : (
                    <>
                      <Plus size={16} />
                      Add Todo
                    </>
                  )}
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </form>
    </motion.div>
  );
};

export default TodoForm;
