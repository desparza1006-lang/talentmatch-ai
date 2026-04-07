"use client";

import React from "react";
import { useInView } from "@/lib/hooks/use-in-view";
import { cn } from "@/lib/utils";

interface AnimatedSectionProps {
  children: React.ReactNode;
  className?: string;
  delay?: "none" | "small" | "medium" | "large";
}

export function AnimatedSection({
  children,
  className,
  delay = "none",
}: AnimatedSectionProps) {
  const { ref, isInView } = useInView<HTMLDivElement>({ threshold: 0.1 });

  const delayClass = {
    none: "",
    small: "delay-100",
    medium: "delay-200",
    large: "delay-300",
  }[delay];

  return (
    <div
      ref={ref}
      className={cn(
        "transition-all duration-700 ease-out",
        delayClass,
        isInView
          ? "opacity-100 translate-y-0"
          : "opacity-0 translate-y-6",
        className
      )}
    >
      {children}
    </div>
  );
}
