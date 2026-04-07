"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, FileText, Loader2, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { api } from "@/lib/api/client";
import { useAnalysisStore } from "@/lib/store/analysis-store";
import { CVData } from "@/types";

interface CVUploadZoneProps {
  onSuccess?: (data: CVData) => void;
}

export function CVUploadZone({ onSuccess }: CVUploadZoneProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const { setCVData, setError: setStoreError } = useAnalysisStore();

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];
      if (!file) return;

      setIsUploading(true);
      setError(null);
      setStoreError(null);

      try {
        const response = await api.uploadCV(file);
        
        if (response.success && response.data) {
          setUploadedFile(file);
          setCVData(response.data);
          onSuccess?.(response.data);
        } else {
          setError(response.message || "Failed to process CV");
          setStoreError(response.message || "Failed to process CV");
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : "Upload failed";
        setError(message);
        setStoreError(message);
      } finally {
        setIsUploading(false);
      }
    },
    [onSuccess, setCVData, setStoreError]
  );

  const onDropRejected = useCallback(
    (fileRejections: any[]) => {
      const rejection = fileRejections[0];
      if (!rejection) return;

      const fileTypeError = rejection.errors.find(
        (e: any) => e.code === "file-invalid-type"
      );
      const fileSizeError = rejection.errors.find(
        (e: any) => e.code === "file-too-large"
      );

      if (fileTypeError) {
        setError("Solo se permite subir archivos PDF. Por favor, selecciona un archivo con extensión .pdf");
      } else if (fileSizeError) {
        setError("El archivo es demasiado grande. El tamaño máximo permitido es 10MB.");
      } else {
        setError("No se pudo subir el archivo. Verifica que sea un PDF válido de menos de 10MB.");
      }
    },
    []
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    onDropRejected,
    accept: {
      "application/pdf": [".pdf"],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
    disabled: isUploading,
  });

  const handleRemove = () => {
    setUploadedFile(null);
    setCVData(null);
    setError(null);
    setStoreError(null);
  };

  if (uploadedFile) {
    return (
      <Card className="border-green-200 bg-green-50/50">
        <CardContent className="p-6">
          <div className="flex items-center gap-4">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-medium text-gray-900 truncate">
                {uploadedFile.name}
              </p>
              <p className="text-sm text-gray-500">
                {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleRemove}
              className="text-gray-500 hover:text-red-600"
            >
              Cambiar
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <Card
        {...getRootProps()}
        className={`
          border-2 border-dashed cursor-pointer transition-colors
          ${isDragActive ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-gray-400"}
          ${isUploading ? "opacity-50 cursor-not-allowed" : ""}
        `}
      >
        <CardContent className="p-8">
          <input {...getInputProps()} />
          <div className="flex flex-col items-center text-center">
            {isUploading ? (
              <>
                <Loader2 className="w-12 h-12 text-blue-500 animate-spin mb-4" />
                <p className="text-lg font-medium text-gray-900">
                  Analizando tu CV...
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  Esto puede tomar unos segundos
                </p>
              </>
            ) : (
              <>
                <div className="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mb-4 transition-colors">
                  {isDragActive ? (
                    <Upload className="w-8 h-8 text-blue-500" />
                  ) : (
                    <FileText className="w-8 h-8 text-gray-400" />
                  )}
                </div>
                <p className="text-lg font-medium text-gray-900">
                  {isDragActive
                    ? "Suelta tu CV aquí"
                    : "Arrastra tu CV o haz clic para seleccionar"}
                </p>
                <p className="text-sm text-gray-500 mt-2">
                  PDF hasta 10MB
                </p>
              </>
            )}
          </div>
        </CardContent>
      </Card>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
    </div>
  );
}
