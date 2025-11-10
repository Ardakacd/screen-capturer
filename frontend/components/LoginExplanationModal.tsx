"use client";

import { useEffect, useState } from "react";

interface LoginExplanationModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function LoginExplanationModal({
  isOpen,
  onClose,
}: LoginExplanationModalProps) {
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <div
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
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
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                How Login Works
              </h2>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Why Login is Needed */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
              <span className="text-2xl">🔐</span>
              Why Login is Needed
            </h3>
            <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
              Most web applications require authentication to access their
              features. Since the AI agent needs to interact with your account
              (e.g., invite teammates, create projects), it needs to be logged
              in.
            </p>
          </div>

          {/* How It Works */}
          <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-5 border border-blue-200 dark:border-blue-800">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <span className="text-2xl">⚡</span>
              How It Works - One-Time Setup
            </h3>
            <div className="space-y-4">
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  1
                </div>
                <div>
                  <p className="font-medium text-gray-900 dark:text-white">
                    Enter Login URL and click Start Capture
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    Playwright will automatically open a browser window and
                    navigate to the login page. You have 60 seconds to login
                    with your credentials.
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  2
                </div>
                <div>
                  <p className="font-medium text-gray-900 dark:text-white">
                    Session is saved automatically
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    Your login session (cookies) is saved in a file. This allows
                    the AI to reuse your login without needing your password.
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  3
                </div>
                <div>
                  <p className="font-medium text-gray-900 dark:text-white">
                    Everything else is automatic
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    From the second task onwards, the AI automatically logs in,
                    finds the correct URL, and executes the workflow - no manual
                    steps needed!
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* What Each Field Does */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
              <span className="text-2xl">📝</span>
              What Each Field Does
            </h3>
            <div className="space-y-3">
              <div className="border-l-4 border-purple-500 pl-4">
                <p className="font-medium text-gray-900 dark:text-white">
                  Login URL (Optional)
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  The login page of the application (e.g.,
                  https://www.notion.so/login). When you click Start Capture,
                  Playwright will automatically open a browser and navigate
                  here. You then have 60 seconds to login. Only needed for the{" "}
                  <strong>first task</strong>.
                </p>
              </div>

              <div className="border-l-4 border-green-500 pl-4">
                <p className="font-medium text-gray-900 dark:text-white">
                  Session File Name
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Where to store your login session (e.g., notion_session.json).
                  Use different files for different apps to keep sessions
                  separate.
                </p>
              </div>
            </div>
          </div>

          {/* Privacy & Security */}
          <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-5 border border-green-200 dark:border-green-800">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
              <span className="text-2xl">🔒</span>
              Your Credentials Stay Private
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              <strong>Important:</strong> You <strong>never</strong> give your
              username or password to the AI. You login manually, and only the
              session cookies (which expire) are saved. Your actual credentials
              remain completely private and secure.
            </p>
          </div>

          {/* Quick Tip */}
          <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-4 border border-yellow-200 dark:border-yellow-800">
            <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-1 flex items-center gap-2">
              💡 Quick Tip
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              If you&apos;re trying a new application for the first time,
              provide the Login URL. For subsequent tasks on the same app, just
              use the same Session File Name and skip the Login URL!
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 rounded-b-2xl">
          <button
            onClick={onClose}
            className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
          >
            Got it!
          </button>
        </div>
      </div>
    </div>
  );
}
