"use client";

import { Briefcase, Github, Linkedin, Twitter } from "lucide-react";
import Link from "next/link";
import { SmoothScrollLink } from "@/components/ui/smooth-scroll-link";

export function Footer() {
  return (
    <footer className="bg-gray-50 border-t">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <Link href="/" className="flex items-center gap-2 mb-4 transition-opacity hover:opacity-80">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shadow-sm">
                <Briefcase className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-xl text-gray-900">TalentMatch AI</span>
            </Link>
            <p className="text-gray-600 max-w-sm">
              Análisis inteligente de CVs con IA. Compara tu perfil con ofertas 
              laborales y descubre tu compatibilidad en segundos.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-4">Producto</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/analyze" className="text-gray-600 hover:text-gray-900 transition-colors">
                  Analizar CV
                </Link>
              </li>
              <li>
                <SmoothScrollLink href="#features" className="text-gray-600 hover:text-gray-900 transition-colors">
                  Características
                </SmoothScrollLink>
              </li>
              <li>
                <SmoothScrollLink href="#how-it-works" className="text-gray-600 hover:text-gray-900 transition-colors">
                  Cómo funciona
                </SmoothScrollLink>
              </li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-4">Síguenos</h3>
            <div className="flex gap-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-gray-900 transition-colors"
              >
                <Github className="w-6 h-6" />
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-gray-900 transition-colors"
              >
                <Twitter className="w-6 h-6" />
              </a>
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-gray-900 transition-colors"
              >
                <Linkedin className="w-6 h-6" />
              </a>
            </div>
          </div>
        </div>

        <div className="border-t mt-8 pt-8 text-center text-gray-500 text-sm">
          © {new Date().getFullYear()} TalentMatch AI. Proyecto de portafolio.
        </div>
      </div>
    </footer>
  );
}
