// Backend API Types (matching backend/models/)
export interface StartTaskRequest {
  login_url?: string;
  session_path: string;
  task: string;
  task_id: string;
}

export interface StartTaskResponse {
  paths: string[];
  explanation: string;
}

// Frontend display type - extends backend response with client metadata
export interface WorkflowDisplay extends StartTaskResponse {
  task_id: string;
  task: string;
}
