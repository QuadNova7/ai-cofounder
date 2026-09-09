export type WorkflowStage =
  | 'INITIALIZED'
  | 'IDEA_ANALYSIS'
  | 'MARKET_RESEARCH'
  | 'CRITIC_VALIDATION'
  | 'REPLANNING'
  | 'BUSINESS_MODEL'
  | 'REVENUE_ESTIMATION'
  | 'MARKETING'
  | 'ROADMAP_COMPILATION'
  | 'COMPLETED'
  | 'FAILED';

export interface FounderInput {
  startup_idea: string;
  target_market: string;
  target_geography?: string;
  budget?: number;
  timeline_months?: number;
  goals?: string;
  constraints?: string[];
  skills_resources?: string;
}

export interface IdeaAnalysisOutput {
  problem_statement: string;
  target_users: string[];
  refined_value_proposition: string;
  key_assumptions: string[];
  red_flags: string[];
  clarity_score: number;
  feasibility_score: number;
  confidence_score: number;
}

export interface Competitor {
  name: string;
  description: string;
  strengths: string[];
  weaknesses: string[];
  pricing_model?: string;
  website_url?: string;
}

export interface MarketResearchOutput {
  competitor_landscape: Competitor[];
  customer_personas: Array<Record<string, string>>;
  market_trends: string[];
  entry_barriers: string[];
  tam_estimate?: number;
  sam_estimate?: number;
  som_estimate?: number;
  supporting_evidence: string[];
  source_urls: string[];
  confidence_score: number;
}

export interface CriticValidationOutput {
  status: string;
  confidence_score: number;
  unsupported_claims: string[];
  verified_sources_count: number;
  feedback_notes: string;
  requires_pivot: boolean;
  suggested_alternatives: string[];
}

export interface BusinessModelCanvas {
  key_partners: string[];
  key_activities: string[];
  key_resources: string[];
  value_propositions: string[];
  customer_relationships: string[];
  channels: string[];
  customer_segments: string[];
  cost_structure: string[];
  revenue_streams: string[];
}

export interface BusinessModelOutput {
  framework_used: string;
  canvas: BusinessModelCanvas;
  key_risks: string[];
  mitigations: string[];
  confidence_score: number;
}

export interface FinancialParameters {
  monthly_price: number;
  starting_customers: number;
  monthly_growth_rate: number;
  monthly_churn_rate: number;
  cogs_per_unit: number;
  fixed_monthly_costs: number;
}

export interface ProjectionScenario {
  scenario_name: string;
  month_12_revenue: number;
  month_12_customers: number;
  break_even_month?: number | null;
  monthly_projections: Array<Record<string, any>>;
}

export interface RevenueEstimationOutput {
  pricing_strategy: string;
  parameters: FinancialParameters;
  scenarios: ProjectionScenario[];
  tam_sam_som_valid: boolean;
  assumptions_summary: string[];
}

export interface Milestone {
  month: number;
  focus: string;
  target_kpi: string;
  deliverables: string[];
}

export interface MarketingPlanOutput {
  positioning_statement: string;
  priority_channels: string[];
  messaging_framework: Record<string, string>;
  gtm_90_day_plan: Milestone[];
  acquisition_tactics: string[];
  budget_allocation: Record<string, number>;
  prioritized_next_actions: string[];
}

export interface StartupRoadmap {
  venture_id: string;
  venture_name: string;
  founder_input: FounderInput;
  idea_analysis: IdeaAnalysisOutput;
  market_research: MarketResearchOutput;
  business_model: BusinessModelOutput;
  revenue_estimation: RevenueEstimationOutput;
  marketing_plan: MarketingPlanOutput;
  overall_confidence_score: number;
  executive_summary: string;
  disclaimer: string;
}

export interface VentureState {
  venture_id: string;
  founder_input: FounderInput;
  current_stage: WorkflowStage;
  idea_analysis?: IdeaAnalysisOutput | null;
  market_research?: MarketResearchOutput | null;
  market_validation?: CriticValidationOutput | null;
  business_model?: BusinessModelOutput | null;
  revenue_estimation?: RevenueEstimationOutput | null;
  marketing_plan?: MarketingPlanOutput | null;
  final_roadmap?: StartupRoadmap | null;
  critique_history?: CriticValidationOutput[];
  retry_counts?: Record<string, number>;
  market_replan_count?: number;
  finance_retune_count?: number;
  replan_count?: number;
  warnings?: string[];
  human_review_required?: boolean;
  human_review_notes?: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface SSEEventEnvelope {
  event_type: string;
  venture_id: string;
  stage: WorkflowStage;
  progress_pct: number;
  message: string;
  data?: Record<string, any>;
  timestamp: string;
}

export interface HumanReviewPayload {
  action: 'PROCEED_ANYWAY' | 'OVERRIDE_ASSUMPTIONS' | 'ABORT';
  notes?: string;
}
