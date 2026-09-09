import type { Metadata } from 'next';
import './globals.css';
import Link from 'next/link';
import { Sparkles, Compass } from 'lucide-react';

export const metadata: Metadata = {
  title: 'AI Co-Founder | Autonomous Multi-Agent Advisory System',
  description: 'Autonomous multi-agent platform that validates startup ideas, analyzes market viability, crafts business models, estimates revenues, and generates 90-day GTM roadmaps.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <header className="header-bar">
          <Link href="/" className="brand">
            <Sparkles size={20} color="#6366f1" />
            <span>AI Co-Founder</span>
            <span className="brand-badge">Multi-Agent</span>
          </Link>
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <Link
              href="/startup/new"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                fontSize: '0.88rem',
                fontWeight: 600,
                color: '#818cf8',
                padding: '6px 14px',
                borderRadius: '9999px',
                background: 'rgba(99, 102, 241, 0.12)',
                border: '1px solid rgba(99, 102, 241, 0.3)',
              }}
            >
              <Compass size={16} />
              <span>+ New Venture</span>
            </Link>
          </div>
        </header>
        <div className="app-container">{children}</div>
      </body>
    </html>
  );
}
