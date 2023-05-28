/**
 * https://ui.shadcn.com/docs/components/button
 */
import * as React from "react";

import { twMerge } from "tailwind-merge";

export const Button = React.forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement>
>(({ className, ...props }, ref) => {
  return (
    <button
      className={twMerge(
        "inline-flex items-center justify-center h-10 py-2 px-4 rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-foreground-muted focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background",
        "bg-primary text-primary-foreground hover:bg-primary/90",
        className
      )}
      ref={ref}
      {...props}
    />
  );
});
Button.displayName = "Button";
