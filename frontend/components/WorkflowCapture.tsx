"use client";

import { useState } from "react";
import axios from "axios";
import { StartTaskRequest, StartTaskResponse, WorkflowResult } from "@/types";

interface WorkflowCaptureProps {
  onWorkflowCaptured: (workflow: WorkflowResult) => void;
  onCapturingChange: (isCapturing: boolean) => void;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function WorkflowCapture({
  onWorkflowCaptured,
  onCapturingChange,
}: WorkflowCaptureProps) {
  const [task, setTask] = useState("");
  const [siteUrl, setSiteUrl] = useState("");
  const [loginUrl, setLoginUrl] = useState("");
  const [sessionPath, setSessionPath] = useState("session.json");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!task.trim()) {
      setError("Please enter a task description");
      return;
    }

    if (!siteUrl.trim()) {
      setError("Please enter a site URL");
      return;
    }

    onCapturingChange(true);

    try {
      const taskId = new Date().toISOString();

      const requestData: StartTaskRequest = {
        site_url: siteUrl.trim(),
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

      // Transform backend response to frontend format
      const workflowResult: WorkflowResult = {
        task_id: taskId,
        task: task.trim(),
        site_url: siteUrl.trim(),
        screenshot_paths: response.data.paths,
        explanation: response.data.explanation,
        total_steps: response.data.paths.length,
      };

      onWorkflowCaptured(workflowResult);
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
      task: "How to connect your Slack account to Notion?",
      siteUrl: "https://www.notion.so",
      loginUrl: "https://www.notion.so/login",
      sessionPath: "notion_session.json",
    },
    {
      task: "How do I change language from English to French?",
      siteUrl: "https://www.notion.so",
      loginUrl: "https://www.notion.so/login",
      sessionPath: "notion_session.json",
    },
    {
      task: "How do I invite a teammate?",
      siteUrl: "https://www.notion.so",
      loginUrl: "https://www.notion.so/login",
      sessionPath: "notion_session.json",
    },
  ];

  return (
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
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white resize-none"
            rows={3}
            required
          />
        </div>

        {/* Site URL Input */}
        <div>
          <label
            htmlFor="siteUrl"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Site URL <span className="text-red-500">*</span>
          </label>
          <input
            id="siteUrl"
            type="url"
            value={siteUrl}
            onChange={(e) => setSiteUrl(e.target.value)}
            placeholder="https://www.notion.so"
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            required
          />
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
            The main URL to navigate after login
          </p>
        </div>

        {/* Login URL Input */}
        <div>
          <label
            htmlFor="loginUrl"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Login URL (optional)
          </label>
          <input
            id="loginUrl"
            type="url"
            value={loginUrl}
            onChange={(e) => setLoginUrl(e.target.value)}
            placeholder="https://www.notion.so/login"
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          />
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
            Leave empty if same as Site URL
          </p>
        </div>

        {/* Session Path Input */}
        <div>
          <label
            htmlFor="sessionPath"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Session File Name
          </label>
          <input
            id="sessionPath"
            type="text"
            value={sessionPath}
            onChange={(e) => setSessionPath(e.target.value)}
            placeholder="notion_session.json"
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
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
              <p className="text-sm text-red-800 dark:text-red-200">{error}</p>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
        >
          Start Capture
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
                setSiteUrl(example.siteUrl);
                setLoginUrl(example.loginUrl);
                setSessionPath(example.sessionPath);
              }}
              className="w-full text-left px-4 py-3 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors text-sm"
            >
              <span className="text-gray-900 dark:text-white font-medium">
                {example.task}
              </span>
              <span className="text-gray-500 dark:text-gray-400 ml-2">
                → {example.siteUrl}
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
