import './globals.css';
import RegisterSW from '@/components/pwa/RegisterSW';
import { ReactNode } from 'react';
export const metadata = { title: 'NeuroEdge', description: 'NeuroEdge frontend' };
export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen">
          {children}
        <RegisterSW />
        </div>
      </body>
    </html>
  );
}
