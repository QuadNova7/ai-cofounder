'use client';

import React from 'react';
import Link from 'next/link';
import { useAgentStream } from '../../../hooks/useAgentStream';
import { AgentProgress } from '../../../components/AgentProgress';
import { HitlReviewBanner } from '../../../components/HitlReviewBanner';
import { AgentResultsView } from '../../../components/AgentResultsView';
import { ArrowLeft, RefreshCw, AlertCircle, Sparkles, MapPin, DollarSign } from 'lucide-react';

export default function StartupMissionControl({ params }: { params: { startupId: string } }) {
  const {
    venture,
    currentStage,
    progressPct,
    statusMessage,
    isStreamConnected,
    refreshState,
    isLoading,
    error,
  } = useAgentStream(params.startupId);

  return (
    <div>
      {/* Top Breadcrumb & Action Bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '20px',
        }}
      >
        <Link
          href="/"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '0.88rem',
            color: 'var(--text-secondary)',
          }}
        >
          <ArrowLeft size={16} />
          <span>Back to Home</span>
        </Link>

        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <button
            type="button"
            onClick={() => refreshState()}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              background: 'var(--bg-surface-elevated)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--text-secondary)',
              padding: '6px 14px',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.82rem',
              cursor: 'pointer',
            }}
          >
            <RefreshCw size={13} />
            <span>Refresh State</span>
          </button>

          {currentStage !== 'COMPLETED' && currentStage !== 'FAILED' && (
            <button
              type="button"
              onClick={async () => {
                if (window.confirm('Are you sure you want to stop the multi-agent analysis pipeline?')) {
                  try {
                    const { submitHumanReview } = await import('../../../services/api');
                    await submitHumanReview(params.startupId, {
                      action: 'ABORT',
                      notes: 'Pipeline stopped manually by founder.',
                    });
                    refreshState();
                  } catch (err: any) {
                    alert(err.message || 'Failed to stop pipeline');
                  }
                }
              }}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                background: 'rgba(239, 68, 68, 0.12)',
                border: '1px solid rgba(239, 68, 68, 0.35)',
                color: '#fca5a5',
                padding: '6px 14px',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.82rem',
                cursor: 'pointer',
                fontWeight: 600,
              }}
            >
              <span style={{ display: 'inline-block', width: '8px', height: '8px', background: '#ef4444', borderRadius: '50%' }} />
              <span>Stop Process</span>
            </button>
          )}
        </div>
      </div>

      {/* Error Callout */}
      {error && (
        <div
          style={{
            background: 'var(--danger-bg)',
            border: '1px solid rgba(239, 68, 68, 0.4)',
            color: '#fca5a5',
            padding: '14px 18px',
            borderRadius: 'var(--radius-md)',
            marginBottom: '20px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            fontSize: '0.9rem',
          }}
        >
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Venture Header Context */}
      <div
        style={{
          background: 'var(--bg-card)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-lg)',
          padding: '20px 24px',
          marginBottom: '24px',
          backdropFilter: 'blur(12px)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <span
            style={{
              fontFamily: 'monospace',
              fontSize: '0.8rem',
              color: 'var(--accent-primary)',
              background: 'rgba(99, 102, 241, 0.1)',
              padding: '2px 8px',
              borderRadius: '4px',
              border: '1px solid rgba(99, 102, 241, 0.25)',
            }}
          >
            Venture ID: {params.startupId}
          </span>
        </div>

        <h2 style={{ fontSize: '1.4rem', fontWeight: 800, marginBottom: '8px', color: 'var(--text-primary)' }}>
          {venture?.founder_input?.startup_idea || 'Analyzing Venture...'}
        </h2>

        {venture?.founder_input && (
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            <div>
              <strong>Target Market: </strong>
              <span>{venture.founder_input.target_market}</span>
            </div>
            {venture.founder_input.target_geography && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                <MapPin size={13} color="#38bdf8" />
                <span>{venture.founder_input.target_geography}</span>
              </div>
            )}
            {venture.founder_input.budget !== undefined && venture.founder_input.budget > 0 && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                <DollarSign size={13} color="#10b981" />
                <span>Budget: ${venture.founder_input.budget.toLocaleString()}</span>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 1. Multi-Agent Progress Tracking */}
      <AgentProgress
        currentStage={currentStage}
        progressPct={progressPct}
        statusMessage={statusMessage}
        isStreamConnected={isStreamConnected}
        humanReviewRequired={venture?.human_review_required}
      />

      {/* 2. Human-In-The-Loop Review Alert (if flagged) */}
      {venture?.human_review_required && (
        <HitlReviewBanner
          ventureId={params.startupId}
          warnings={venture.warnings}
          criticNotes={venture.human_review_notes || venture.market_validation?.feedback_notes}
          onReviewSubmitted={() => refreshState()}
        />
      )}

      {/* 3. Tabbed Results Display */}
      <AgentResultsView venture={venture} currentStage={currentStage} />
    </div>
  );
}
