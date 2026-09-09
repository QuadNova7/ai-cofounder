import Link from 'next/link';
import { ArrowRight, Compass, ShieldCheck, LineChart, Calendar } from 'lucide-react';

export default function HomePage() {
  return (
    <div>
      <section className="hero-wrapper">
        <div className="hero-pill">
          <span>✨ Autonomous Multi-Agent Advisory Platform</span>
        </div>

        <h1 className="hero-title">Your On-Demand Autonomous AI Co-Founder</h1>

        <p className="hero-description">
          Validate raw startup ideas with grounded live web research, stress-test business models,
          estimate deterministic unit economics, and formulate actionable 90-day GTM roadmaps.
        </p>

        <Link href="/startup/new" className="hero-cta-btn">
          <Compass size={20} />
          <span>Start New Venture</span>
          <ArrowRight size={18} />
        </Link>

        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">💡</div>
            <h3>Idea & Problem Clarification</h3>
            <p>Deconstructs customer pain points, value propositions, and surfaces critical blindspots.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>Live Market Research & Critic</h3>
            <p>Grounded live web research analyzes competitor landscapes with factual evidence validation.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Deterministic Financial Engine</h3>
            <p>Calculates strict TAM/SAM/SOM boundaries, unit economics, and 12-month runway projections.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🚀</div>
            <h3>90-Day Actionable GTM Plan</h3>
            <p>Produces phased month-by-month milestone targets, key KPIs, and prioritized founder tasks.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
