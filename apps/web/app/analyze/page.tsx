"use client";

import { useState } from "react";
import { ArrowLeft, Loader2 } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CVUploadZone } from "@/components/cv-upload/cv-upload-zone";
import { CVTextInput } from "@/components/cv-upload/cv-text-input";
import { JobInputForm } from "@/components/job-input/job-input-form";
import { ScoreDisplay } from "@/components/results/score-display";
import { AnalysisDetails } from "@/components/results/analysis-details";
import { api } from "@/lib/api/client";
import { useAnalysisStore } from "@/lib/store/analysis-store";
import { CVData, JobDescription, MatchResult } from "@/types";

export default function AnalyzePage() {
  const [activeTab, setActiveTab] = useState("upload");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    cvData,
    jobData,
    matchResult,
    setCVData,
    setJobData,
    setMatchResult,
    clearCurrent,
  } = useAnalysisStore();

  const handleCVSuccess = (data: CVData) => {
    setCVData(data);
  };

  const handleJobSubmit = async (job: JobDescription) => {
    if (!cvData) {
      setError("Primero debes cargar un CV");
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setJobData(job);

    try {
      const response = await api.analyzeMatch(cvData, job);

      if (response.success && response.data) {
        setMatchResult(response.data.match_result);
      } else {
        setError(response.message || "Error analyzing match");
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : "Analysis failed";
      setError(message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    clearCurrent();
    setError(null);
    setActiveTab("upload");
  };

  // Show results if we have a match result
  if (matchResult) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-6">
            <Button variant="ghost" onClick={handleReset} className="gap-2">
              <ArrowLeft className="w-4 h-4" />
              Nuevo análisis
            </Button>
          </div>

          <ScoreDisplay result={matchResult} />

          <div className="mt-8">
            <AnalysisDetails analysis={matchResult.analysis} />
          </div>

          {cvData && jobData && (
            <div className="mt-8 bg-white rounded-lg p-6 border">
              <h3 className="font-semibold text-gray-900 mb-4">Resumen del análisis</h3>
              <div className="grid md:grid-cols-2 gap-6 text-sm">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">CV analizado:</h4>
                  <p className="text-gray-600">
                    {cvData.personal_info.name || "Candidato"}
                  </p>
                  <p className="text-gray-500">
                    {cvData.experience.length} experiencias, {" "}
                    {cvData.skills.technical.length} habilidades técnicas
                  </p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Puesto objetivo:</h4>
                  <p className="text-gray-600">{jobData.title}</p>
                  {jobData.company && (
                    <p className="text-gray-500">{jobData.company}</p>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <Link
            href="/"
            className="text-sm text-gray-500 hover:text-gray-900 flex items-center gap-1"
          >
            <ArrowLeft className="w-4 h-4" />
            Volver al inicio
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 mt-4">
            Analiza tu CV
          </h1>
          <p className="text-gray-600 mt-2">
            Sube tu CV y compáralo con una oferta laboral para obtener insights.
          </p>
        </div>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Step 1: CV Input */}
        {!cvData && (
          <div className="space-y-6">
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="upload">Subir PDF</TabsTrigger>
                <TabsTrigger value="text">Pegar texto</TabsTrigger>
              </TabsList>

              <TabsContent value="upload" className="mt-6">
                <CVUploadZone onSuccess={handleCVSuccess} />
              </TabsContent>

              <TabsContent value="text" className="mt-6">
                <CVTextInput onSuccess={handleCVSuccess} />
              </TabsContent>
            </Tabs>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-medium text-blue-900 mb-1">💡 Consejo</h4>
              <p className="text-sm text-blue-700">
                Para mejores resultados, asegúrate de que tu CV incluya información 
                clara sobre tu experiencia, habilidades técnicas y formación.
              </p>
            </div>
          </div>
        )}

        {/* Step 2: Job Input */}
        {cvData && !matchResult && (
          <div className="space-y-6">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-green-600 font-bold">✓</span>
                </div>
                <div>
                  <h4 className="font-medium text-green-900">CV cargado correctamente</h4>
                  <p className="text-sm text-green-700">
                    {cvData.personal_info.name || "Candidato"} • {" "}
                    {cvData.experience.length} experiencias • {" "}
                    {cvData.skills.technical.length} habilidades
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setCVData(null)}
                  className="ml-auto text-green-700 hover:text-green-900"
                >
                  Cambiar
                </Button>
              </div>
            </div>

            <JobInputForm onSubmit={handleJobSubmit} isLoading={isAnalyzing} />
          </div>
        )}

        {/* Loading State */}
        {isAnalyzing && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-8 text-center">
              <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900">
                Analizando compatibilidad...
              </h3>
              <p className="text-gray-600 mt-2">
                Esto puede tomar 10-30 segundos dependiendo de la carga.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
