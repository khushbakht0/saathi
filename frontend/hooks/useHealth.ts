"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { ApiError, apiClient, type HealthResponse } from "@/lib/api";

export interface HealthStatusState {
  status: "loading" | "connected" | "offline";
  responseTimeMs: number | null;
  version: string | null;
  errorMessage: string | null;
}

const INITIAL_STATE: HealthStatusState = {
  status: "loading",
  responseTimeMs: null,
  version: null,
  errorMessage: null,
};

export function useHealth() {
  const [state, setState] = useState<HealthStatusState>(INITIAL_STATE);
  const retryCountRef = useRef(0);

  const checkHealth = useCallback(async () => {
    const startedAt = performance.now();

    setState((currentState) => ({
      ...currentState,
      status: "loading",
      errorMessage: null,
    }));

    try {
      const response = await apiClient.get<HealthResponse>("/health");
      const responseTimeMs = Math.round(performance.now() - startedAt);

      setState({
        status: "connected",
        responseTimeMs,
        version: response.version ?? null,
        errorMessage: null,
      });

      retryCountRef.current = 0;
    } catch (error) {
      const nextAttempt = retryCountRef.current + 1;
      const nextDelayMs = Math.min(1000 * 2 ** retryCountRef.current, 5000);

      retryCountRef.current = nextAttempt;

      setState({
        status: "offline",
        responseTimeMs: Math.round(performance.now() - startedAt),
        version: null,
        errorMessage: error instanceof ApiError ? error.message : "Unknown backend error.",
      });

      if (nextAttempt < 4) {
        window.setTimeout(() => {
          void checkHealth();
        }, nextDelayMs);
      }
    }
  }, []);

  useEffect(() => {
    void checkHealth();
  }, [checkHealth]);

  return useMemo(
    () => ({
      ...state,
      retry: () => {
        retryCountRef.current = 0;
        void checkHealth();
      },
    }),
    [checkHealth, state],
  );
}
