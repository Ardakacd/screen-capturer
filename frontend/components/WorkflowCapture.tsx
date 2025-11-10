"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import { StartTaskRequest, StartTaskResponse, WorkflowDisplay } from "@/types";
import LoginExplanationModal from "./LoginExplanationModal";

interface WorkflowCaptureProps {
  onWorkflowCaptured: (workflow: WorkflowDisplay) => void;
  onCapturingChange: (isCapturing: boolean) => void;
  isCapturing: boolean;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function WorkflowCapture({
  onWorkflowCaptured,
  onCapturingChange,
  isCapturing,
}: WorkflowCaptureProps) {
  const [task, setTask] = useState("");
  const [loginUrl, setLoginUrl] = useState("");
  const [sessionPath, setSessionPath] = useState("");
  const [error, setError] = useState("");
  const [showLoginModal, setShowLoginModal] = useState(false);

  useEffect(() => {
    const hasSeenModal = localStorage.getItem("hasSeenLoginModal");
    if (!hasSeenModal) {
      setShowLoginModal(true);
      localStorage.setItem("hasSeenLoginModal", "true");
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!task.trim()) {
      setError("Please enter a task description");
      return;
    }

    onCapturingChange(true);

    try {
      const taskId = new Date().toISOString();

      const requestData: StartTaskRequest = {
        login_url: loginUrl.trim() || undefined,
        session_path: sessionPath.trim(),
        task: task.trim(),
        task_id: taskId,
      };

      const response = await axios.post<StartTaskResponse>(
        `${API_URL}/tasks/start`,
        requestData,
        {
          timeout: 300000, // 5 minutes timeout
        }
      );

      // Add client metadata to backend response
      const workflowDisplay: WorkflowDisplay = {
        ...response.data,
        task_id: taskId,
        task: task.trim(),
      };

      onWorkflowCaptured(workflowDisplay);
    } catch (err: any) {
      console.error("Error capturing workflow:", err);
      setError(
        err.response?.data?.detail ||
          "Failed to capture workflow. Please try again."
      );
      onCapturingChange(false);
    }
  };

  const exampleTasks = [
    {
      task: "How to connect your Slack account in Notion?",
      loginUrl: "https://www.notion.so/login",
      sessionPath: "notion_session.json",
    },
    {
      task: "How do I change language from English to French in Notion?",
      loginUrl: "https://www.notion.so/login",
      sessionPath: "notion_session.json",
    },
    {
      task: "How do I share my workspace with my teammate in Notion?",
      loginUrl: "https://www.notion.so/login",
      sessionPath: "notion_session.json",
    },

    {
      task: "How to filter issues with high priority in Linear?",
      loginUrl: "https://linear.app/login",
      sessionPath: "linear_session.json",
    },
  ];

  return (
    <>
      <LoginExplanationModal
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
      />

      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Capture a Workflow
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Task Input */}
          <div>
            <label
              htmlFor="task"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              What do you want to learn? <span className="text-red-500">*</span>
            </label>
            <textarea
              id="task"
              value={task}
              onChange={(e) => setTask(e.target.value)}
              placeholder="e.g., How to connect your Slack account to Notion?"
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white resize-none disabled:opacity-50 disabled:cursor-not-allowed"
              rows={3}
              required
              disabled={isCapturing}
            />
          </div>

          {/* Login URL Input */}
          <div>
            <div className="flex items-center gap-2 mb-2">
              <label
                htmlFor="loginUrl"
                className="text-sm font-medium text-gray-700 dark:text-gray-300"
              >
                Login URL (optional)
              </label>
              <button
                type="button"
                onClick={() => setShowLoginModal(true)}
                className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors"
                title="How login works"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </button>
            </div>
            <input
              id="loginUrl"
              type="url"
              value={loginUrl}
              onChange={(e) => setLoginUrl(e.target.value)}
              placeholder="https://www.notion.so/login"
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={isCapturing}
            />
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              Login URL for the site (e.g., https://www.notion.so/login). After
              you click Start Capture, Playwright will open a browser window
              where you can login manually. Only needed for the first task.
            </p>
          </div>

          {/* Session Path Input */}
          <div>
            <label
              htmlFor="sessionPath"
              className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Session File Name <span className="text-red-500">*</span>
            </label>
            <input
              id="sessionPath"
              type="text"
              value={sessionPath}
              onChange={(e) => setSessionPath(e.target.value)}
              placeholder="notion_session.json"
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={isCapturing}
              required
            />
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              Where to store session cookies (reused for subsequent tasks)
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
              <div className="flex items-start">
                <svg
                  className="w-5 h-5 text-red-600 dark:text-red-400 mt-0.5 mr-3"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
                <p className="text-sm text-red-800 dark:text-red-200">
                  {error}
                </p>
              </div>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isCapturing}
            className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:transform-none disabled:hover:shadow-lg"
          >
            {isCapturing ? (
              <span className="inline-flex items-center justify-center gap-2">
                <svg
                  className="animate-spin h-5 w-5"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Capturing...
              </span>
            ) : (
              "Start Capture"
            )}
          </button>
        </form>

        {/* Example Tasks */}
        <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">
            Example tasks:
          </h3>
          <div className="space-y-2">
            {exampleTasks.map((example, index) => (
              <button
                key={index}
                type="button"
                onClick={() => {
                  setTask(example.task);
                  setLoginUrl(example.loginUrl);
                  setSessionPath(example.sessionPath);
                }}
                disabled={isCapturing}
                className="w-full text-left px-4 py-3 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span className="text-gray-900 dark:text-white font-medium">
                  {example.task}
                </span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
