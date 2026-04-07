"use client";

import Link from "next/link";
import { Briefcase, Menu, X } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { SmoothScrollLink } from "@/components/ui/smooth-scroll-link";

export function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center gap-2 transition-opacity hover:opacity-80">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shadow-sm">
                <Briefcase className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-xl text-gray-900">TalentMatch</span>
              <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-medium">
                AI
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6">
            <SmoothScrollLink 
              href="#features" 
              className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
            >
              Características
            </SmoothScrollLink>
            <SmoothScrollLink 
              href="#how-it-works" 
              className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
            >
              Cómo funciona
            </SmoothScrollLink>
            <Button asChild className="shadow-sm hover:shadow transition-shadow">
              <Link href="/analyze">Analizar CV</Link>
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="flex items-center md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-600 hover:text-gray-900 p-2 rounded-md hover:bg-gray-100 transition-colors"
            >
              {isMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className="md:hidden border-t bg-white">
          <div className="px-4 pt-2 pb-4 space-y-1">
            <SmoothScrollLink
              href="#features"
              className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              Características
            </SmoothScrollLink>
            <SmoothScrollLink
              href="#how-it-works"
              className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              Cómo funciona
            </SmoothScrollLink>
            <Link
              href="/analyze"
              className="block px-3 py-2 rounded-md text-base font-medium text-blue-600 hover:bg-blue-50 transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              Analizar CV
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}
