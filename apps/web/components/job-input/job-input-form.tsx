"use client";

import { useState } from "react";
import { Briefcase, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { useAnalysisStore } from "@/lib/store/analysis-store";
import { JobDescription } from "@/types";

interface JobInputFormProps {
  onSubmit: (data: JobDescription) => void;
  isLoading?: boolean;
}

export function JobInputForm({ onSubmit, isLoading }: JobInputFormProps) {
  const [title, setTitle] = useState("");
  const [company, setCompany] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState<string | null>(null);

  const { cvData } = useAnalysisStore();

  const extractSkills = (text: string): string[] => {
    // Simple skill extraction - in production this would be smarter
    const commonSkills = [
      "python", "javascript", "typescript", "java", "react", "angular", "vue",
      "node.js", "docker", "kubernetes", "aws", "azure", "gcp", "sql",
      "mongodb", "postgresql", "git", "agile", "scrum", "machine learning",
      "data analysis", "project management", "leadership", "communication"
    ];
    
    const textLower = text.toLowerCase();
    return commonSkills.filter(skill => textLower.includes(skill.toLowerCase()));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!cvData) {
      setError("Primero debes cargar un CV");
      return;
    }

    if (!title.trim()) {
      setError("El título del puesto es obligatorio");
      return;
    }

    if (description.trim().length < 50) {
      setError("La descripción debe tener al menos 50 caracteres");
      return;
    }

    const requiredSkills = extractSkills(description);

    const jobData: JobDescription = {
      title: title.trim(),
      company: company.trim() || undefined,
      description: description.trim(),
      required_skills: requiredSkills,
      preferred_skills: [],
    };

    onSubmit(jobData);
  };

  const detectedSkills = description ? extractSkills(description) : [];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Briefcase className="w-5 h-5" />
          Descripción del Puesto
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Título del puesto *</label>
              <Input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="ej. Senior Full Stack Developer"
                disabled={isLoading}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Empresa</label>
              <Input
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="ej. Tech Corp"
                disabled={isLoading}
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Descripción completa *</label>
            <Textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Pega aquí la descripción completa de la oferta laboral..."
              className="min-h-[200px]"
              disabled={isLoading}
            />
            <p className="text-xs text-gray-500">
              Mínimo 50 caracteres. Incluye requisitos, responsabilidades y habilidades deseadas.
            </p>
          </div>

          {detectedSkills.length > 0 && (
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-600">
                Habilidades detectadas:
              </label>
              <div className="flex flex-wrap gap-2">
                {detectedSkills.map((skill) => (
                  <Badge key={skill} variant="secondary" className="text-xs">
                    {skill}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <Button
            type="submit"
            disabled={isLoading || !title || description.length < 50}
            className="w-full"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Analizando compatibilidad...
              </>
            ) : (
              "Calcular compatibilidad"
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
