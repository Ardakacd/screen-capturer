"use client";

import { useState } from "react";
import WorkflowCapture from "@/components/WorkflowCapture";
import WorkflowViewer from "@/components/WorkflowViewer";
import { WorkflowResult } from "@/types";

export default function Home() {
  const [currentWorkflow, setCurrentWorkflow] = useState<WorkflowResult | null>(
    null
  );
  const [isCapturing, setIsCapturing] = useState(false);

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="mb-12 text-center">
          <div className="inline-flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg">
              <svg
                className="w-7 h-7 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                />
              </svg>
            </div>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
              Agent B
            </h1>
          </div>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            AI-driven workflow capture system that autonomously navigates web
            apps and creates visual guides
          </p>
        </header>

        {/* Main Content */}
        <div className="max-w-7xl mx-auto">
          {/* Workflow Capture Form */}
          <div className="mb-8">
            <WorkflowCapture
              onWorkflowCaptured={(workflow) => {
                setCurrentWorkflow(workflow);
                setIsCapturing(false);
              }}
              onCapturingChange={setIsCapturing}
            />
          </div>

          {/* Workflow Display */}
          {isCapturing && (
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
              <div className="inline-flex items-center gap-3 text-blue-600 dark:text-blue-400">
                <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                <span className="text-lg font-medium">
                  Capturing workflow...
                </span>
              </div>
              <p className="mt-4 text-gray-600 dark:text-gray-400">
                Agent B is navigating the application and capturing each step
              </p>
            </div>
          )}

          {currentWorkflow && !isCapturing && (
            <WorkflowViewer workflow={currentWorkflow} />
          )}

          {/* Info Cards */}
          {!currentWorkflow && !isCapturing && (
            <div className="grid md:grid-cols-3 gap-6 mt-12">
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mb-4">
                  <svg
                    className="w-6 h-6 text-blue-600 dark:text-blue-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 10V3L4 14h7v7l9-11h-7z"
                    />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Autonomous Navigation
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  AI agents navigate any web app in real-time, capturing each UI
                  state automatically
                </p>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center mb-4">
                  <svg
                    className="w-6 h-6 text-purple-600 dark:text-purple-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Visual Documentation
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Screenshots and descriptions for every step, including modals
                  and dynamic states
                </p>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
                <div className="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center mb-4">
                  <svg
                    className="w-6 h-6 text-green-600 dark:text-green-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                    />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Natural Language
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Just describe what you want to learn - works with any web
                  application
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
