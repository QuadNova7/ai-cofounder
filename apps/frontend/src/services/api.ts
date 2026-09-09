import { FounderInput, VentureState, HumanReviewPayload } from '../types/venture';

export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function startVenture(input: FounderInput): Promise<{ venture_id: string; status: string; message: string }> {
  const res = await fetch(`${API_BASE}/api/ventures/start`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(input),
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Failed to start venture: ${res.statusText}`);
  }

  return res.json();
}

export async function getVentureState(ventureId: string): Promise<VentureState> {
  const res = await fetch(`${API_BASE}/api/ventures/${ventureId}`);
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Failed to fetch venture state: ${res.statusText}`);
  }
  return res.json();
}

export async function submitHumanReview(
  ventureId: string,
  review: HumanReviewPayload
): Promise<{ venture_id: string; status: string; action_taken?: string }> {
  const res = await fetch(`${API_BASE}/api/ventures/${ventureId}/review`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(review),
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Failed to submit review: ${res.statusText}`);
  }

  return res.json();
}

export function getVentureStreamUrl(ventureId: string): string {
  return `${API_BASE}/api/ventures/${ventureId}/stream`;
}
