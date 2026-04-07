"use client";

import { useState } from "react";
import { FileText, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { api } from "@/lib/api/client";
import { useAnalysisStore } from "@/lib/store/analysis-store";
import { CVData } from "@/types";

interface CVTextInputProps {
  onSuccess?: (data: CVData) => void;
}

export function CVTextInput({ onSuccess }: CVTextInputProps) {
  const [text, setText] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { setCVData, setError: setStoreError } = useAnalysisStore();

  const handleSubmit = async () => {
    if (text.trim().length < 50) {
      setError("Por favor ingresa al menos 50 caracteres");
      return;
    }

    setIsProcessing(true);
    setError(null);
    setStoreError(null);

    try {
      const response = await api.parseCVText(text);
      
      if (response.success && response.data) {
        setCVData(response.data);
        onSuccess?.(response.data);
      } else {
        setError(response.message || "Failed to process text");
        setStoreError(response.message || "Failed to process text");
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : "Processing failed";
      setError(message);
      setStoreError(message);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleClear = () => {
    setText("");
    setCVData(null);
    setError(null);
  };

  return (
    <Card>
      <CardContent className="p-6 space-y-4">
        <div className="flex items-center gap-2 text-gray-700">
          <FileText className="w-5 h-5" />
          <h3 className="font-medium">Pega el texto de tu CV</h3>
        </div>
        
        <Textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Pega aquí el contenido de tu CV..."
          className="min-h-[200px] resize-none"
          disabled={isProcessing}
        />
        
        <div className="flex justify-between items-center text-sm text-gray-500">
          <span>{text.length} caracteres</span>
          <span>Mínimo recomendado: 200</span>
        </div>

        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <div className="flex gap-2">
          <Button
            onClick={handleSubmit}
            disabled={isProcessing || text.trim().length < 50}
            className="flex-1"
          >
            {isProcessing ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Procesando...
              </>
            ) : (
              "Analizar CV"
            )}
          </Button>
          {text && (
            <Button
              variant="outline"
              onClick={handleClear}
              disabled={isProcessing}
            >
              Limpiar
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
