'use client';

import React from 'react';
import { WorkflowStage } from '../types/venture';
import {
  Lightbulb,
  Search,
  Scale,
  LayoutGrid,
  TrendingUp,
  Rocket,
  CheckCircle2,
  AlertTriangle,
  Loader2,
  Radio,
} from 'lucide-react';

interface AgentProgressProps {
  currentStage: WorkflowStage;
  progressPct: number;
  statusMessage: string;
  isStreamConnected: boolean;
  humanReviewRequired?: boolean;
}

interface StageStep {
  id: WorkflowStage;
  label: string;
  shortLabel: string;
  icon: React.ReactNode;
}

const STAGES: StageStep[] = [
  { id: 'IDEA_ANALYSIS', label: 'Idea Analysis', shortLabel: 'Idea', icon: <Lightbulb size={16} /> },
  { id: 'MARKET_RESEARCH', label: 'Market Research', shortLabel: 'Market', icon: <Search size={16} /> },
  { id: 'CRITIC_VALIDATION', label: 'Critic Validation', shortLabel: 'Critic', icon: <Scale size={16} /> },
  { id: 'BUSINESS_MODEL', label: 'Business Model', shortLabel: 'Canvas', icon: <LayoutGrid size={16} /> },
  { id: 'REVENUE_ESTIMATION', label: 'Financial Engine', shortLabel: 'Finance', icon: <TrendingUp size={16} /> },
  { id: 'MARKETING', label: '90-Day GTM', shortLabel: 'Marketing', icon: <Rocket size={16} /> },
  { id: 'ROADMAP_COMPILATION', label: 'Roadmap Ready', shortLabel: 'Complete', icon: <CheckCircle2 size={16} /> },
];

const STAGE_ORDER: Record<WorkflowStage, number> = {
  INITIALIZED: 0,
  IDEA_ANALYSIS: 1,
  MARKET_RESEARCH: 2,
  CRITIC_VALIDATION: 3,
  REPLANNING: 3,
  BUSINESS_MODEL: 4,
  REVENUE_ESTIMATION: 5,
  MARKETING: 6,
  ROADMAP_COMPILATION: 7,
  COMPLETED: 8,
  FAILED: -1,
};

export const AgentProgress: React.FC<AgentProgressProps> = ({
  currentStage,
  progressPct,
  statusMessage,
  isStreamConnected,
  humanReviewRequired = false,
}) => {
  const currentIdx = STAGE_ORDER[currentStage] ?? 0;
  const isFailed = currentStage === 'FAILED';
  const isCompleted = currentStage === 'COMPLETED';

  return (
    <div className="progress-container">
      <div className="progress-header">
        <div className="progress-title-wrap">
          <h3 style={{ fontSize: '1.15rem', fontWeight: 700 }}>Multi-Agent Execution Pipeline</h3>
          {isFailed ? (
            <span className="status-badge failed">
              <AlertTriangle size={13} />
              <span>Failed</span>
            </span>
          ) : isCompleted ? (
            <span className="status-badge completed">
              <CheckCircle2 size={13} />
              <span>Completed</span>
            </span>
          ) : humanReviewRequired ? (
            <span className="status-badge review">
              <AlertTriangle size={13} />
              <span>Review Required</span>
            </span>
          ) : (
            <span className="status-badge running">
              <Loader2 size={13} className="spin" />
              <span>Running</span>
            </span>
          )}

          {isStreamConnected && (
            <span
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '5px',
                fontSize: '0.75rem',
                color: 'var(--success)',
                fontWeight: 500,
              }}
            >
              <Radio size={12} />
              <span>Live SSE</span>
            </span>
          )}
        </div>

        <div className="percentage-badge">{Math.min(100, Math.max(0, progressPct))}%</div>
      </div>

      {/* Progress Bar */}
      <div className="progress-bar-track">
        <div
          className="progress-bar-fill"
          style={{
            width: `${Math.min(100, Math.max(0, progressPct))}%`,
            background: isFailed
              ? 'var(--danger)'
              : humanReviewRequired
              ? 'var(--warning)'
              : undefined,
          }}
        />
      </div>

      {/* Horizontal Stage Stepper */}
      <div className="stepper-row">
        {STAGES.map((step, idx) => {
          const stepOrderIdx = idx + 1;
          const isStepCompleted = isCompleted || currentIdx > stepOrderIdx;
          const isStepActive = !isCompleted && currentIdx === stepOrderIdx;
          const isStepFlagged = isStepActive && humanReviewRequired;

          let stepClass = 'step-node';
          if (isStepCompleted) stepClass += ' completed';
          else if (isStepFlagged) stepClass += ' flagged';
          else if (isStepActive) stepClass += ' active';

          return (
            <div key={step.id} className={stepClass}>
              <div className="step-icon-circle">
                {isStepCompleted ? (
                  <CheckCircle2 size={18} />
                ) : isStepFlagged ? (
                  <AlertTriangle size={18} />
                ) : isStepActive ? (
                  <Loader2 size={18} className="spin" />
                ) : (
                  step.icon
                )}
              </div>
              <span className="step-label">{step.shortLabel}</span>
            </div>
          );
        })}
      </div>

      {/* Live SSE Activity Ticker */}
      <div className="activity-ticker">
        <div className="pulsing-dot" />
        <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>Live Agent Activity:</span>
        <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {statusMessage || 'Awaiting next agent cycle...'}
        </span>
      </div>
    </div>
  );
};
