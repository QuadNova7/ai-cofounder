'use client';

import React from 'react';
import { MarketingPlanOutput } from '../../types/venture';
import { Megaphone, Target, Rocket, MessageSquare, CheckSquare, PieChart, Calendar } from 'lucide-react';

interface Props {
  data?: MarketingPlanOutput | null;
}

export const MarketingPlanView: React.FC<Props> = ({ data }) => {
  if (!data) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📣</div>
        <h4>No data received from agent</h4>
        <p>Marketing Plan Agent output is pending or has not yet been generated.</p>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}>
        <Megaphone size={20} color="#6366f1" />
        <h4 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Marketing & GTM Strategy Plan</h4>
      </div>

      {/* Positioning Statement */}
      {data.positioning_statement && (
        <div className="content-section">
          <div className="section-title">
            <Target size={18} color="#6366f1" />
            <span>Market Positioning Statement</span>
          </div>
          <div
            style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-md)',
              padding: '16px',
              fontSize: '0.95rem',
              color: 'var(--text-primary)',
              lineHeight: 1.6,
            }}
          >
            {data.positioning_statement}
          </div>
        </div>
      )}

      {/* Messaging Framework */}
      {data.messaging_framework && Object.keys(data.messaging_framework).length > 0 && (
        <div className="content-section" style={{ marginTop: '20px' }}>
          <div className="section-title">
            <MessageSquare size={18} color="#818cf8" />
            <span>Core Messaging Framework</span>
          </div>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
              gap: '12px',
            }}
          >
            {Object.entries(data.messaging_framework).map(([key, value], idx) => (
              <div
                key={idx}
                style={{
                  background: 'var(--bg-surface)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  padding: '14px',
                }}
              >
                <div
                  style={{
                    fontSize: '0.75rem',
                    textTransform: 'uppercase',
                    color: 'var(--text-muted)',
                    fontWeight: 700,
                    marginBottom: '4px',
                  }}
                >
                  {key.replace(/_/g, ' ')}
                </div>
                <div style={{ fontSize: '0.9rem', color: 'var(--text-primary)', lineHeight: 1.4 }}>
                  {value}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Priority Acquisition Channels */}
      {data.priority_channels && data.priority_channels.length > 0 && (
        <div className="content-section" style={{ marginTop: '20px' }}>
          <div className="section-title">
            <Rocket size={18} color="#10b981" />
            <span>High-Priority Acquisition Channels</span>
          </div>
          <div className="tag-list">
            {data.priority_channels.map((ch, idx) => (
              <span
                key={idx}
                className="tag"
                style={{
                  background: 'rgba(16, 185, 129, 0.1)',
                  borderColor: 'rgba(16, 185, 129, 0.3)',
                  color: '#6ee7b7',
                }}
              >
                {ch}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Acquisition Tactics */}
      {data.acquisition_tactics && data.acquisition_tactics.length > 0 && (
        <div className="content-section" style={{ marginTop: '20px' }}>
          <div className="section-title">
            <span>Growth & Customer Acquisition Tactics</span>
          </div>
          <ul style={{ paddingLeft: '20px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            {data.acquisition_tactics.map((tactic, idx) => (
              <li key={idx} style={{ marginBottom: '6px' }}>
                {tactic}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 90-Day Execution Plan */}
      {data.gtm_90_day_plan && data.gtm_90_day_plan.length > 0 && (
        <div className="content-section" style={{ marginTop: '24px' }}>
          <div className="section-title">
            <Calendar size={18} color="#38bdf8" />
            <span>90-Day GTM Action Plan</span>
          </div>
          <div className="milestones-list">
            {data.gtm_90_day_plan.map((m, idx) => (
              <div key={idx} className="milestone-item">
                <div className="milestone-month-badge">Month {m.month}</div>
                <div style={{ flex: 1 }}>
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      marginBottom: '6px',
                    }}
                  >
                    <h5 style={{ fontSize: '1rem', color: 'var(--text-primary)' }}>{m.focus}</h5>
                    <span style={{ fontSize: '0.78rem', color: '#10b981', fontWeight: 600 }}>
                      Target KPI: {m.target_kpi}
                    </span>
                  </div>
                  {m.deliverables && m.deliverables.length > 0 && (
                    <ul style={{ paddingLeft: '18px', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                      {m.deliverables.map((deliv, dIdx) => (
                        <li key={dIdx} style={{ marginBottom: '4px' }}>
                          {deliv}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Prioritized Next Actions */}
      {data.prioritized_next_actions && data.prioritized_next_actions.length > 0 && (
        <div className="content-section" style={{ marginTop: '24px' }}>
          <div className="section-title">
            <CheckSquare size={18} color="#f59e0b" />
            <span>Immediate Founder Next Actions (Day 1 - 14)</span>
          </div>
          <ul style={{ paddingLeft: '20px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            {data.prioritized_next_actions.map((act, idx) => (
              <li key={idx} style={{ marginBottom: '6px' }}>
                {act}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Budget Allocation */}
      {data.budget_allocation && Object.keys(data.budget_allocation).length > 0 && (
        <div className="content-section" style={{ marginTop: '24px' }}>
          <div className="section-title">
            <PieChart size={18} color="#a855f7" />
            <span>Marketing Budget Allocation</span>
          </div>
          <div className="tag-list">
            {Object.entries(data.budget_allocation).map(([channel, amount], idx) => (
              <span key={idx} className="tag">
                <strong>{channel}:</strong> ${amount}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
