import Link from 'next/link';
import { ArrowLeft, Compass } from 'lucide-react';

export default function DashboardPage() {
  return (
    <div style={{ textAlign: 'center', padding: '60px 20px' }}>
      <h2 style={{ fontSize: '1.8rem', fontWeight: 700, marginBottom: '12px' }}>Venture Dashboard</h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
        Start a new venture to view real-time agent progression and strategic analysis.
      </p>
      <Link href="/startup/new" className="hero-cta-btn" style={{ display: 'inline-flex' }}>
        <Compass size={18} />
        <span>Launch New Venture</span>
      </Link>
    </div>
  );
}
