import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Agentic Financial Planner",
  description: "Multi-agent financial planning demo"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main className="page">{children}</main>
      </body>
    </html>
  );
}
