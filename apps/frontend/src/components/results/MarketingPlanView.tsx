'use client';

import React from 'react';
import { MarketingPlanOutput } from '../../types/venture';
import {
  Megaphone,
  Target,
  Rocket,
  MessageSquare,
  CheckSquare,
  DollarSign,
  Calendar,
  Layers,
  Clock,
  TrendingUp,
  AlertCircle
} from 'lucide-react';

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

  const totalBudget = data.budget_allocation
    ? Object.values(data.budget_allocation).reduce((acc, val) => acc + val, 0)
    : 0;

  const ltvCacRatio =
    data.estimated_ltv && data.target_cac && data.target_cac > 0
      ? (data.estimated_ltv / data.target_cac).toFixed(1)
      : '3.0';

  return (
    <div>
      {/* Header with Archetype Badge */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '12px',
          marginBottom: '20px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Megaphone size={22} color="#6366f1" />
          <h4 style={{ fontSize: '1.2rem', fontWeight: 700, margin: 0 }}>Marketing & GTM Strategy Plan</h4>
        </div>
        {data.venture_archetype && (
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '4px 12px',
              borderRadius: '9999px',
              background: 'rgba(99, 102, 241, 0.12)',
              border: '1px solid rgba(99, 102, 241, 0.3)',
              color: '#818cf8',
              fontSize: '0.82rem',
              fontWeight: 600,
            }}
          >
            <Layers size={14} />
            <span>{data.venture_archetype}</span>
          </div>
        )}
      </div>

      {/* Warnings / Feedback Banner if present */}
      {data.warnings && data.warnings.length > 0 && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            padding: '10px 14px',
            marginBottom: '20px',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(245, 158, 11, 0.1)',
            border: '1px solid rgba(245, 158, 11, 0.3)',
            color: '#fbbf24',
            fontSize: '0.85rem',
          }}
        >
          <AlertCircle size={16} />
          <span>{data.warnings.join(' ')}</span>
        </div>
      )}

      {/* Unit Economics KPI Strip */}
      {(data.target_cac !== undefined || data.estimated_ltv !== undefined) && (
        <div className="content-section" style={{ marginBottom: '20px' }}>
          <div className="section-title">
            <TrendingUp size={18} color="#10b981" />
            <span>Deterministic Unit Economics & CAC Guardrails</span>
          </div>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
              gap: '12px',
            }}
          >
            {/* Target CAC */}
            <div
              style={{
                background: 'var(--bg-surface)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '14px',
              }}
            >
              <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700 }}>
                Target CAC Ceiling
              </div>
              <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#10b981', margin: '4px 0' }}>
                ${data.target_cac ? data.target_cac.toLocaleString() : '—'}
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                Max acquisition cost to sustain 3:1 ratio
              </div>
            </div>

            {/* Estimated LTV */}
            <div
              style={{
                background: 'var(--bg-surface)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '14px',
              }}
            >
              <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700 }}>
                Estimated LTV
              </div>
              <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#38bdf8', margin: '4px 0' }}>
                ${data.estimated_ltv ? data.estimated_ltv.toLocaleString() : '—'}
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                Derived from monthly price & churn rate
              </div>
            </div>

            {/* Payback Period */}
            <div
              style={{
                background: 'var(--bg-surface)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '14px',
              }}
            >
              <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700 }}>
                CAC Payback
              </div>
              <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#a855f7', margin: '4px 0' }}>
                {data.cac_payback_months ? `${data.cac_payback_months} mo` : '—'}
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                Capital recovery time (Target &le; 12 mo)
              </div>
            </div>

            {/* LTV:CAC Ratio */}
            <div
              style={{
                background: 'var(--bg-surface)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '14px',
              }}
            >
              <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700 }}>
                LTV : CAC Ratio
              </div>
              <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#f59e0b', margin: '4px 0' }}>
                {ltvCacRatio}:1
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                Healthy venture benchmark &ge; 3.0
              </div>
            </div>
          </div>
        </div>
      )}

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

      {/* Priority Acquisition Channels (Bullseye Inner Circle) */}
      {data.priority_channels && data.priority_channels.length > 0 && (
        <div className="content-section" style={{ marginTop: '20px' }}>
          <div className="section-title">
            <Rocket size={18} color="#10b981" />
            <span>High-Priority Traction Channels (Bullseye Inner Circle)</span>
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
                  padding: '6px 12px',
                  fontSize: '0.88rem',
                }}
              >
                #{idx + 1} {ch}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Budget Allocation (Absolute Dollars) */}
      {data.budget_allocation && Object.keys(data.budget_allocation).length > 0 && (
        <div className="content-section" style={{ marginTop: '24px' }}>
          <div className="section-title">
            <DollarSign size={18} color="#a855f7" />
            <span>Marketing Budget Distribution (Total: ${totalBudget.toLocaleString()})</span>
          </div>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
              gap: '12px',
            }}
          >
            {Object.entries(data.budget_allocation).map(([channel, amount], idx) => (
              <div
                key={idx}
                style={{
                  background: 'var(--bg-surface)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  padding: '14px',
                }}
              >
                <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, marginBottom: '4px' }}>
                  {channel}
                </div>
                <div style={{ fontSize: '1.25rem', fontWeight: 800, color: amount > 0 ? '#10b981' : 'var(--text-secondary)' }}>
                  ${amount.toLocaleString()}
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                  {amount === 0 ? 'Sweat-Equity (0-CAC Organic)' : `${totalBudget > 0 ? ((amount / totalBudget) * 100).toFixed(0) : 0}% of budget`}
                </div>
              </div>
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

      {/* Immediate Founder Next Actions (Day 1 - 14) */}
      {data.prioritized_next_actions && data.prioritized_next_actions.length > 0 && (
        <div className="content-section" style={{ marginTop: '24px' }}>
          <div className="section-title">
            <CheckSquare size={18} color="#f59e0b" />
            <span>Immediate Founder Next Actions (Day 1 – 14)</span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {data.prioritized_next_actions.map((act, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '10px',
                  background: 'var(--bg-surface)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '10px 14px',
                  fontSize: '0.9rem',
                  color: 'var(--text-primary)',
                }}
              >
                <span
                  style={{
                    background: 'rgba(245, 158, 11, 0.15)',
                    color: '#fbbf24',
                    borderRadius: '4px',
                    padding: '2px 6px',
                    fontSize: '0.75rem',
                    fontWeight: 700,
                    whiteSpace: 'nowrap',
                  }}
                >
                  Step {idx + 1}
                </span>
                <span>{act}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 90-Day (12-Week) Execution Roadmap */}
      {data.gtm_90_day_plan && data.gtm_90_day_plan.length > 0 && (
        <div className="content-section" style={{ marginTop: '24px' }}>
          <div className="section-title">
            <Calendar size={18} color="#38bdf8" />
            <span>90-Day GTM Sprint Execution Schedule (12 Weekly Sprints)</span>
          </div>
          <div className="milestones-list">
            {data.gtm_90_day_plan.map((m, idx) => (
              <div key={idx} className="milestone-item">
                <div
                  className="milestone-month-badge"
                  style={{ minWidth: '90px', textAlign: 'center' }}
                >
                  {m.week ? `Week ${m.week}` : `Week ${idx + 1}`}
                  <div style={{ fontSize: '0.7rem', opacity: 0.8 }}>Month {m.month}</div>
                </div>
                <div style={{ flex: 1 }}>
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      flexWrap: 'wrap',
                      gap: '8px',
                      marginBottom: '6px',
                    }}
                  >
                    <h5 style={{ fontSize: '0.98rem', fontWeight: 600, color: 'var(--text-primary)', margin: 0 }}>
                      {m.focus}
                    </h5>
                    <span
                      style={{
                        fontSize: '0.78rem',
                        color: '#10b981',
                        fontWeight: 600,
                        background: 'rgba(16, 185, 129, 0.1)',
                        padding: '2px 8px',
                        borderRadius: '4px',
                      }}
                    >
                      Target KPI: {m.target_kpi}
                    </span>
                  </div>
                  {m.deliverables && m.deliverables.length > 0 && (
                    <ul style={{ paddingLeft: '18px', fontSize: '0.85rem', color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                      {m.deliverables.map((deliv, dIdx) => (
                        <li key={dIdx} style={{ marginBottom: '3px' }}>
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
    </div>
  );
};
