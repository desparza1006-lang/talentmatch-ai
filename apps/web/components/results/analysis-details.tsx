"use client";

import { CheckCircle, AlertTriangle, Lightbulb, Target } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MatchAnalysis } from "@/types";

interface AnalysisDetailsProps {
  analysis: MatchAnalysis;
}

export function AnalysisDetails({ analysis }: AnalysisDetailsProps) {
  const { strengths, gaps, recommendations, skill_comparison } = analysis;

  return (
    <Tabs defaultValue="skills" className="w-full">
      <TabsList className="grid w-full grid-cols-4">
        <TabsTrigger value="skills">Habilidades</TabsTrigger>
        <TabsTrigger value="strengths">Fortalezas</TabsTrigger>
        <TabsTrigger value="gaps">Brechas</TabsTrigger>
        <TabsTrigger value="recommendations">Recomendaciones</TabsTrigger>
      </TabsList>

      {/* Skills Tab */}
      <TabsContent value="skills" className="mt-4">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Target className="w-5 h-5 text-blue-500" />
              Comparación de Habilidades
              <Badge variant={skill_comparison.match_percentage >= 60 ? "default" : "destructive"}>
                {skill_comparison.match_percentage.toFixed(0)}% match
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Matched Skills */}
            <div>
              <h4 className="text-sm font-medium text-green-700 mb-2 flex items-center gap-2">
                <CheckCircle className="w-4 h-4" />
                Habilidades coincidentes ({skill_comparison.matched.length})
              </h4>
              <div className="flex flex-wrap gap-2">
                {skill_comparison.matched.length > 0 ? (
                  skill_comparison.matched.map((skill) => (
                    <Badge key={skill} variant="secondary" className="bg-green-50 text-green-700 hover:bg-green-100">
                      {skill}
                    </Badge>
                  ))
                ) : (
                  <span className="text-gray-500 text-sm">No se encontraron coincidencias exactas</span>
                )}
              </div>
            </div>

            <Separator />

            {/* Missing Skills */}
            <div>
              <h4 className="text-sm font-medium text-red-700 mb-2 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                Habilidades faltantes ({skill_comparison.missing.length})
              </h4>
              <div className="flex flex-wrap gap-2">
                {skill_comparison.missing.length > 0 ? (
                  skill_comparison.missing.map((skill) => (
                    <Badge key={skill} variant="outline" className="border-red-300 text-red-600">
                      {skill}
                    </Badge>
                  ))
                ) : (
                  <span className="text-gray-500 text-sm">¡Excelente! Tienes todas las habilidades requeridas</span>
                )}
              </div>
            </div>

            <Separator />

            {/* Extra Skills */}
            <div>
              <h4 className="text-sm font-medium text-blue-700 mb-2">
                Habilidades adicionales que te diferencian ({skill_comparison.extra.length})
              </h4>
              <div className="flex flex-wrap gap-2">
                {skill_comparison.extra.length > 0 ? (
                  skill_comparison.extra.slice(0, 10).map((skill) => (
                    <Badge key={skill} variant="outline" className="border-blue-300 text-blue-600">
                      {skill}
                    </Badge>
                  ))
                ) : (
                  <span className="text-gray-500 text-sm">No se detectaron habilidades adicionales</span>
                )}
                {skill_comparison.extra.length > 10 && (
                  <Badge variant="outline">+{skill_comparison.extra.length - 10} más</Badge>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      {/* Strengths Tab */}
      <TabsContent value="strengths" className="mt-4">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <CheckCircle className="w-5 h-5 text-green-500" />
              Tus Fortalezas
            </CardTitle>
          </CardHeader>
          <CardContent>
            {strengths.length > 0 ? (
              <ul className="space-y-3">
                {strengths.map((strength, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <CheckCircle className="w-4 h-4 text-green-600" />
                    </div>
                    <span className="text-gray-700">{strength}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-center py-4">
                No se identificaron fortalezas específicas para este puesto.
              </p>
            )}
          </CardContent>
        </Card>
      </TabsContent>

      {/* Gaps Tab */}
      <TabsContent value="gaps" className="mt-4">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <AlertTriangle className="w-5 h-5 text-amber-500" />
              Áreas de Mejora
            </CardTitle>
          </CardHeader>
          <CardContent>
            {gaps.length > 0 ? (
              <ul className="space-y-3">
                {gaps.map((gap, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="w-6 h-6 rounded-full bg-amber-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <AlertTriangle className="w-4 h-4 text-amber-600" />
                    </div>
                    <span className="text-gray-700">{gap}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-center py-8">
                <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-3" />
                <p className="text-gray-600 font-medium">¡No se identificaron brechas importantes!</p>
                <p className="text-gray-500 text-sm">Tu perfil está bien alineado con este puesto.</p>
              </div>
            )}
          </CardContent>
        </Card>
      </TabsContent>

      {/* Recommendations Tab */}
      <TabsContent value="recommendations" className="mt-4">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Lightbulb className="w-5 h-5 text-yellow-500" />
              Recomendaciones
            </CardTitle>
          </CardHeader>
          <CardContent>
            {recommendations.length > 0 ? (
              <ul className="space-y-3">
                {recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="w-6 h-6 rounded-full bg-yellow-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <Lightbulb className="w-4 h-4 text-yellow-600" />
                    </div>
                    <span className="text-gray-700">{rec}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-center py-4">
                No hay recomendaciones específicas en este momento.
              </p>
            )}
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
  );
}
