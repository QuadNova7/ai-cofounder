'use client';

import React, { useState } from 'react';
import { submitHumanReview } from '../services/api';
import { HumanReviewPayload } from '../types/venture';
import { AlertTriangle, CheckCircle, RefreshCw, XOctagon, Loader2 } from 'lucide-react';

interface HitlReviewBannerProps {
  ventureId: string;
  warnings?: string[];
  criticNotes?: string;
  onReviewSubmitted: () => void;
}

export const HitlReviewBanner: React.FC<HitlReviewBannerProps> = ({
  ventureId,
  warnings = [],
  criticNotes,
  onReviewSubmitted,
}) => {
  const [notes, setNotes] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAction = async (action: HumanReviewPayload['action']) => {
    setIsSubmitting(true);
    setError(null);
    try {
      await submitHumanReview(ventureId, {
        action,
        notes: notes.trim() || undefined,
      });
      onReviewSubmitted();
    } catch (err: any) {
      setError(err.message || 'Failed to submit review action');
      setIsSubmitting(false);
    }
  };

  return (
    <div className="hitl-banner">
      <div className="hitl-header">
        <AlertTriangle size={20} />
        <span>Founder Decision Required (Human-in-the-Loop Interrupt)</span>
      </div>

      <p className="hitl-desc">
        The multi-agent validation engine paused the pipeline because an agent flagged a critical issue requiring founder discretion.
      </p>

      {criticNotes && (
        <div
          style={{
            background: 'rgba(0,0,0,0.25)',
            borderLeft: '3px solid #fbbf24',
            padding: '10px 14px',
            borderRadius: '4px',
            marginBottom: '12px',
            fontSize: '0.88rem',
            color: '#fef3c7',
          }}
        >
          <strong>Agent Feedback: </strong>
          {criticNotes}
        </div>
      )}

      {warnings.length > 0 && (
        <ul style={{ paddingLeft: '20px', marginBottom: '16px', fontSize: '0.85rem', color: '#fcd34d' }}>
          {warnings.map((w, idx) => (
            <li key={idx} style={{ marginBottom: '4px' }}>{w}</li>
          ))}
        </ul>
      )}

      {error && (
        <div style={{ color: 'var(--danger)', fontSize: '0.85rem', marginBottom: '12px' }}>
          {error}
        </div>
      )}

      <div style={{ marginBottom: '16px' }}>
        <input
          type="text"
          className="form-input"
          style={{ fontSize: '0.88rem', padding: '8px 12px' }}
          placeholder="Optional founder rationale or parameter override instructions..."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          disabled={isSubmitting}
        />
      </div>

      <div className="hitl-actions">
        <button
          type="button"
          className="btn-proceed"
          onClick={() => handleAction('PROCEED_ANYWAY')}
          disabled={isSubmitting}
        >
          {isSubmitting ? <Loader2 size={14} className="spin" /> : <CheckCircle size={14} />}
          <span>Proceed Anyway</span>
        </button>

        <button
          type="button"
          className="btn-override"
          onClick={() => handleAction('OVERRIDE_ASSUMPTIONS')}
          disabled={isSubmitting}
        >
          {isSubmitting ? <Loader2 size={14} className="spin" /> : <RefreshCw size={14} />}
          <span>Override Assumptions</span>
        </button>

        <button
          type="button"
          className="btn-abort"
          onClick={() => handleAction('ABORT')}
          disabled={isSubmitting}
        >
          {isSubmitting ? <Loader2 size={14} className="spin" /> : <XOctagon size={14} />}
          <span>Abort Pipeline</span>
        </button>
      </div>
    </div>
  );
};
