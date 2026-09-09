'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { startVenture } from '../services/api';
import { FounderInput } from '../types/venture';
import { Sparkles, ChevronDown, ChevronUp, ArrowRight, Loader2, Wand2 } from 'lucide-react';

export const StartupForm: React.FC = () => {
  const router = useRouter();

  const [idea, setIdea] = useState('');
  const [market, setMarket] = useState('');
  const [geography, setGeography] = useState('Global');
  const [budget, setBudget] = useState<number | ''>(0);
  const [timeline, setTimeline] = useState<number>(3);
  const [goals, setGoals] = useState('');
  const [constraintsText, setConstraintsText] = useState('');
  const [skillsResources, setSkillsResources] = useState('');

  const [showAdvanced, setShowAdvanced] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadSamplePreset = () => {
    setIdea('On-demand laundry pickup and scheduled delivery subscription service for university hostel students with app tracking and 24-hour turnaround.');
    setMarket('University undergraduate & postgraduate hostel students and campus young professionals');
    setGeography('Colombo, Sri Lanka');
    setBudget(150000);
    setTimeline(3);
    setGoals('Onboard 300 active subscribers across 3 campus clusters within 60 days.');
    setConstraintsText('Limited upfront capital for commercial washers, reliance on local dry-cleaner partnerships, fuel cost volatility.');
    setSkillsResources('Operations team of 2 students, access to electric cargo scooter, mobile web development experience.');
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!idea.trim() || !market.trim()) {
      setError('Please provide both your startup idea and target market.');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    const payload: FounderInput = {
      startup_idea: idea.trim(),
      target_market: market.trim(),
      target_geography: geography.trim() || 'Global',
      budget: typeof budget === 'number' ? budget : 0,
      timeline_months: timeline || 3,
      goals: goals.trim(),
      constraints: constraintsText
        ? constraintsText.split(',').map((c) => c.trim()).filter(Boolean)
        : [],
      skills_resources: skillsResources.trim() || undefined,
    };

    try {
      const res = await startVenture(payload);
      router.push(`/startup/${res.venture_id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to start multi-agent analysis pipeline.');
      setIsSubmitting(false);
    }
  };

  return (
    <div className="form-card">
      <div className="form-header">
        <h2>Launch Startup Venture Analysis</h2>
        <p>
          Enter your raw startup concept. Our autonomous multi-agent co-founder system will analyze
          market viability, validate assumptions, synthesize a business model, estimate deterministic financials, and build your 90-day GTM roadmap.
        </p>
      </div>

      <div className="preset-bar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.88rem', color: '#94a3b8' }}>
          <Wand2 size={16} color="#6366f1" />
          <span>Need a quick starting example?</span>
        </div>
        <button type="button" onClick={loadSamplePreset} className="preset-btn">
          Load Sample Idea
        </button>
      </div>

      {error && (
        <div
          style={{
            background: 'var(--danger-bg)',
            border: '1px solid rgba(239, 68, 68, 0.4)',
            color: '#fca5a5',
            padding: '12px 16px',
            borderRadius: 'var(--radius-md)',
            marginBottom: '20px',
            fontSize: '0.9rem',
          }}
        >
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">
            Startup Idea Concept <span className="req">*</span>
          </label>
          <textarea
            className="form-textarea"
            rows={4}
            placeholder="e.g. An AI-powered virtual co-founder that helps first-time founders stress-test market ideas and build 90-day execution roadmaps..."
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">
            Target Market / Audience <span className="req">*</span>
          </label>
          <input
            type="text"
            className="form-input"
            placeholder="e.g. Solo entrepreneurs, university student builders, pre-seed startup founders"
            value={market}
            onChange={(e) => setMarket(e.target.value)}
            required
          />
        </div>

        <button
          type="button"
          className="advanced-toggle"
          onClick={() => setShowAdvanced(!showAdvanced)}
        >
          {showAdvanced ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          <span>{showAdvanced ? 'Hide Optional Details' : 'Add Financials, Timeline & Constraints (Optional)'}</span>
        </button>

        {showAdvanced && (
          <div style={{ padding: '16px 0', borderTop: '1px solid var(--border-subtle)', marginBottom: '16px' }}>
            <div className="form-grid-2">
              <div className="form-group">
                <label className="form-label">Target Geography</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g. Global, North America, Sri Lanka"
                  value={geography}
                  onChange={(e) => setGeography(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Starting Budget ($ or LKR)</label>
                <input
                  type="number"
                  className="form-input"
                  placeholder="e.g. 5000"
                  value={budget}
                  onChange={(e) => setBudget(e.target.value === '' ? '' : Number(e.target.value))}
                />
              </div>
            </div>

            <div className="form-grid-2">
              <div className="form-group">
                <label className="form-label">Execution Timeline (Months)</label>
                <input
                  type="number"
                  className="form-input"
                  min={1}
                  max={24}
                  value={timeline}
                  onChange={(e) => setTimeline(Number(e.target.value))}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Core Milestone Goals</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g. Launch MVP within 30 days, achieve $2k MRR"
                  value={goals}
                  onChange={(e) => setGoals(e.target.value)}
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Specific Constraints (comma-separated)</label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. No full-time engineers, strictly organic marketing, regulatory compliance"
                value={constraintsText}
                onChange={(e) => setConstraintsText(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Founder Skills & Resources Available</label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. Domain expertise in B2B sales, full-stack Next.js developer"
                value={skillsResources}
                onChange={(e) => setSkillsResources(e.target.value)}
              />
            </div>
          </div>
        )}

        <button type="submit" className="submit-btn" disabled={isSubmitting}>
          {isSubmitting ? (
            <>
              <Loader2 size={18} className="spin" />
              <span>Initializing Multi-Agent Pipeline...</span>
            </>
          ) : (
            <>
              <span>Launch Multi-Agent Analysis</span>
              <ArrowRight size={18} />
            </>
          )}
        </button>
      </form>
    </div>
  );
};
