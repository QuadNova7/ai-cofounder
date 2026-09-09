'use client';

import React, { useState, useEffect, useRef } from 'react';
import { VentureState, WorkflowStage } from '../types/venture';
import { IdeaAnalysisView } from './results/IdeaAnalysisView';
import { MarketResearchView } from './results/MarketResearchView';
import { BusinessModelView } from './results/BusinessModelView';
import { RevenueProjectionsView } from './results/RevenueProjectionsView';
import { MarketingPlanView } from './results/MarketingPlanView';
import { RoadmapView } from './results/RoadmapView';
import {
  Lightbulb,
  Search,
  LayoutGrid,
  TrendingUp,
  Megaphone,
  Award,
  CheckCircle2,
  Loader2,
} from 'lucide-react';

interface AgentResultsViewProps {
  venture: VentureState | null;
  currentStage: WorkflowStage;
}

type TabKey = 'idea' | 'market' | 'canvas' | 'finance' | 'marketing' | 'roadmap';

interface TabDef {
  key: TabKey;
  label: string;
  icon: React.ReactNode;
  stageTrigger: WorkflowStage[];
  isCompleted: (v: VentureState | null) => boolean;
  isRunning: (stage: WorkflowStage) => boolean;
}

export const AgentResultsView: React.FC<AgentResultsViewProps> = ({ venture, currentStage }) => {
  const [activeTab, setActiveTab] = useState<TabKey>('idea');
  const prevStageRef = useRef<WorkflowStage>(currentStage);

  const TABS: TabDef[] = [
    {
      key: 'idea',
      label: 'Idea Analysis',
      icon: <Lightbulb size={16} />,
      stageTrigger: ['IDEA_ANALYSIS'],
      isCompleted: (v) => Boolean(v?.idea_analysis),
      isRunning: (s) => s === 'IDEA_ANALYSIS',
    },
    {
      key: 'market',
      label: 'Market & Critic',
      icon: <Search size={16} />,
      stageTrigger: ['MARKET_RESEARCH', 'CRITIC_VALIDATION'],
      isCompleted: (v) => Boolean(v?.market_research || v?.market_validation),
      isRunning: (s) => s === 'MARKET_RESEARCH' || s === 'CRITIC_VALIDATION' || s === 'REPLANNING',
    },
    {
      key: 'canvas',
      label: 'Business Model',
      icon: <LayoutGrid size={16} />,
      stageTrigger: ['BUSINESS_MODEL'],
      isCompleted: (v) => Boolean(v?.business_model),
      isRunning: (s) => s === 'BUSINESS_MODEL',
    },
    {
      key: 'finance',
      label: 'Financial Engine',
      icon: <TrendingUp size={16} />,
      stageTrigger: ['REVENUE_ESTIMATION'],
      isCompleted: (v) => Boolean(v?.revenue_estimation),
      isRunning: (s) => s === 'REVENUE_ESTIMATION',
    },
    {
      key: 'marketing',
      label: 'Marketing Plan',
      icon: <Megaphone size={16} />,
      stageTrigger: ['MARKETING'],
      isCompleted: (v) => Boolean(v?.marketing_plan),
      isRunning: (s) => s === 'MARKETING',
    },
    {
      key: 'roadmap',
      label: 'Final Roadmap',
      icon: <Award size={16} />,
      stageTrigger: ['ROADMAP_COMPILATION', 'COMPLETED'],
      isCompleted: (v) => Boolean(v?.final_roadmap),
      isRunning: (s) => s === 'ROADMAP_COMPILATION',
    },
  ];

  // Auto-switch to newly completed agent stage tab
  useEffect(() => {
    if (prevStageRef.current !== currentStage) {
      if (currentStage === 'MARKET_RESEARCH' && venture?.idea_analysis) {
        setActiveTab('idea');
      } else if (currentStage === 'BUSINESS_MODEL' && (venture?.market_research || venture?.market_validation)) {
        setActiveTab('market');
      } else if (currentStage === 'REVENUE_ESTIMATION' && venture?.business_model) {
        setActiveTab('canvas');
      } else if (currentStage === 'MARKETING' && venture?.revenue_estimation) {
        setActiveTab('finance');
      } else if (currentStage === 'ROADMAP_COMPILATION' && venture?.marketing_plan) {
        setActiveTab('marketing');
      } else if (currentStage === 'COMPLETED' && venture?.final_roadmap) {
        setActiveTab('roadmap');
      }
      prevStageRef.current = currentStage;
    }
  }, [currentStage, venture]);

  return (
    <div className="tabs-container">
      {/* Tab Navigation */}
      <div className="tabs-nav">
        {TABS.map((tab) => {
          const completed = tab.isCompleted(venture);
          const running = tab.isRunning(currentStage);
          const isActive = activeTab === tab.key;

          return (
            <button
              key={tab.key}
              type="button"
              className={`tab-btn ${isActive ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.key)}
            >
              {tab.icon}
              <span>{tab.label}</span>

              {completed ? (
                <span className="tab-badge done">
                  <CheckCircle2 size={12} />
                </span>
              ) : running ? (
                <span className="tab-badge running">
                  <Loader2 size={12} className="spin" />
                </span>
              ) : (
                <span className="tab-badge pending">—</span>
              )}
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'idea' && <IdeaAnalysisView data={venture?.idea_analysis} />}
        {activeTab === 'market' && (
          <MarketResearchView
            marketData={venture?.market_research}
            criticData={venture?.market_validation}
          />
        )}
        {activeTab === 'canvas' && <BusinessModelView data={venture?.business_model} />}
        {activeTab === 'finance' && <RevenueProjectionsView data={venture?.revenue_estimation} />}
        {activeTab === 'marketing' && <MarketingPlanView data={venture?.marketing_plan} />}
        {activeTab === 'roadmap' && <RoadmapView data={venture?.final_roadmap} />}
      </div>
    </div>
  );
};
