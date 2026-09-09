'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { VentureState, WorkflowStage, SSEEventEnvelope } from '../types/venture';
import { getVentureState, getVentureStreamUrl } from '../services/api';

export interface UseAgentStreamReturn {
  venture: VentureState | null;
  currentStage: WorkflowStage;
  progressPct: number;
  statusMessage: string;
  events: SSEEventEnvelope[];
  isLoading: boolean;
  error: string | null;
  isStreamConnected: boolean;
  refreshState: () => Promise<void>;
}

export const useAgentStream = (ventureId: string): UseAgentStreamReturn => {
  const [venture, setVenture] = useState<VentureState | null>(null);
  const [currentStage, setCurrentStage] = useState<WorkflowStage>('INITIALIZED');
  const [progressPct, setProgressPct] = useState<number>(0);
  const [statusMessage, setStatusMessage] = useState<string>('Connecting to multi-agent orchestrator...');
  const [events, setEvents] = useState<SSEEventEnvelope[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isStreamConnected, setIsStreamConnected] = useState<boolean>(false);

  const eventSourceRef = useRef<EventSource | null>(null);

  const refreshState = useCallback(async () => {
    if (!ventureId) return;
    try {
      const state = await getVentureState(ventureId);
      setVenture(state);
      if (state.current_stage) {
        setCurrentStage(state.current_stage);
      }
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to refresh venture state');
    }
  }, [ventureId]);

  useEffect(() => {
    if (!ventureId) return;

    let isMounted = true;

    // 1. Initial State Hydration
    setIsLoading(true);
    getVentureState(ventureId)
      .then((state) => {
        if (!isMounted) return;
        setVenture(state);
        setCurrentStage(state.current_stage || 'INITIALIZED');
        if (state.current_stage === 'COMPLETED') {
          setProgressPct(100);
          setStatusMessage('Startup Roadmap compilation completed.');
        } else if (state.current_stage === 'FAILED') {
          setStatusMessage('Pipeline stopped or failed.');
        } else {
          setStatusMessage('Hydrated existing state. Awaiting live updates...');
        }
        setIsLoading(false);
      })
      .catch((err) => {
        if (!isMounted) return;
        setError(err.message || 'Could not load venture state');
        setIsLoading(false);
      });

    // 2. Connect to Server-Sent Events (SSE)
    const streamUrl = getVentureStreamUrl(ventureId);
    const es = new EventSource(streamUrl);
    eventSourceRef.current = es;

    es.onopen = () => {
      if (!isMounted) return;
      setIsStreamConnected(true);
      setError(null);
    };

    es.onmessage = (event) => {
      if (!isMounted) return;
      try {
        const payload: SSEEventEnvelope = JSON.parse(event.data);
        if (payload.stage) {
          setCurrentStage(payload.stage);
        }
        if (typeof payload.progress_pct === 'number') {
          setProgressPct(payload.progress_pct);
        }
        if (payload.message) {
          setStatusMessage(payload.message);
        }

        setEvents((prev) => [...prev.slice(-49), payload]);

        // When stages complete or when HITL is triggered, refresh state to pull output cards
        if (
          payload.event_type === 'STAGE_COMPLETED' ||
          payload.event_type === 'ROADMAP_READY' ||
          payload.event_type === 'HITL_REQUIRED' ||
          payload.stage === 'COMPLETED'
        ) {
          refreshState();
        }
      } catch (e) {
        // Fallback for non-JSON SSE lines
        setStatusMessage(event.data);
      }
    };

    es.onerror = () => {
      if (!isMounted) return;
      setIsStreamConnected(false);
      // Don't flag error if pipeline is already completed
      if (currentStage !== 'COMPLETED') {
        // Try refreshing state once on disconnect to catch any final update
        refreshState();
      }
    };

    return () => {
      isMounted = false;
      es.close();
      eventSourceRef.current = null;
    };
  }, [ventureId, refreshState, currentStage]);

  return {
    venture,
    currentStage,
    progressPct,
    statusMessage,
    events,
    isLoading,
    error,
    isStreamConnected,
    refreshState,
  };
};
