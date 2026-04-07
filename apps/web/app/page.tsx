import Link from "next/link";
import { ArrowRight, Upload, BarChart3, Sparkles, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { SmoothScrollLink } from "@/components/ui/smooth-scroll-link";
import { AnimatedSection } from "@/components/ui/animated-section";

export default function LandingPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16 text-center">
          <AnimatedSection>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-50 text-blue-700 text-sm font-medium mb-8">
              <Sparkles className="w-4 h-4" />
              Impulsado por IA local (Ollama)
            </div>
          </AnimatedSection>
          
          <AnimatedSection delay="small">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 tracking-tight mb-6">
              Descubre qué tan compatible eres<br />
              <span className="text-blue-600">con tu próximo trabajo</span>
            </h1>
          </AnimatedSection>
          
          <AnimatedSection delay="medium">
            <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-10">
              TalentMatch AI analiza tu CV y lo compara con descripciones de puesto 
              usando embeddings semánticos. Obtén un score de compatibilidad y 
              recomendaciones personalizadas.
            </p>
          </AnimatedSection>
          
          <AnimatedSection delay="large">
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild className="shadow-md hover:shadow-lg transition-all hover:-translate-y-0.5">
                <Link href="/analyze">
                  Analizar mi CV
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Link>
              </Button>
              <Button size="lg" variant="outline" asChild className="hover:bg-gray-50 transition-all hover:-translate-y-0.5">
                <SmoothScrollLink href="#how-it-works">
                  Ver cómo funciona
                </SmoothScrollLink>
              </Button>
            </div>
          </AnimatedSection>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Todo lo que necesitas para optimizar tu búsqueda
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Nuestra plataforma combina procesamiento de lenguaje natural, 
              embeddings semánticos y análisis de IA para darte insights accionables.
            </p>
          </AnimatedSection>

          <div className="grid md:grid-cols-3 gap-8">
            <AnimatedSection delay="small">
              <Card className="group h-full hover:shadow-lg hover:-translate-y-1 transition-all duration-300 border-0 shadow-sm">
                <CardContent className="pt-6">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                    <Upload className="w-6 h-6 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    Sube tu CV
                  </h3>
                  <p className="text-gray-600">
                    Arrastra tu PDF o pega el texto directamente. Extraemos 
                    automáticamente tu información profesional.
                  </p>
                </CardContent>
              </Card>
            </AnimatedSection>

            <AnimatedSection delay="medium">
              <Card className="group h-full hover:shadow-lg hover:-translate-y-1 transition-all duration-300 border-0 shadow-sm">
                <CardContent className="pt-6">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                    <BarChart3 className="w-6 h-6 text-green-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    Análisis Semántico
                  </h3>
                  <p className="text-gray-600">
                    Comparamos tu perfil con la oferta usando embeddings. 
                    Más allá de keywords: entendemos el contexto.
                  </p>
                </CardContent>
              </Card>
            </AnimatedSection>

            <AnimatedSection delay="large">
              <Card className="group h-full hover:shadow-lg hover:-translate-y-1 transition-all duration-300 border-0 shadow-sm">
                <CardContent className="pt-6">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                    <Sparkles className="w-6 h-6 text-purple-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    Recomendaciones IA
                  </h3>
                  <p className="text-gray-600">
                    Recibe sugerencias personalizadas para mejorar tu CV 
                    y aumentar tus chances de ser contratado.
                  </p>
                </CardContent>
              </Card>
            </AnimatedSection>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Cómo funciona
            </h2>
            <p className="text-gray-600">
              Tres simples pasos para conocer tu compatibilidad
            </p>
          </AnimatedSection>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: "1",
                title: "Carga tu CV",
                description: "Sube tu CV en PDF o pega el texto. Nuestro sistema extrae automáticamente tu información.",
              },
              {
                step: "2",
                title: "Pega la oferta",
                description: "Copia la descripción del puesto que te interesa y pégala en el formulario.",
              },
              {
                step: "3",
                title: "Obtén insights",
                description: "Recibe un score de compatibilidad, análisis de fortalezas y recomendaciones.",
              },
            ].map((item, idx) => (
              <AnimatedSection key={item.step} delay={idx === 0 ? "small" : idx === 1 ? "medium" : "large"}>
                <div className="text-center group">
                  <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4 shadow-md group-hover:scale-110 transition-transform duration-300">
                    {item.step}
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {item.title}
                  </h3>
                  <p className="text-gray-600">{item.description}</p>
                </div>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <section className="py-20 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <AnimatedSection>
            <h2 className="text-3xl font-bold mb-4">Stack Tecnológico Moderno</h2>
            <p className="text-gray-400 mb-12 max-w-2xl mx-auto">
              Construido con tecnologías de vanguardia para máximo rendimiento y escalabilidad.
            </p>
          </AnimatedSection>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { name: "Next.js 16", desc: "Frontend React" },
              { name: "FastAPI", desc: "Backend Python" },
              { name: "Ollama", desc: "IA Local" },
              { name: "Tailwind", desc: "Estilos" },
            ].map((tech, idx) => (
              <AnimatedSection key={tech.name} delay={idx === 0 ? "small" : idx === 1 ? "medium" : idx === 2 ? "large" : "none"}>
                <div className="bg-gray-800 rounded-lg p-4 hover:bg-gray-700 transition-colors duration-300">
                  <div className="font-semibold">{tech.name}</div>
                  <div className="text-sm text-gray-400">{tech.desc}</div>
                </div>
              </AnimatedSection>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <AnimatedSection>
            <h2 className="text-3xl font-bold text-gray-900 mb-6">
              ¿Listo para optimizar tu CV?
            </h2>
            <p className="text-gray-600 mb-8">
              Comienza gratis. Sin registro necesario para el análisis básico.
            </p>
            <Button size="lg" asChild className="shadow-md hover:shadow-lg transition-all hover:-translate-y-0.5">
              <Link href="/analyze">
                Analizar mi CV ahora
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
            </Button>
          </AnimatedSection>
        </div>
      </section>
    </div>
  );
}
