"use client";

import Image from "next/image";
import { WorkflowDisplay } from "@/types";

interface WorkflowViewerProps {
  workflow: WorkflowDisplay;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function WorkflowViewer({ workflow }: WorkflowViewerProps) {
  // Parse explanation into steps (split by numbered list)
  const explanationSteps = workflow.explanation
    .split(/\d+\)/)
    .filter((step) => step.trim().length > 0)
    .map((step) => step.trim());

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Workflow Captured ✅
            </h2>
            <p className="text-gray-600 dark:text-gray-400">{workflow.task}</p>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-green-100 dark:bg-green-900 rounded-lg">
            <svg
              className="w-5 h-5 text-green-600 dark:text-green-400"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            <span className="text-sm font-medium text-green-600 dark:text-green-400">
              Completed
            </span>
          </div>
        </div>

        <div className="flex items-center gap-6 text-sm text-gray-500 dark:text-gray-400">
          <div className="flex items-center gap-2">
            <svg
              className="w-4 h-4"
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
            <span>{workflow.paths.length} visual steps</span>
          </div>
        </div>
      </div>

      {/* Explanation Section */}
      <div className="mb-8 p-6 bg-blue-50 dark:bg-blue-900/20 rounded-xl border border-blue-200 dark:border-blue-800">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <svg
            className="w-5 h-5 text-blue-600 dark:text-blue-400"
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
          How to Complete This Workflow
        </h3>
        <ol className="space-y-3">
          {explanationSteps.map((step, index) => (
            <li
              key={index}
              className="flex gap-3 text-gray-700 dark:text-gray-300"
            >
              <span className="flex-shrink-0 w-6 h-6 bg-blue-600 dark:bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-semibold">
                {index + 1}
              </span>
              <span className="flex-1">{step}</span>
            </li>
          ))}
        </ol>
      </div>

      {/* Screenshots Timeline */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
          Visual Steps
        </h3>
        <div className="space-y-6">
          {workflow.paths.map((screenshotPath, index) => (
            <div key={index} className="relative">
              {/* Timeline connector */}
              {index < workflow.paths.length - 1 && (
                <div className="absolute left-6 top-16 bottom-0 w-0.5 bg-gradient-to-b from-blue-200 to-transparent dark:from-blue-800" />
              )}

              <div className="flex gap-6">
                {/* Step number badge */}
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white font-bold shadow-lg">
                    {index + 1}
                  </div>
                </div>

                {/* Screenshot */}
                <div className="flex-1">
                  <div className="bg-gray-50 dark:bg-gray-700 rounded-xl p-4">
                    {explanationSteps[index] && (
                      <p className="text-gray-900 dark:text-white font-medium mb-4">
                        {explanationSteps[index]}
                      </p>
                    )}
                    <div className="relative rounded-lg overflow-hidden border-2 border-gray-200 dark:border-gray-600 shadow-md hover:shadow-xl transition-shadow">
                      <Image
                        src={`${API_URL}/${screenshotPath}`}
                        alt={`Step ${index + 1}`}
                        width={1920}
                        height={1080}
                        className="w-full h-auto"
                        unoptimized
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700 text-center">
        <p className="text-gray-600 dark:text-gray-400">
          Task ID:{" "}
          <code className="text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
            {workflow.task_id}
          </code>
        </p>
      </div>
    </div>
  );
}
