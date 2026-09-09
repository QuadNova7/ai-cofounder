'use client';

import React from 'react';
import { MarketResearchOutput, CriticValidationOutput } from '../../types/venture';
import { Search, ShieldAlert, CheckCircle, ExternalLink, TrendingUp, AlertTriangle } from 'lucide-react';

interface Props {
  marketData?: MarketResearchOutput | null;
  criticData?: CriticValidationOutput | null;
}

export const MarketResearchView: React.FC<Props> = ({ marketData, criticData }) => {
  if (!marketData && !criticData) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">🔍</div>
        <h4>No data received from agent</h4>
        <p>Market Research & Critic validation output is pending or has not yet been generated.</p>
      </div>
    );
  }

  const formatCurrency = (val?: number) => {
    if (val === undefined || val === null) return 'N/A';
    if (val >= 1_000_000_000) return `$${(val / 1_000_000_000).toFixed(1)}B`;
    if (val >= 1_000_000) return `$${(val / 1_000_000).toFixed(1)}M`;
    if (val >= 1_000) return `$${(val / 1_000).toFixed(0)}K`;
    return `$${val}`;
  };

  return (
    <div>
      {/* Critic Validation Callout */}
      {criticData && (
        <div
          style={{
            background: criticData.requires_pivot ? 'var(--danger-bg)' : 'var(--success-bg)',
            border: `1px solid ${criticData.requires_pivot ? 'rgba(239, 68, 68, 0.4)' : 'rgba(16, 185, 129, 0.4)'}`,
            borderRadius: 'var(--radius-md)',
            padding: '16px',
            marginBottom: '24px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 700 }}>
              {criticData.requires_pivot ? (
                <ShieldAlert size={18} color="#ef4444" />
              ) : (
                <CheckCircle size={18} color="#10b981" />
              )}
              <span style={{ color: criticData.requires_pivot ? '#fca5a5' : '#6ee7b7' }}>
                Critic Validation Status: {criticData.status || 'EVALUATED'}
              </span>
            </div>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
              {criticData.verified_sources_count} Sources Verified
            </span>
          </div>

          {criticData.feedback_notes && (
            <p style={{ fontSize: '0.9rem', color: 'var(--text-primary)', lineHeight: 1.5 }}>
              {criticData.feedback_notes}
            </p>
          )}

          {criticData.unsupported_claims && criticData.unsupported_claims.length > 0 && (
            <div style={{ marginTop: '12px' }}>
              <div style={{ fontSize: '0.8rem', fontWeight: 600, color: '#f87171', marginBottom: '4px' }}>
                Unsupported Claims Flagged by Critic:
              </div>
              <ul style={{ paddingLeft: '20px', fontSize: '0.85rem', color: '#fca5a5' }}>
                {criticData.unsupported_claims.map((claim, idx) => (
                  <li key={idx}>{claim}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Market Sizing (TAM / SAM / SOM) */}
      {marketData && (marketData.tam_estimate || marketData.sam_estimate || marketData.som_estimate) && (
        <div className="scores-grid">
          <div className="score-box">
            <div className="score-label">TAM (Total Addressable)</div>
            <div className="score-value" style={{ color: '#818cf8' }}>
              {formatCurrency(marketData.tam_estimate)}
            </div>
          </div>
          <div className="score-box">
            <div className="score-label">SAM (Serviceable)</div>
            <div className="score-value" style={{ color: '#38bdf8' }}>
              {formatCurrency(marketData.sam_estimate)}
            </div>
          </div>
          <div className="score-box">
            <div className="score-label">SOM (Serviceable Obtainable)</div>
            <div className="score-value" style={{ color: '#34d399' }}>
              {formatCurrency(marketData.som_estimate)}
            </div>
          </div>
        </div>
      )}

      {/* Competitor Landscape */}
      {marketData && marketData.competitor_landscape && marketData.competitor_landscape.length > 0 && (
        <div className="content-section">
          <div className="section-title">
            <Search size={18} color="#6366f1" />
            <span>Direct & Indirect Competitor Landscape</span>
          </div>
          <div className="competitors-grid">
            {marketData.competitor_landscape.map((comp, idx) => (
              <div key={idx} className="competitor-card">
                <div className="competitor-header">
                  <h5>{comp.name}</h5>
                  {comp.pricing_model && (
                    <span className="tag" style={{ fontSize: '0.75rem' }}>
                      {comp.pricing_model}
                    </span>
                  )}
                </div>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '12px', lineHeight: 1.5 }}>
                  {comp.description}
                </p>
                {comp.strengths && comp.strengths.length > 0 && (
                  <div style={{ marginBottom: '8px' }}>
                    <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#34d399' }}>Strengths: </span>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                      {comp.strengths.join(', ')}
                    </span>
                  </div>
                )}
                {comp.weaknesses && comp.weaknesses.length > 0 && (
                  <div style={{ marginBottom: '8px' }}>
                    <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#f87171' }}>Weaknesses: </span>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                      {comp.weaknesses.join(', ')}
                    </span>
                  </div>
                )}
                {comp.website_url && (
                  <a
                    href={comp.website_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '4px',
                      fontSize: '0.78rem',
                      color: '#818cf8',
                      marginTop: '4px',
                    }}
                  >
                    <span>Visit website</span>
                    <ExternalLink size={12} />
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Market Trends */}
      {marketData && marketData.market_trends && marketData.market_trends.length > 0 && (
        <div className="content-section">
          <div className="section-title">
            <TrendingUp size={18} color="#10b981" />
            <span>Key Market Trends & Tailwinds</span>
          </div>
          <div className="tag-list">
            {marketData.market_trends.map((trend, idx) => (
              <span key={idx} className="tag">
                {trend}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Entry Barriers */}
      {marketData && marketData.entry_barriers && marketData.entry_barriers.length > 0 && (
        <div className="content-section">
          <div className="section-title">
            <AlertTriangle size={18} color="#f59e0b" />
            <span>Market Entry Barriers</span>
          </div>
          <ul style={{ paddingLeft: '20px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            {marketData.entry_barriers.map((barrier, idx) => (
              <li key={idx} style={{ marginBottom: '4px' }}>
                {barrier}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Citations & Source URLs */}
      {marketData && marketData.source_urls && marketData.source_urls.length > 0 && (
        <div className="content-section">
          <div className="section-title">
            <ExternalLink size={18} color="#38bdf8" />
            <span>Evidence & Research Sources</span>
          </div>
          <ul style={{ paddingLeft: '20px', fontSize: '0.85rem' }}>
            {marketData.source_urls.map((url, idx) => (
              <li key={idx} style={{ marginBottom: '4px' }}>
                <a
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: '#818cf8', textDecoration: 'underline' }}
                >
                  {url}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
