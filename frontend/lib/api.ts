const DEFAULT_TIMEOUT_MS = 5000;

export interface HealthResponse {
  status: string;
  version?: string;
}

export interface ApiClientOptions extends RequestInit {
  timeoutMs?: number;
}

export class ApiError extends Error {
  readonly statusCode?: number;

  constructor(message: string, statusCode?: number) {
    super(message);
    this.name = "ApiError";
    this.statusCode = statusCode;
  }
}

function getApiBaseUrl(): string {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  if (!apiUrl) {
    throw new Error("NEXT_PUBLIC_API_URL must be defined in the environment.");
  }

  return apiUrl.replace(/\/$/, "");
}

function buildUrl(path: string): string {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${getApiBaseUrl()}${normalizedPath}`;
}

async function parseJsonResponse<T>(response: Response): Promise<T> {
  const contentType = response.headers.get("content-type") ?? "";

  if (!contentType.includes("application/json")) {
    throw new ApiError("Unexpected response format from backend.", response.status);
  }

  return (await response.json()) as T;
}

export class ApiClient {
  async get<T>(path: string, options: ApiClientOptions = {}): Promise<T> {
    const { timeoutMs = DEFAULT_TIMEOUT_MS, headers, ...rest } = options;
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);

    try {
      const response = await fetch(buildUrl(path), {
        ...rest,
        headers: {
          Accept: "application/json",
          ...(headers ?? {}),
        },
        signal: controller.signal,
      });

      if (!response.ok) {
        const payload = await parseJsonResponse<{ message?: string }>(response).catch(() => undefined);
        throw new ApiError(payload?.message ?? "Request failed.", response.status);
      }

      return await parseJsonResponse<T>(response);
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        throw new ApiError("Request timed out.");
      }

      if (error instanceof ApiError) {
        throw error;
      }

      throw new ApiError("Network request failed.");
    } finally {
      window.clearTimeout(timeoutId);
    }
  }
}

export const apiClient = new ApiClient();
