'use client';

import React from 'react';
import { BusinessModelOutput } from '../../types/venture';
import { LayoutGrid, AlertTriangle, ShieldCheck } from 'lucide-react';

interface Props {
  data?: BusinessModelOutput | null;
}

export const BusinessModelView: React.FC<Props> = ({ data }) => {
  if (!data || !data.canvas) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📊</div>
        <h4>No data received from agent</h4>
        <p>Business Model Canvas synthesis is pending or has not yet been generated.</p>
      </div>
    );
  }

  const { canvas } = data;

  const renderList = (items?: string[]) => {
    if (!items || items.length === 0) {
      return <li style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>None listed</li>;
    }
    return items.map((item, idx) => <li key={idx}>{item}</li>);
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <LayoutGrid size={20} color="#6366f1" />
          <h4 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
            {data.framework_used || 'Business Model Canvas'}
          </h4>
        </div>
        {typeof data.confidence_score === 'number' && (
          <span className="status-badge running" style={{ background: 'rgba(99, 102, 241, 0.12)' }}>
            Confidence: {Math.round(data.confidence_score * 100)}%
          </span>
        )}
      </div>

      {/* 9-Box Canvas Grid */}
      <div className="bmc-grid">
        {/* Row 1 */}
        <div className="bmc-box tall">
          <h5>1. Key Partners</h5>
          <ul>{renderList(canvas.key_partners)}</ul>
        </div>

        <div className="bmc-box">
          <h5>2. Key Activities</h5>
          <ul>{renderList(canvas.key_activities)}</ul>
        </div>

        <div className="bmc-box tall">
          <h5>4. Value Propositions</h5>
          <ul>{renderList(canvas.value_propositions)}</ul>
        </div>

        <div className="bmc-box">
          <h5>5. Customer Relationships</h5>
          <ul>{renderList(canvas.customer_relationships)}</ul>
        </div>

        <div className="bmc-box tall">
          <h5>7. Customer Segments</h5>
          <ul>{renderList(canvas.customer_segments)}</ul>
        </div>

        {/* Row 2 (under activities and relationships) */}
        <div className="bmc-box">
          <h5>3. Key Resources</h5>
          <ul>{renderList(canvas.key_resources)}</ul>
        </div>

        <div className="bmc-box">
          <h5>6. Channels</h5>
          <ul>{renderList(canvas.channels)}</ul>
        </div>

        {/* Row 3: Bottom Costs & Revenues */}
        <div className="bmc-box wide" style={{ gridColumn: 'span 2' }}>
          <h5>8. Cost Structure</h5>
          <ul>{renderList(canvas.cost_structure)}</ul>
        </div>

        <div className="bmc-box wide" style={{ gridColumn: 'span 3' }}>
          <h5>9. Revenue Streams</h5>
          <ul>{renderList(canvas.revenue_streams)}</ul>
        </div>
      </div>

      {/* Key Risks & Mitigations */}
      {((data.key_risks && data.key_risks.length > 0) || (data.mitigations && data.mitigations.length > 0)) && (
        <div style={{ marginTop: '28px' }} className="form-grid-2">
          <div className="content-section">
            <div className="section-title" style={{ color: '#f87171' }}>
              <AlertTriangle size={18} color="#ef4444" />
              <span>Key Business Risks</span>
            </div>
            <ul style={{ paddingLeft: '20px', fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
              {data.key_risks?.map((risk, idx) => (
                <li key={idx} style={{ marginBottom: '6px' }}>
                  {risk}
                </li>
              ))}
            </ul>
          </div>

          <div className="content-section">
            <div className="section-title" style={{ color: '#34d399' }}>
              <ShieldCheck size={18} color="#10b981" />
              <span>Proposed Mitigations</span>
            </div>
            <ul style={{ paddingLeft: '20px', fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
              {data.mitigations?.map((mit, idx) => (
                <li key={idx} style={{ marginBottom: '6px' }}>
                  {mit}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};
