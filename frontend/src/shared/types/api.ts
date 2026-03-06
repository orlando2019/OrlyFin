export interface ErrorResponse {
  code: string;
  message: string;
  details: Array<Record<string, unknown>>;
  trace_id: string;
  timestamp: string;
}
