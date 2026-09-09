'use client';

import React from 'react';
import { IdeaAnalysisOutput } from '../../types/venture';
import { Lightbulb, AlertCircle, Users, Target, ShieldCheck } from 'lucide-react';

interface Props {
  data?: IdeaAnalysisOutput | null;
}

export const IdeaAnalysisView: React.FC<Props> = ({ data }) => {
  if (!data) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">💡</div>
        <h4>No data received from agent</h4>
        <p>Idea Analysis output is pending or has not yet been submitted by the orchestrator.</p>
      </div>
    );
  }

  const formatScore = (val: number) => `${Math.round(val * 100)}%`;

  return (
    <div>
      {/* Scores Grid */}
      <div className="scores-grid">
        <div className="score-box">
          <div className="score-label">Clarity Score</div>
          <div className="score-value" style={{ color: '#818cf8' }}>
            {formatScore(data.clarity_score ?? 0)}
          </div>
        </div>
        <div className="score-box">
          <div className="score-label">Feasibility Score</div>
          <div className="score-value" style={{ color: '#34d399' }}>
            {formatScore(data.feasibility_score ?? 0)}
          </div>
        </div>
        <div className="score-box">
          <div className="score-label">Confidence Score</div>
          <div className="score-value" style={{ color: '#38bdf8' }}>
            {formatScore(data.confidence_score ?? 0)}
          </div>
        </div>
      </div>

      {/* Refined Value Proposition */}
      <div className="content-section">
        <div className="section-title">
          <Target size={18} color="#6366f1" />
          <span>Refined Value Proposition</span>
        </div>
        <div
          style={{
            background: 'var(--bg-surface)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            padding: '16px',
            fontSize: '1rem',
            color: 'var(--text-primary)',
            lineHeight: 1.6,
          }}
        >
          {data.refined_value_proposition || 'None specified.'}
        </div>
      </div>

      {/* Problem Statement */}
      <div className="content-section">
        <div className="section-title">
          <Lightbulb size={18} color="#f59e0b" />
          <span>Problem Statement</span>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', lineHeight: 1.6 }}>
          {data.problem_statement || 'None specified.'}
        </p>
      </div>

      {/* Target Users */}
      {data.target_users && data.target_users.length > 0 && (
        <div className="content-section">
          <div className="section-title">
            <Users size={18} color="#10b981" />
            <span>Target User Segments</span>
          </div>
          <div className="tag-list">
            {data.target_users.map((user, idx) => (
              <span key={idx} className="tag">
                {user}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Key Assumptions */}
      {data.key_assumptions && data.key_assumptions.length > 0 && (
        <div className="content-section">
          <div className="section-title">
            <ShieldCheck size={18} color="#38bdf8" />
            <span>Key Assumptions to Validate</span>
          </div>
          <ul style={{ paddingLeft: '20px', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            {data.key_assumptions.map((item, idx) => (
              <li key={idx} style={{ marginBottom: '6px' }}>
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Red Flags */}
      {data.red_flags && data.red_flags.length > 0 && (
        <div className="content-section">
          <div className="section-title" style={{ color: '#f87171' }}>
            <AlertCircle size={18} color="#ef4444" />
            <span>Identified Red Flags & Blindspots</span>
          </div>
          <div className="tag-list">
            {data.red_flags.map((flag, idx) => (
              <span key={idx} className="tag red-flag">
                {flag}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
