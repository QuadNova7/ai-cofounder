import Link from 'next/link';
import { ArrowLeft, Compass } from 'lucide-react';

export default function RoadmapPage() {
  return (
    <div style={{ textAlign: 'center', padding: '60px 20px' }}>
      <h2 style={{ fontSize: '1.8rem', fontWeight: 700, marginBottom: '12px' }}>90-Day GTM Roadmap</h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
        Roadmaps are generated specifically per active venture. Launch a venture to synthesize your customized 90-day plan.
      </p>
      <Link href="/startup/new" className="hero-cta-btn" style={{ display: 'inline-flex' }}>
        <Compass size={18} />
        <span>Launch New Venture</span>
      </Link>
    </div>
  );
}
