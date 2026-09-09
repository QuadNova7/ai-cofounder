'use client';

import React, { useState } from 'react';
import { RevenueEstimationOutput } from '../../types/venture';
import { TrendingUp, DollarSign, Calendar, Users, CheckCircle } from 'lucide-react';

interface Props {
  data?: RevenueEstimationOutput | null;
}

export const RevenueProjectionsView: React.FC<Props> = ({ data }) => {
  const [selectedScenarioIdx, setSelectedScenarioIdx] = useState(0);

  if (!data) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📈</div>
        <h4>No data received from agent</h4>
        <p>Revenue & deterministic financial modeling output is pending or has not yet been generated.</p>
      </div>
    );
  }

  const { parameters, scenarios, pricing_strategy, assumptions_summary } = data;
  const activeScenario = scenarios && scenarios[selectedScenarioIdx] ? scenarios[selectedScenarioIdx] : null;

  return (
    <div>
      {/* Pricing Strategy */}
      <div
        style={{
          background: 'var(--bg-surface)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-md)',
          padding: '16px',
          marginBottom: '20px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
          <DollarSign size={18} color="#10b981" />
          <h4 style={{ fontSize: '1rem', fontWeight: 700 }}>Pricing & Monetization Strategy</h4>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', lineHeight: 1.5 }}>
          {pricing_strategy || 'Subscription / transactional pricing'}
        </p>
      </div>

      {/* Financial Parameters */}
      {parameters && (
        <div className="scores-grid">
          <div className="score-box">
            <div className="score-label">Unit / Monthly Price</div>
            <div className="score-value" style={{ color: '#10b981' }}>
              ${parameters.monthly_price ?? 0}
            </div>
          </div>
          <div className="score-box">
            <div className="score-label">Starting Customers</div>
            <div className="score-value" style={{ color: '#818cf8' }}>
              {parameters.starting_customers ?? 0}
            </div>
          </div>
          <div className="score-box">
            <div className="score-label">Monthly Growth</div>
            <div className="score-value" style={{ color: '#38bdf8' }}>
              {Math.round((parameters.monthly_growth_rate ?? 0) * 100)}%
            </div>
          </div>
          <div className="score-box">
            <div className="score-label">Monthly Churn</div>
            <div className="score-value" style={{ color: '#f87171' }}>
              {Math.round((parameters.monthly_churn_rate ?? 0) * 100)}%
            </div>
          </div>
          <div className="score-box">
            <div className="score-label">Fixed Monthly Costs</div>
            <div className="score-value" style={{ color: '#f59e0b' }}>
              ${parameters.fixed_monthly_costs ?? 0}
            </div>
          </div>
        </div>
      )}

      {/* Scenarios Header & Selector */}
      {scenarios && scenarios.length > 0 && (
        <div className="content-section" style={{ marginTop: '24px' }}>
          <div className="section-title">
            <TrendingUp size={18} color="#6366f1" />
            <span>Deterministic Projection Scenarios</span>
          </div>

          <div className="scenarios-grid">
            {scenarios.map((sc, idx) => {
              const isSelected = idx === selectedScenarioIdx;
              return (
                <div
                  key={idx}
                  className={`scenario-card ${isSelected ? 'moderate' : ''}`}
                  onClick={() => setSelectedScenarioIdx(idx)}
                  style={{
                    cursor: 'pointer',
                    borderColor: isSelected ? 'var(--accent-primary)' : undefined,
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                    <h5 style={{ textTransform: 'capitalize', fontSize: '1rem', color: isSelected ? '#818cf8' : 'var(--text-primary)' }}>
                      {sc.scenario_name}
                    </h5>
                    {isSelected && <CheckCircle size={16} color="#6366f1" />}
                  </div>
                  <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#10b981', marginBottom: '4px' }}>
                    ${Math.round(sc.month_12_revenue).toLocaleString()}
                    <span style={{ fontSize: '0.75rem', fontWeight: 500, color: 'var(--text-muted)' }}> /mo (Yr 1)</span>
                  </div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', gap: '12px' }}>
                    <span><Users size={13} style={{ display: 'inline', marginRight: '4px' }} />{sc.month_12_customers} Users</span>
                    <span><Calendar size={13} style={{ display: 'inline', marginRight: '4px' }} />Break-even: {sc.break_even_month ? `Mo ${sc.break_even_month}` : 'N/A'}</span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Monthly Table for Active Scenario */}
          {activeScenario && activeScenario.monthly_projections && activeScenario.monthly_projections.length > 0 && (
            <div style={{ marginTop: '20px', overflowX: 'auto' }}>
              <h5 style={{ fontSize: '0.9rem', marginBottom: '10px', color: 'var(--text-secondary)' }}>
                Monthly Trajectory ({activeScenario.scenario_name.toUpperCase()} SCENARIO)
              </h5>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
                <thead>
                  <tr style={{ background: 'var(--bg-surface-elevated)', borderBottom: '1px solid var(--border-subtle)', textAlign: 'left' }}>
                    <th style={{ padding: '8px 12px' }}>Month</th>
                    <th style={{ padding: '8px 12px' }}>Active Customers</th>
                    <th style={{ padding: '8px 12px' }}>Revenue</th>
                    <th style={{ padding: '8px 12px' }}>Net Profit / Burn</th>
                  </tr>
                </thead>
                <tbody>
                  {activeScenario.monthly_projections.map((row: any, idx: number) => (
                    <tr key={idx} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                      <td style={{ padding: '8px 12px' }}>Month {row.month || idx + 1}</td>
                      <td style={{ padding: '8px 12px' }}>{row.customers || row.users || '—'}</td>
                      <td style={{ padding: '8px 12px', color: '#34d399' }}>
                        {row.revenue ? `$${Math.round(row.revenue).toLocaleString()}` : '—'}
                      </td>
                      <td
                        style={{
                          padding: '8px 12px',
                          color: (row.net_profit ?? row.profit ?? 0) >= 0 ? '#10b981' : '#f87171',
                        }}
                      >
                        {row.net_profit !== undefined ? `$${Math.round(row.net_profit).toLocaleString()}` : '—'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Assumptions Summary */}
      {assumptions_summary && assumptions_summary.length > 0 && (
        <div className="content-section" style={{ marginTop: '24px' }}>
          <div className="section-title">
            <span>Model Invariants & Assumptions</span>
          </div>
          <ul style={{ paddingLeft: '20px', fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
            {assumptions_summary.map((assump, idx) => (
              <li key={idx} style={{ marginBottom: '4px' }}>
                {assump}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
