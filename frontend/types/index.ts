// Backend API Types (matching backend/models/)
export interface StartTaskRequest {
  site_url: string;
  login_url?: string;
  session_path: string;
  task: string;
  task_id: string;
}

export interface StartTaskResponse {
  paths: string[];
  explanation: string;
}

// Frontend UI Types
export interface WorkflowResult {
  task_id: string;
  task: string;
  site_url: string;
  screenshot_paths: string[];
  explanation: string;
  total_steps: number;
}
