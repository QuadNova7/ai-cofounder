'use client';

import React from 'react';
import { MarketingPlanOutput, StartupRoadmap } from '../../types/venture';
import { Rocket, Target, CheckSquare, Calendar, PieChart, Award } from 'lucide-react';

interface Props {
  marketingData?: MarketingPlanOutput | null;
  roadmapData?: StartupRoadmap | null;
}

export const MarketingRoadmapView: React.FC<Props> = ({ marketingData, roadmapData }) => {
  if (!marketingData && !roadmapData) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">🚀</div>
        <h4>No data received from agent</h4>
        <p>90-Day GTM Marketing Plan & Executive Roadmap output is pending or has not yet been compiled.</p>
      </div>
    );
  }

  return (
    <div>
      {/* Executive Summary (if compiled) */}
      {roadmapData && roadmapData.executive_summary && (
        <div
          style={{
            background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(168, 85, 247, 0.08) 100%)',
            border: '1px solid var(--border-highlight)',
            borderRadius: 'var(--radius-md)',
            padding: '20px',
            marginBottom: '24px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 700, fontSize: '1.05rem', color: '#818cf8' }}>
              <Award size={20} />
              <span>Executive Advisory Summary</span>
            </div>
            {roadmapData.overall_confidence_score && (
              <span className="status-badge completed">
                Overall Score: {Math.round(roadmapData.overall_confidence_score * 100)}%
              </span>
            )}
          </div>
          <p style={{ color: 'var(--text-primary)', fontSize: '0.94rem', lineHeight: 1.6 }}>
            {roadmapData.executive_summary}
          </p>
        </div>
      )}

      {/* Positioning Statement */}
      {marketingData && marketingData.positioning_statement && (
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
              lineHeight: 1.5,
            }}
          >
            {marketingData.positioning_statement}
          </div>
        </div>
      )}

      {/* Priority Acquisition Channels */}
      {marketingData && marketingData.priority_channels && marketingData.priority_channels.length > 0 && (
        <div className="content-section">
          <div className="section-title">
            <Rocket size={18} color="#10b981" />
            <span>High-Priority Customer Acquisition Channels</span>
          </div>
          <div className="tag-list">
            {marketingData.priority_channels.map((ch, idx) => (
              <span key={idx} className="tag" style={{ border: '1px solid rgba(16, 185, 129, 0.3)' }}>
                {ch}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* 90-Day GTM Milestones Timeline */}
      {marketingData && marketingData.gtm_90_day_plan && marketingData.gtm_90_day_plan.length > 0 && (
        <div className="content-section" style={{ marginTop: '24px' }}>
          <div className="section-title">
            <Calendar size={18} color="#38bdf8" />
            <span>90-Day Execution Roadmap (Month-by-Month)</span>
          </div>

          <div className="milestones-list">
            {marketingData.gtm_90_day_plan.map((m, idx) => (
              <div key={idx} className="milestone-item">
                <div className="milestone-month-badge">Month {m.month}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                    <h5 style={{ fontSize: '1rem', color: 'var(--text-primary)' }}>{m.focus}</h5>
                    <span style={{ fontSize: '0.78rem', color: '#10b981', fontWeight: 600 }}>
                      KPI: {m.target_kpi}
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
      {marketingData && marketingData.prioritized_next_actions && marketingData.prioritized_next_actions.length > 0 && (
        <div className="content-section" style={{ marginTop: '24px' }}>
          <div className="section-title">
            <CheckSquare size={18} color="#f59e0b" />
            <span>Prioritized Founder Next Actions (Day 1 - 14)</span>
          </div>
          <ul style={{ paddingLeft: '20px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            {marketingData.prioritized_next_actions.map((act, idx) => (
              <li key={idx} style={{ marginBottom: '6px' }}>
                {act}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Budget Allocation */}
      {marketingData && marketingData.budget_allocation && Object.keys(marketingData.budget_allocation).length > 0 && (
        <div className="content-section" style={{ marginTop: '24px' }}>
          <div className="section-title">
            <PieChart size={18} color="#a855f7" />
            <span>Marketing Budget Allocation</span>
          </div>
          <div className="tag-list">
            {Object.entries(marketingData.budget_allocation).map(([channel, amount], idx) => (
              <span key={idx} className="tag">
                <strong>{channel}:</strong> ${amount}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Advisory Disclaimer */}
      {roadmapData && (
        <div style={{ marginTop: '30px', borderTop: '1px solid var(--border-subtle)', paddingTop: '14px', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
          {roadmapData.disclaimer}
        </div>
      )}
    </div>
  );
};
