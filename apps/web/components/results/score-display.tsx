"use client";

import { CheckCircle, AlertCircle, XCircle, Zap } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { MatchResult } from "@/types";

interface ScoreDisplayProps {
  result: MatchResult;
}

export function ScoreDisplay({ result }: ScoreDisplayProps) {
  const { overall_score, section_scores, summary } = result;

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-green-600";
    if (score >= 60) return "text-blue-600";
    if (score >= 40) return "text-yellow-600";
    return "text-red-600";
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return "bg-green-600";
    if (score >= 60) return "bg-blue-600";
    if (score >= 40) return "bg-yellow-600";
    return "bg-red-600";
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return { text: "Excelente match", icon: Zap, color: "text-green-600", bg: "bg-green-100" };
    if (score >= 60) return { text: "Buen match", icon: CheckCircle, color: "text-blue-600", bg: "bg-blue-100" };
    if (score >= 40) return { text: "Match moderado", icon: AlertCircle, color: "text-yellow-600", bg: "bg-yellow-100" };
    return { text: "Necesita mejoras", icon: XCircle, color: "text-red-600", bg: "bg-red-100" };
  };

  const scoreInfo = getScoreLabel(overall_score);
  const ScoreIcon = scoreInfo.icon;

  return (
    <Card className="border-2">
      <CardHeader className="pb-4">
        <CardTitle className="text-center text-2xl">Resultado del Análisis</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Overall Score */}
        <div className="text-center">
          <div className={`text-6xl font-bold ${getScoreColor(overall_score)}`}>
            {overall_score.toFixed(0)}%
          </div>
          <div className={`inline-flex items-center gap-2 mt-3 px-4 py-2 rounded-full ${scoreInfo.bg}`}>
            <ScoreIcon className={`w-5 h-5 ${scoreInfo.color}`} />
            <span className={`font-medium ${scoreInfo.color}`}>{scoreInfo.text}</span>
          </div>
        </div>

        {/* Summary */}
        <p className="text-gray-600 text-center max-w-lg mx-auto">
          {summary}
        </p>

        {/* Section Scores */}
        <div className="space-y-4 pt-4 border-t">
          <h4 className="font-medium text-gray-700">Desglose por sección:</h4>
          {section_scores.map((section) => (
            <div key={section.name} className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">{section.name}</span>
                <span className="font-medium">{section.score.toFixed(0)}%</span>
              </div>
              <Progress 
                value={section.score} 
                className="h-2"
              />
              {section.details && (
                <p className="text-xs text-gray-500">{section.details}</p>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
