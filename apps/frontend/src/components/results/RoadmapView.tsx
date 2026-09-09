'use client';

import React from 'react';
import { StartupRoadmap } from '../../types/venture';
import { Award, Compass, CheckCircle2, ShieldAlert, TrendingUp, Rocket, FileText } from 'lucide-react';

interface Props {
  data?: StartupRoadmap | null;
}

export const RoadmapView: React.FC<Props> = ({ data }) => {
  if (!data) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">🏁</div>
        <h4>No data received from agent</h4>
        <p>The Final Executive Roadmap has not yet been compiled by the orchestrator.</p>
      </div>
    );
  }

  return (
    <div>
      {/* Executive Summary Card */}
      <div
        style={{
          background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.14) 0%, rgba(168, 85, 247, 0.08) 100%)',
          border: '1px solid var(--border-highlight)',
          borderRadius: 'var(--radius-lg)',
          padding: '24px',
          marginBottom: '24px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Award size={22} color="#818cf8" />
            <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-primary)' }}>
              Executive Advisory Roadmap
            </h3>
          </div>
          {typeof data.overall_confidence_score === 'number' && (
            <span className="status-badge completed">
              Overall Viability: {Math.round(data.overall_confidence_score * 100)}%
            </span>
          )}
        </div>

        <p style={{ color: 'var(--text-primary)', fontSize: '0.98rem', lineHeight: 1.65 }}>
          {data.executive_summary}
        </p>
      </div>

      {/* Synthesis Snapshot Across All Agents */}
      <div className="content-section">
        <div className="section-title">
          <FileText size={18} color="#6366f1" />
          <span>Strategic Synthesis Snapshot</span>
        </div>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: '16px',
            marginTop: '12px',
          }}
        >
          {data.idea_analysis && (
            <div className="feature-card" style={{ padding: '18px' }}>
              <div style={{ fontSize: '0.8rem', color: '#818cf8', fontWeight: 700, textTransform: 'uppercase', marginBottom: '6px' }}>
                1. Core Value Proposition
              </div>
              <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                {data.idea_analysis.refined_value_proposition}
              </p>
            </div>
          )}

          {data.market_research && (
            <div className="feature-card" style={{ padding: '18px' }}>
              <div style={{ fontSize: '0.8rem', color: '#34d399', fontWeight: 700, textTransform: 'uppercase', marginBottom: '6px' }}>
                2. Market Landscape
              </div>
              <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                {data.market_research.competitor_landscape?.length || 0} competitors analyzed. Top trends:{' '}
                {data.market_research.market_trends?.slice(0, 2).join(', ') || 'Emerging market sector.'}
              </p>
            </div>
          )}

          {data.revenue_estimation && (
            <div className="feature-card" style={{ padding: '18px' }}>
              <div style={{ fontSize: '0.8rem', color: '#f59e0b', fontWeight: 700, textTransform: 'uppercase', marginBottom: '6px' }}>
                3. Financial Trajectory
              </div>
              <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                Pricing: {data.revenue_estimation.pricing_strategy}. Moderate Yr 1 MRR:{' '}
                ${Math.round(data.revenue_estimation.scenarios?.[1]?.month_12_revenue || data.revenue_estimation.scenarios?.[0]?.month_12_revenue || 0).toLocaleString()}
              </p>
            </div>
          )}

          {data.marketing_plan && (
            <div className="feature-card" style={{ padding: '18px' }}>
              <div style={{ fontSize: '0.8rem', color: '#ec4899', fontWeight: 700, textTransform: 'uppercase', marginBottom: '6px' }}>
                4. Primary GTM Channels
              </div>
              <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                {data.marketing_plan.priority_channels?.join(', ') || 'Direct founder outreach & organic search.'}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Advisory Disclaimer */}
      <div
        style={{
          marginTop: '32px',
          borderTop: '1px solid var(--border-subtle)',
          paddingTop: '16px',
          fontSize: '0.8rem',
          color: 'var(--text-muted)',
          lineHeight: 1.5,
        }}
      >
        <span style={{ fontWeight: 600 }}>Notice: </span>
        {data.disclaimer ||
          'This document is an AI-generated decision-support roadmap and does not constitute formal legal, tax, or investment advice.'}
      </div>
    </div>
  );
};
